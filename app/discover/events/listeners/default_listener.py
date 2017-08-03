#!/usr/bin/env python3
###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

import argparse
import datetime
import json
import os
import time
from collections import defaultdict
from typing import List

from kombu import Connection, Queue, Exchange
from kombu.mixins import ConsumerMixin

from discover.configuration import Configuration
from discover.event_handler import EventHandler
from discover.events.event_base import EventResult
from discover.events.event_metadata_parser import parse_metadata_file
from discover.events.listeners.listener_base import ListenerBase
from messages.message import Message
from monitoring.setup.monitoring_setup_manager import MonitoringSetupManager
from utils.constants import OperationalStatus, EnvironmentFeatures
from utils.inventory_mgr import InventoryMgr
from utils.logging.full_logger import FullLogger
from utils.mongo_access import MongoAccess
from utils.string_utils import stringify_datetime
from utils.util import SignalHandler, setup_args


class DefaultListener(ListenerBase, ConsumerMixin):

    SOURCE_SYSTEM = "OpenStack"

    COMMON_METADATA_FILE = "events.json"

    DEFAULTS = {
        "env": "Mirantis-Liberty",
        "mongo_config": "",
        "metadata_file": "",
        "inventory": "inventory",
        "loglevel": "INFO",
        "environments_collection": "environments_config",
        "retry_limit": 10,
        "consume_all": False
    }

    def __init__(self, connection: Connection,
                 event_handler: EventHandler,
                 event_queues: List,
                 env_name: str = DEFAULTS["env"],
                 inventory_collection: str = DEFAULTS["inventory"],
                 retry_limit: int = DEFAULTS["retry_limit"],
                 consume_all: bool = DEFAULTS["consume_all"]):
        super().__init__()

        self.connection = connection
        self.retry_limit = retry_limit
        self.env_name = env_name
        self.consume_all = consume_all
        self.handler = event_handler
        self.event_queues = event_queues
        self.failing_messages = defaultdict(int)

        self.inv = InventoryMgr()
        self.inv.set_collections(inventory_collection)
        if self.inv.is_feature_supported(self.env_name, EnvironmentFeatures.MONITORING):
            self.inv.monitoring_setup_manager = \
                MonitoringSetupManager(self.env_name)

    def get_consumers(self, consumer, channel):
        return [consumer(queues=self.event_queues,
                         accept=['json'],
                         callbacks=[self.process_task])]

    # Determines if message should be processed by a handler
    # and extracts message body if yes.
    @staticmethod
    def _extract_event_data(body):
        if "event_type" in body:
            return True, body
        elif "event_type" in body.get("oslo.message", ""):
            return True, json.loads(body["oslo.message"])
        else:
            return False, None

    def process_task(self, body, message):
        received_timestamp = stringify_datetime(datetime.datetime.now())
        processable, event_data = self._extract_event_data(body)
        # If env listener can't process the message
        # or it's not intended for env listener to handle,
        # leave the message in the queue unless "consume_all" flag is set
        if processable and event_data["event_type"] in self.handler.handlers:
            event_result = self.handle_event(event_data["event_type"],
                                             event_data)
            finished_timestamp = stringify_datetime(datetime.datetime.now())
            self.save_message(message_body=event_data,
                              result=event_result,
                              started=received_timestamp,
                              finished=finished_timestamp)

            # Check whether the event was fully handled
            # and, if not, whether it should be retried later
            if event_result.result:
                message.ack()
            elif event_result.retry:
                if 'message_id' not in event_data:
                    message.reject()
                else:
                    # Track message retry count
                    message_id = event_data['message_id']
                    self.failing_messages[message_id] += 1

                    # Retry handling the message
                    if self.failing_messages[message_id] <= self.retry_limit:
                        self.inv.log.info("Retrying handling message " +
                                          "with id '{}'".format(message_id))
                        message.requeue()
                    # Discard the message if it's not accepted
                    # after specified number of trials
                    else:
                        self.inv.log.warn("Discarding message with id '{}' ".
                                          format(message_id) +
                                          "as it's exceeded the retry limit")
                        message.reject()
                        del self.failing_messages[message_id]
            else:
                message.reject()
        elif self.consume_all:
            message.reject()

    # This method passes the event to its handler.
    # Returns a (result, retry) tuple:
    # 'Result' flag is True if handler has finished successfully,
    #                  False otherwise
    # 'Retry' flag specifies if the error is recoverable or not
    # 'Retry' flag is checked only is 'result' is False
    def handle_event(self, event_type: str, notification: dict) -> EventResult:
        print("Got notification.\nEvent_type: {}\nNotification:\n{}".
              format(event_type, notification))
        try:
            result = self.handler.handle(event_name=event_type,
                                         notification=notification)
            return result if result else EventResult(result=False, retry=False)
        except Exception as e:
            self.inv.log.exception(e)
            return EventResult(result=False, retry=False)

    def save_message(self, message_body: dict, result: EventResult,
                     started: str, finished: str):
        try:
            message = Message(
                msg_id=message_body.get('message_id'),
                env=self.env_name,
                source=self.SOURCE_SYSTEM,
                object_id=result.related_object,
                display_context=result.display_context,
                level=message_body.get('priority'),
                msg=message_body,
                ts=message_body.get('timestamp'),
                received_ts=started,
                finished_ts=finished
            )
            self.inv.collections['messages'].insert_one(message.get())
            return True
        except Exception as e:
            self.inv.log.error("Failed to save message")
            self.inv.log.exception(e)
            return False

    @staticmethod
    def listen(args: dict = None):

        args = setup_args(args, DefaultListener.DEFAULTS, get_args)
        if 'process_vars' not in args:
            args['process_vars'] = {}

        env_name = args["env"]
        inventory_collection = args["inventory"]

        MongoAccess.set_config_file(args["mongo_config"])
        inv = InventoryMgr()
        inv.set_collections(inventory_collection)
        conf = Configuration(args["environments_collection"])
        conf.use_env(env_name)

        event_handler = EventHandler(env_name, inventory_collection)
        event_queues = []

        env_config = conf.get_env_config()
        common_metadata_file = os.path.join(env_config.get('app_path', '/etc/calipso'),
                                            'config',
                                            DefaultListener.COMMON_METADATA_FILE)

        # import common metadata
        import_metadata(event_handler, event_queues, common_metadata_file)

        # import custom metadata if supplied
        if args["metadata_file"]:
            import_metadata(event_handler, event_queues, args["metadata_file"])

        logger = FullLogger()
        logger.set_loglevel(args["loglevel"])

        amqp_config = conf.get("AMQP")
        connect_url = 'amqp://{user}:{pwd}@{host}:{port}//' \
            .format(user=amqp_config["user"],
                    pwd=amqp_config["pwd"],
                    host=amqp_config["host"],
                    port=amqp_config["port"])

        with Connection(connect_url) as conn:
            try:
                print(conn)
                conn.connect()
                args['process_vars']['operational'] = OperationalStatus.RUNNING
                terminator = SignalHandler()
                worker = \
                    DefaultListener(connection=conn,
                                    event_handler=event_handler,
                                    event_queues=event_queues,
                                    retry_limit=args["retry_limit"],
                                    consume_all=args["consume_all"],
                                    inventory_collection=inventory_collection,
                                    env_name=env_name)
                worker.run()
                if terminator.terminated:
                    args.get('process_vars', {})['operational'] = \
                        OperationalStatus.STOPPED
            except KeyboardInterrupt:
                print('Stopped')
                args['process_vars']['operational'] = OperationalStatus.STOPPED
            except Exception as e:
                logger.log.exception(e)
                args['process_vars']['operational'] = OperationalStatus.ERROR
            finally:
                # This should enable safe saving of shared variables
                time.sleep(0.1)


def get_args():
    # Read listener config from command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mongo_config", nargs="?", type=str,
                        default=DefaultListener.DEFAULTS["mongo_config"],
                        help="Name of config file with MongoDB access details")
    parser.add_argument("--metadata_file", nargs="?", type=str,
                        default=DefaultListener.DEFAULTS["metadata_file"],
                        help="Name of custom configuration metadata file")
    def_env_collection = DefaultListener.DEFAULTS["environments_collection"]
    parser.add_argument("-c", "--environments_collection", nargs="?", type=str,
                        default=def_env_collection,
                        help="Name of collection where selected environment " +
                             "is taken from \n(default: {})"
                        .format(def_env_collection))
    parser.add_argument("-e", "--env", nargs="?", type=str,
                        default=DefaultListener.DEFAULTS["env"],
                        help="Name of target listener environment \n" +
                             "(default: {})"
                        .format(DefaultListener.DEFAULTS["env"]))
    parser.add_argument("-y", "--inventory", nargs="?", type=str,
                        default=DefaultListener.DEFAULTS["inventory"],
                        help="Name of inventory collection \n"" +"
                             "(default: '{}')"
                        .format(DefaultListener.DEFAULTS["inventory"]))
    parser.add_argument("-l", "--loglevel", nargs="?", type=str,
                        default=DefaultListener.DEFAULTS["loglevel"],
                        help="Logging level \n(default: '{}')"
                        .format(DefaultListener.DEFAULTS["loglevel"]))
    parser.add_argument("-r", "--retry_limit", nargs="?", type=int,
                        default=DefaultListener.DEFAULTS["retry_limit"],
                        help="Maximum number of times the OpenStack message "
                             "should be requeued before being discarded \n" +
                             "(default: {})"
                        .format(DefaultListener.DEFAULTS["retry_limit"]))
    parser.add_argument("--consume_all", action="store_true",
                        help="If this flag is set, " +
                             "environment listener will try to consume"
                             "all messages from OpenStack event queue "
                             "and reject incompatible messages."
                             "Otherwise they'll just be ignored.",
                        default=DefaultListener.DEFAULTS["consume_all"])
    args = parser.parse_args()
    return args


# Imports metadata from file,
# updates event handler with new handlers
# and event queues with new queues
def import_metadata(event_handler: EventHandler,
                    event_queues: List[Queue],
                    metadata_file_path: str) -> None:
    handlers_package, queues, event_handlers = \
        parse_metadata_file(metadata_file_path)
    event_handler.discover_handlers(handlers_package, event_handlers)
    event_queues.extend([
        Queue(q['queue'],
              Exchange(q['exchange'], 'topic', durable=False),
              durable=False, routing_key='#') for q in queues
    ])


if __name__ == '__main__':
    DefaultListener.listen()
