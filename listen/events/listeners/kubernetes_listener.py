###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import argparse
import datetime
import uuid
from time import sleep

import os
import warnings
from kubernetes.client import Configuration as KubeConf, CoreV1Api
from kubernetes.watch import Watch
from urllib3.exceptions import ReadTimeoutError

from base.messages.message import Message
from base.utils.configuration import Configuration
from base.utils.constants import EnvironmentFeatures, OperationalStatus
from base.utils.exceptions import ResourceGoneError
from base.utils.inventory_mgr import InventoryMgr
from base.utils.kube_utils import update_resource_version
from base.utils.logging.logger import Logger
from base.utils.mongo_access import MongoAccess
from base.utils.util import setup_args
from listen.event_handler import EventHandler
from listen.events.event_base import EventResult
from listen.events.kube.kube_metadata_parser import parse_metadata_file, KubeMetadataParser
from listen.events.listeners.listener_base import ListenerBase
from monitoring.setup.monitoring_setup_manager import MonitoringSetupManager


class KubernetesListener(ListenerBase):

    SOURCE_SYSTEM = "Kubernetes"
    COMMON_METADATA_FILE = "kube_events.json"

    LOG_FILENAME = "kubernetes_listener.log"
    LOG_LEVEL = Logger.INFO

    DEFAULTS = {
        "env": "Kubernetes",
        "mongo_config": "",
        "metadata_file": "",
        "inventory": "inventory",
        "loglevel": "INFO",
        "environments_collection": "environments_config",
        "resource_versions": {},
        "request_timeout": 1,
        "polling_interval": 1
    }

    def __init__(self, config, event_handler,
                 environment: str = DEFAULTS["env"],
                 inventory_collection: str = DEFAULTS["inventory"],
                 connection_pool_size: int = 10,
                 request_timeout: int = 1,
                 polling_inverval: int = 1,
                 process_vars: dict = None):
        super().__init__(environment=environment)
        self.handler = event_handler

        self.inv = InventoryMgr()
        self.inv.set_collections(inventory_collection)
        if self.inv.is_feature_supported(self.environment,
                                         EnvironmentFeatures.MONITORING):
            self.inv.monitoring_setup_manager = \
                MonitoringSetupManager(self.environment)

        self.base_url = 'https://{}:{}'.format(config['host'], config['port'])
        self.bearer_token = config.get('token', '')
        conf = KubeConf()
        conf.host = self.base_url
        conf.user = config['user']
        conf.api_key_prefix['authorization'] = 'Bearer'
        conf.api_key['authorization'] = self.bearer_token
        conf.verify_ssl = False
        conf.connection_pool_maxsize = connection_pool_size
        self.api = CoreV1Api()

        self.watch = Watch()
        self.endpoints = {}
        self.resource_versions = {}
        self.request_timeout = request_timeout
        self.polling_interval = polling_inverval
        self.process_vars = process_vars if process_vars is not None else {}

    def process_event(self, event):
        received_timestamp = datetime.datetime.now()

        event_type = ".".join(
            (event['object'].kind, event['type'])
        ).lower()
        result = self.handle_event(event_type=event_type, notification=event)

        finished_timestamp = datetime.datetime.now()
        self.save_message(message_body=event,
                          result=result,
                          started=received_timestamp,
                          finished=finished_timestamp)

        if result.result is True:
            self.log.info("Event '{event_type}' for object '{object_id}' "
                          "was handled successfully."
                          .format(event_type=event_type,
                                  object_id=result.related_object))
        else:
            self.log.error("Event handling '{event_type}' "
                           "for object '{object_id}' failed.\n"
                           "Message: {message}"
                           .format(event_type=event_type,
                                   object_id=result.related_object,
                                   message=result.message))
        return result

    def handle_event(self, event_type: str, notification: dict) -> EventResult:
        try:
            result = self.handler.handle(event_name=event_type,
                                         notification=notification)
            return result if result else EventResult(result=False, retry=False)
        except Exception as e:
            self.log.exception(e)
            return EventResult(result=False, retry=False)

    @staticmethod
    def _prepare_message_body(message_body):
        obj = message_body['object']
        return {
            'event_type': message_body['type'],
            'kind': obj.kind,
            'object_id': obj.metadata.uid,
            'object_name': obj.metadata.name,
            'namespace': obj.metadata.namespace,
            'creation_timestamp': obj.metadata.creation_timestamp,
            'resource_version': obj.metadata.resource_version
        }

    def save_message(self, message_body: dict, result: EventResult,
                     started: datetime, finished: datetime):
        try:
            message = Message(
                msg_id=str(uuid.uuid1()),
                env=self.environment,
                source=self.SOURCE_SYSTEM,
                object_id=result.related_object,
                display_context=result.display_context,
                level="info" if result.result is True else "error",
                msg=self._prepare_message_body(message_body),
                received_ts=started,
                finished_ts=finished
            )
            self.inv.collections['messages'].insert_one(message.get())
            return True
        except Exception as e:
            self.inv.log.error("Failed to save message")
            self.inv.log.exception(e)
            return False

    def run(self):
        self.process_vars['operational'] = OperationalStatus.RUNNING
        if not self.endpoints:
            self.log.error("No Watch API endpoints defined. "
                           "Stopping listener")
            self.process_vars['operational'] = OperationalStatus.ERROR
            return

        streams = {}
        for name, endpoint in self.endpoints.items():
            rv = self.resource_versions.get(name, 0)
            stream = self.watch.stream(endpoint,
                                       resource_version=rv,
                                       _request_timeout=self.request_timeout)
            streams[name] = {
                'endpoint': endpoint,
                'watch': self.watch,
                'stream': stream,
                'resource_version': rv,
                'last_event': {}
            }

        while True:
            try:
                events_handled = False

                for name, stream in streams.items():
                    try:
                        event = next(stream['stream'], None)
                    except ReadTimeoutError:
                        stream['stream'] = \
                            self.watch.stream(stream['endpoint'],
                                              resource_version=stream['resource_version'],
                                              _request_timeout=self.request_timeout)
                        continue

                    if event:
                        events_handled = True
                        rv = event['object'].metadata.resource_version

                        # Repeating events workaround
                        event_identity = {
                            'type': event['type'],
                            'resource_version': rv
                        }
                        if event_identity == stream['last_event']:
                            continue
                        stream['last_event'] = event_identity

                        # TODO: research two events having the same rv
                        try:
                            if not rv:
                                self.process_vars['operational'] = OperationalStatus.ERROR
                                raise ResourceGoneError

                            result = self.process_event(event)
                            if result.result is True:
                                rv = int(rv)
                                stream['resource_version'] = rv

                                update_resource_version(inv=self.inv,
                                                        env=self.environment,
                                                        method=name,
                                                        resource_version=rv)

                        except ResourceGoneError:
                            # TODO: perform a rescan?
                            # TODO: Fetch and set resource version from rescan?
                            env_config = self.inv.get_env_config(self.environment)
                            rv = (
                                env_config.get('listener_kwargs', {})
                                          .get('resource_versions', {})
                                          .get(name, stream['resource_version'])
                            )
                            stream['stream'] = \
                                self.watch.stream(stream['endpoint'],
                                                  resource_version=rv,
                                                  _request_timeout=self.request_timeout)
                            continue
                if not events_handled:
                    sleep(self.polling_interval)
            except Exception as e:
                self.log.exception(e)
                self.process_vars['operational'] = OperationalStatus.ERROR
                return

    @staticmethod
    def listen(args: dict = None):
        args = setup_args(args, KubernetesListener.DEFAULTS, get_args)
        if 'process_vars' not in args:
            args['process_vars'] = {}

        env_name = args['env']
        inventory_collection = args["inventory"]

        MongoAccess.set_config_file(args["mongo_config"])
        inv = InventoryMgr()
        inv.set_collections(inventory_collection)
        conf = Configuration(args["environments_collection"])
        conf.use_env(env_name)

        event_handler = EventHandler(env_name, inventory_collection)

        env_config = conf.get_env_config()
        common_metadata_file = os.path.join(
            env_config.get('app_path', '/etc/calipso'),
            'listen/config',
            KubernetesListener.COMMON_METADATA_FILE
        )

        # import common metadata
        metadata_parser = import_metadata(event_handler=event_handler,
                                          metadata_file_path=common_metadata_file)

        # import custom metadata if supplied
        if args["metadata_file"]:
            import_metadata(event_handler, args["metadata_file"])

        kube_config = conf.get('Kubernetes')
        connection_pool_size = len(metadata_parser.endpoints.keys())
        listener = KubernetesListener(config=kube_config,
                                      event_handler=event_handler,
                                      environment=env_name,
                                      inventory_collection=inventory_collection,
                                      connection_pool_size=connection_pool_size,
                                      request_timeout=args['request_timeout'],
                                      polling_inverval=args['polling_interval'],
                                      process_vars=args['process_vars'])
        listener.endpoints = metadata_parser.load_endpoints(api=listener.api)
        listener.resource_versions = args['resource_versions']

        # Suppress mongo and https warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            listener.run()


def get_args():
    # Read listener config from command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mongo_config", nargs="?", type=str,
                        default=KubernetesListener.DEFAULTS["mongo_config"],
                        help="Name of config file with MongoDB access details")
    parser.add_argument("--metadata_file", nargs="?", type=str,
                        default=KubernetesListener.DEFAULTS["metadata_file"],
                        help="Name of custom configuration metadata file")
    def_env_collection = KubernetesListener.DEFAULTS["environments_collection"]
    parser.add_argument("-c", "--environments_collection", nargs="?", type=str,
                        default=def_env_collection,
                        help="Name of collection where selected environment " +
                             "is taken from \n(default: {})"
                        .format(def_env_collection))
    parser.add_argument("-e", "--env", nargs="?", type=str,
                        default=KubernetesListener.DEFAULTS["env"],
                        help="Name of target listener environment \n" +
                             "(default: {})"
                        .format(KubernetesListener.DEFAULTS["env"]))
    parser.add_argument("-y", "--inventory", nargs="?", type=str,
                        default=KubernetesListener.DEFAULTS["inventory"],
                        help="Name of inventory collection \n"" +"
                             "(default: '{}')"
                        .format(KubernetesListener.DEFAULTS["inventory"]))
    parser.add_argument("-t", "--request_timeout", nargs="?", type=int,
                        default=KubernetesListener.DEFAULTS["request_timeout"],
                        help="Watch API request timeout \n(default: {})"
                        .format(KubernetesListener.DEFAULTS["request_timeout"]))
    parser.add_argument("-i", "--polling_interval", nargs="?", type=int,
                        default=KubernetesListener.DEFAULTS["polling_interval"],
                        help="Watch API streams polling interval \n(default: {})"
                        .format(KubernetesListener.DEFAULTS["polling_interval"]))
    parser.add_argument("-l", "--loglevel", nargs="?", type=str,
                        default=KubernetesListener.DEFAULTS["loglevel"],
                        help="Logging level \n(default: '{}')"
                        .format(KubernetesListener.DEFAULTS["loglevel"]))
    args = parser.parse_args()
    return args


# Imports metadata from file,
# updates event handler with new handlers
def import_metadata(event_handler: EventHandler,
                    metadata_file_path: str) -> KubeMetadataParser:
    metadata_parser = parse_metadata_file(metadata_file_path)
    event_handler.discover_handlers(metadata_parser.handlers_package,
                                    metadata_parser.event_handlers)
    return metadata_parser

if __name__ == '__main__':
    KubernetesListener.listen()
