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
import signal
import time
from datetime import timedelta, datetime
from multiprocessing import Process, Manager as SharedManager
from typing import Iterable

import os

from base.utils.constants import OperationalStatus, EnvironmentFeatures
from base.utils.inventory_mgr import InventoryMgr
from base.utils.logging.file_logger import FileLogger
from base.utils.logging.full_logger import FullLogger
from base.utils.logging.logger import Logger
from base.utils.logging.message_logger import MessageLogger
from base.utils.mongo_access import MongoAccess
from listen.events.listeners.default_listener import DefaultListener
from listen.events.listeners.kubernetes_listener import KubernetesListener
from listen.events.listeners.listener_base import ListenerBase
from scan.manager import Manager


class ProcessMonitor:
    MIN_RETRY_DELAY_LIMIT = 10
    RETRY_DELAY_LIMIT = 600  # Maximum backoff time between restarts
    BASE_DELAY = 10

    def __init__(self, process: Process, environment: str, logger: Logger,
                 variables):
        self.process = process
        self.environment = environment
        self.logger = logger
        self.variables = variables
        self.is_on_backoff = False  # Is listener crashing and suspended?
        self.crash_count = 0  # How many times listener has crashed consecutively
        self.next_retry_time = None  # Earliest time the listener can be restarted again

    # Provides the most accurate operational status for the process
    @property
    def operational(self):
        try:
            operational = self.variables.get('operational')
        except:
            self.logger.error(
                "Event listener '{0}' is unreachable".format(self.environment)
            )
            return OperationalStatus.STOPPED

        if operational:
            return operational
        if self.is_alive:
            return OperationalStatus.RUNNING
        if self.process.exitcode == 0:
            return OperationalStatus.STOPPED

        return OperationalStatus.ERROR

    @property
    def ready_to_start(self):
        return not self.is_on_backoff

    @property
    def is_alive(self):
        return self.process.is_alive()

    # Listener health check and restart scheduler
    def update_backoff(self):
        # Listener has recovered
        if self.operational != OperationalStatus.ERROR:
            self.is_on_backoff = False
            self.crash_count = 0
            return

        # Listener has been suspended for the designated time
        # and is ready to be restarted again
        if self.is_on_backoff and self.next_retry_time < datetime.now():
            self.is_on_backoff = False
            return

        # Listener has crashed and should be suspended for some time
        # before it is restarted again.
        if not self.is_on_backoff:
            self.is_on_backoff = True
            self.crash_count += 1
            retry_delay = int(min(self.crash_count * self.BASE_DELAY,
                                  self.RETRY_DELAY_LIMIT))
            self.next_retry_time = datetime.now() + timedelta(seconds=retry_delay)

    def start(self):
        return self.process.start()

    def terminate(self):
        return self.process.terminate()


class EventManager(Manager):

    # After EventManager receives a SIGTERM,
    # it will try to terminate all listeners.
    # After this delay, a SIGKILL will be sent
    # to each listener that is still alive.
    SIGKILL_DELAY = 5  # in seconds

    DEFAULTS = {
        "mongo_config": "",
        "collection": "environments_config",
        "inventory": "inventory",
        "interval": 5,
        "loglevel": "INFO"
    }

    LISTENERS = {
        'ANY': DefaultListener,
        'Kubernetes': {
            'ANY': KubernetesListener
        }
    }

    def __init__(self):
        self.args = self.get_args()
        super().__init__(log_directory=self.args.log_directory,
                         mongo_config_file=self.args.mongo_config)
        self.db_client = None
        self.interval = None
        self.processes = {}

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--mongo_config", nargs="?", type=str,
                            default=EventManager.DEFAULTS["mongo_config"],
                            help="Name of config file with MongoDB server access details")
        parser.add_argument("-c", "--collection", nargs="?", type=str,
                            default=EventManager.DEFAULTS["collection"],
                            help="Environments collection to read from "
                                 "(default: '{}')"
                                 .format(EventManager.DEFAULTS["collection"]))
        parser.add_argument("-y", "--inventory", nargs="?", type=str,
                            default=EventManager.DEFAULTS["inventory"],
                            help="name of inventory collection "
                                 "(default: '{}')"
                                 .format(EventManager.DEFAULTS["inventory"]))
        parser.add_argument("-i", "--interval", nargs="?", type=float,
                            default=EventManager.DEFAULTS["interval"],
                            help="Interval between collection polls "
                                 "(must be more than {} seconds. Default: {})"
                                 .format(EventManager.MIN_INTERVAL,
                                         EventManager.DEFAULTS["interval"]))
        parser.add_argument("-B", "--base_delay", nargs="?", type=int,
                            default=ProcessMonitor.RETRY_DELAY_LIMIT,
                            help="Base delay between restarts "
                                 "of a failing event listener "
                                 "(must be more than {} seconds. Default: {})"
                                 .format(1, ProcessMonitor.BASE_DELAY))
        parser.add_argument("-D", "--max_delay", nargs="?", type=int,
                            default=ProcessMonitor.RETRY_DELAY_LIMIT,
                            help="Maximum delay between restarts "
                                 "of a failing event listener "
                                 "(must be more than {} seconds. Default: {})"
                                 .format(ProcessMonitor.MIN_RETRY_DELAY_LIMIT,
                                         ProcessMonitor.RETRY_DELAY_LIMIT))
        parser.add_argument("-l", "--loglevel", nargs="?", type=str,
                            default=EventManager.DEFAULTS["loglevel"],
                            help="Logging level \n(default: '{}')"
                                 .format(EventManager.DEFAULTS["loglevel"]))
        parser.add_argument("-d", "--log_directory", nargs="?", type=str,
                            default=FileLogger.LOG_DIRECTORY,
                            help="File logger directory \n(default: '{}')"
                                 .format(FileLogger.LOG_DIRECTORY))
        args = parser.parse_args()
        return args

    def configure(self):
        self.db_client = MongoAccess()
        self.inv = InventoryMgr()
        self.inv.set_collections(self.args.inventory)
        self.collection = self.db_client.db[self.args.collection]
        self.interval = max(self.MIN_INTERVAL, self.args.interval)
        ProcessMonitor.BASE_DELAY = max(1, self.args.base_delay)
        ProcessMonitor.RETRY_DELAY_LIMIT = max(ProcessMonitor.MIN_RETRY_DELAY_LIMIT,
                                               self.args.max_delay)
        self.log.set_loglevel(self.args.loglevel)

        self.log.info("Started EventManager with following configuration:\n"
                      "{1}\n"
                      "Collection: {0.collection.name}\n"
                      "Polling interval: {0.interval} second(s)"
                      .format(self, MongoAccess.get_source_text()))

    def get_listener(self, env: str):
        env_config = self.inv.get_env_config(env)
        versions = self.LISTENERS.get(env_config.get('distribution'))
        if versions:
            if isinstance(versions, dict):
                return versions.get(env_config.get('distribution_version'),
                                    versions.get('ANY', DefaultListener))
            else:
                return versions

        return self.LISTENERS.get('ANY', DefaultListener)

    def listen_to_events(self, listener: ListenerBase, env_name: str,
                               process_vars: dict, **kwargs):
        kwargs.update({
            'env': env_name,
            'mongo_config': self.args.mongo_config,
            'inventory': self.args.inventory,
            'loglevel': self.args.loglevel,
            'environments_collection': self.args.collection,
            'process_vars': process_vars
        })
        logger = MessageLogger(env=env_name, level=self.args.loglevel)
        try:
            listener.listen(kwargs)
        except Exception as e:
            logger.error(e)
            raise

    def _get_alive_processes(self) -> dict:
        return {env: p for env, p in self.processes.items() if p.is_alive}

    # Get all processes that should be terminated
    def _get_stuck_processes(self, stopped_processes: Iterable) -> dict:
        return {env: p for env, p in self._get_alive_processes().items()
                if p.environment in stopped_processes}

    # Give processes time to finish and kill them if they are stuck
    def _kill_stuck_processes(self, process_list: Iterable):
        if self._get_stuck_processes(process_list):
            time.sleep(self.SIGKILL_DELAY)
        for env, process in self._get_stuck_processes(process_list).items():
            process.logger.info("Killing event listener '{0}'".format(env))
            os.kill(process.get("process").pid, signal.SIGKILL)

    def _update_operational_status(self, status: OperationalStatus):
        self.collection.update_many(
            {"name": {"$in": [env
                              for env, process
                              in self.processes.items()
                              if process.operational == status]}},
            {"$set": {"operational": status.value}}
        )

    def update_operational_statuses(self):
        self._update_operational_status(OperationalStatus.RUNNING)
        self._update_operational_status(OperationalStatus.ERROR)
        self._update_operational_status(OperationalStatus.STOPPED)

    def stop_processes(self):
        # Query for envs that are no longer eligible for listening
        # (scanned == false and/or listen == false)
        dropped_envs = [env['name']
                        for env
                        in self.collection
                               .find(filter={'$or': [{'scanned': False},
                                                     {'listen': False}]},
                                     projection=['name'])]

        stopped_processes = {}
        # Drop already terminated processes
        # and for all others perform filtering
        for env, process in self._get_alive_processes().items():
            # If env no longer qualifies for listening, stop the listener
            if env in dropped_envs:
                process.logger.info("Stopping event listener '{0}'".format(env))
                process.terminate()
                stopped_processes[env] = process

        self._kill_stuck_processes(stopped_processes.keys())

        # Update all 'operational' statuses
        # for processes stopped on the previous step
        self._update_operational_status(OperationalStatus.STOPPED)

    def filter_out_working_listeners(self, environments) -> Iterable:
        return (
            env
            for env in environments
            if env not in self._get_alive_processes()
        )

    # Filter out the listeners that are consistently crashing on startup
    def filter_out_failing_listeners(self, environments) -> Iterable:
        remaining_environments = []
        for env in environments:
            process = self.processes.get(env)
            # If the listener hasn't been set up yet, skip this filter
            if not process:
                remaining_environments.append(env)
                continue

            # Update current backoff state for the listener
            process.update_backoff()
            if process.ready_to_start:
                remaining_environments.append(env)
                continue

        return remaining_environments

    def get_environments_to_listen(self) -> Iterable:
        environments = [
            env['name']
            for env
            in self.collection.find({'scanned': True, 'listen': True})
        ]
        environments = self.filter_out_failing_listeners(environments)
        return self.filter_out_working_listeners(environments)

    def do_action(self):
        try:
            while True:
                # Update "operational" field in initial_data before removing dead processes
                # so that we keep last statuses of env listeners before they were terminated
                self.update_operational_statuses()

                # Stop processes that should no longer be listening
                self.stop_processes()

                environments = self.get_environments_to_listen()

                # Iterate over environments that don't have an event listener attached
                for env_name in environments:
                    logger = FullLogger(env=env_name, level=self.args.loglevel)

                    if not self.inv.is_feature_supported(env_name, EnvironmentFeatures.LISTENING):
                        logger.error("Listening is not supported for env '{}'".format(env_name))
                        self.collection.update({"name": env_name},
                                               {"$set": {"operational": OperationalStatus.ERROR.value}})
                        continue

                    listener = self.get_listener(env_name)

                    # A dict that is shared between event manager and newly created env listener
                    process_vars = SharedManager().dict()
                    env_config = self.inv.get_env_config(env=env_name)
                    p = Process(target=self.listen_to_events,
                                args=(listener, env_name, process_vars),
                                kwargs=env_config.get('listener_kwargs', {}),
                                name=env_name)

                    if env_name not in self.processes:
                        self.processes[env_name] = ProcessMonitor(process=p,
                                                                  environment=env_name,
                                                                  logger=logger,
                                                                  variables=process_vars)
                    else:
                        self.processes[env_name].process = p

                    logger.info("Starting event listener '{0}'".format(env_name))
                    self.processes[env_name].start()

                # Make sure statuses are up-to-date before event manager goes to sleep
                self.update_operational_statuses()
                time.sleep(self.interval)
        finally:
            # Fetch operational statuses before terminating listeners.
            # Shared variables won't be available after termination.
            stopping_processes = [env
                                  for env, process
                                  in self.processes.items()
                                  if process.operational != OperationalStatus.ERROR]
            self._update_operational_status(OperationalStatus.ERROR)

            # Gracefully stop processes
            for env, process in self._get_alive_processes().items():
                process.logger.info("Stopping event listener '{0}'".format(env))
                process.terminate()

            # Kill all remaining processes
            self._kill_stuck_processes(self.processes)

            # Updating operational statuses for stopped processes
            self.collection.update_many(
                {"name": {"$in": stopping_processes}},
                {"$set": {"operational": OperationalStatus.STOPPED.value}}
            )

if __name__ == "__main__":
    EventManager().run()
