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

import time

import pymongo
from functools import partial

from discover.manager import Manager
from utils.constants import ScanStatus, EnvironmentFeatures
from utils.exceptions import ScanArgumentsError
from utils.inventory_mgr import InventoryMgr
from utils.logging.file_logger import FileLogger
from utils.mongo_access import MongoAccess
from discover.scan import ScanController


class ScanManager(Manager):

    DEFAULTS = {
        "mongo_config": "",
        "scans": "scans",
        "scheduled_scans": "scheduled_scans",
        "environments": "environments_config",
        "interval": 1,
        "loglevel": "INFO"
    }

    def __init__(self):
        self.args = self.get_args()
        super().__init__(log_directory=self.args.log_directory,
                         mongo_config_file=self.args.mongo_config)
        self.db_client = None
        self.environments_collection = None
        self.scans_collection = None
        self.scheduled_scans_collection = None

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--mongo_config", nargs="?", type=str,
                            default=ScanManager.DEFAULTS["mongo_config"],
                            help="Name of config file " +
                                 "with MongoDB server access details")
        parser.add_argument("-c", "--scans_collection", nargs="?", type=str,
                            default=ScanManager.DEFAULTS["scans"],
                            help="Scans collection to read from")
        parser.add_argument("-s", "--scheduled_scans_collection", nargs="?",
                            type=str,
                            default=ScanManager.DEFAULTS["scheduled_scans"],
                            help="Scans collection to read from")
        parser.add_argument("-e", "--environments_collection", nargs="?",
                            type=str,
                            default=ScanManager.DEFAULTS["environments"],
                            help="Environments collection to update "
                                 "after scans")
        parser.add_argument("-i", "--interval", nargs="?", type=float,
                            default=ScanManager.DEFAULTS["interval"],
                            help="Interval between collection polls"
                                 "(must be more than {} seconds)"
                                 .format(ScanManager.MIN_INTERVAL))
        parser.add_argument("-l", "--loglevel", nargs="?", type=str,
                            default=ScanManager.DEFAULTS["loglevel"],
                            help="Logging level \n(default: '{}')"
                                 .format(ScanManager.DEFAULTS["loglevel"]))
        parser.add_argument("-d", "--log_directory", nargs="?", type=str,
                            default=FileLogger.LOG_DIRECTORY,
                            help="File logger directory \n(default: '{}')"
                                 .format(FileLogger.LOG_DIRECTORY))
        args = parser.parse_args()
        return args

    def configure(self):
        self.db_client = MongoAccess()
        self.inv = InventoryMgr()
        self.inv.set_collections()
        self.scans_collection = self.db_client.db[self.args.scans_collection]
        self.scheduled_scans_collection = \
            self.db_client.db[self.args.scheduled_scans_collection]
        self.environments_collection = \
            self.db_client.db[self.args.environments_collection]
        self._update_document = \
            partial(MongoAccess.update_document, self.scans_collection)
        self.interval = max(self.MIN_INTERVAL, self.args.interval)
        self.log.set_loglevel(self.args.loglevel)

        self.log.info("Started ScanManager with following configuration:\n"
                      "Mongo config file path: {0.args.mongo_config}\n"
                      "Scans collection: {0.scans_collection.name}\n"
                      "Environments collection: "
                      "{0.environments_collection.name}\n"
                      "Polling interval: {0.interval} second(s)"
                      .format(self))

    def _build_scan_args(self, scan_request: dict):
        args = {
            'mongo_config': self.args.mongo_config,
            'scheduled': True if scan_request.get('interval') else False
        }

        def set_arg(name_from: str, name_to: str = None):
            if name_to is None:
                name_to = name_from
            val = scan_request.get(name_from)
            if val:
                args[name_to] = val

        set_arg("_id")
        set_arg("object_id", "id")
        set_arg("log_level", "loglevel")
        set_arg("environment", "env")
        set_arg("scan_only_inventory", "inventory_only")
        set_arg("scan_only_links", "links_only")
        set_arg("scan_only_cliques", "cliques_only")
        set_arg("inventory")
        set_arg("clear")
        set_arg("clear_all")

        return args

    def _finalize_scan(self, scan_request: dict, status: ScanStatus,
                       scanned: bool):
        scan_request['status'] = status.value
        self._update_document(scan_request)
        # If no object id is present, it's a full env scan.
        # We need to update environments collection
        # to reflect the scan results.
        if not scan_request.get('id'):
            self.environments_collection\
                .update_one(filter={'name': scan_request.get('environment')},
                            update={'$set': {'scanned': scanned}})

    def _fail_scan(self, scan_request: dict):
        self._finalize_scan(scan_request, ScanStatus.FAILED, False)

    def _complete_scan(self, scan_request: dict, result_message: str):
        status = ScanStatus.COMPLETED if result_message == 'ok' \
            else ScanStatus.COMPLETED_WITH_ERRORS
        self._finalize_scan(scan_request, status, True)

    # PyCharm type checker can't reliably check types of document
    # noinspection PyTypeChecker
    def _clean_up(self):
        # Find and fail all running scans
        running_scans = list(self
                             .scans_collection
                             .find(filter={'status': ScanStatus.RUNNING.value}))
        self.scans_collection \
            .update_many(filter={'_id': {'$in': [scan['_id']
                                                 for scan
                                                 in running_scans]}},
                         update={'$set': {'status': ScanStatus.FAILED.value}})

        # Find all environments connected to failed full env scans
        env_scans = [scan['environment']
                     for scan in running_scans
                     if not scan.get('object_id')
                     and scan.get('environment')]

        # Set 'scanned' flag in those envs to false
        if env_scans:
            self.environments_collection\
                .update_many(filter={'name': {'$in': env_scans}},
                             update={'$set': {'scanned': False}})

    def _submit_scan_request_for_schedule(self, scheduled_scan, interval, ts):
        scans = self.scans_collection
        new_scan = {
            'status': 'submitted',
            'log_level': scheduled_scan['log_level'],
            'clear': scheduled_scan['clear'],
            'scan_only_inventory': scheduled_scan['scan_only_inventory'],
            'scan_only_links': scheduled_scan['scan_only_links'],
            'scan_only_cliques': scheduled_scan['scan_only_cliques'],
            'submit_timestamp': ts,
            'interval': interval,
            'environment': scheduled_scan['environment'],
            'inventory': 'inventory'
        }
        scans.insert_one(new_scan)

    def _set_scheduled_requests_next_run(self, scheduled_scan, interval, ts):
        scheduled_scan['scheduled_timestamp'] = ts + self.INTERVALS[interval]
        doc_id = scheduled_scan.pop('_id')
        self.scheduled_scans_collection.update({'_id': doc_id}, scheduled_scan)

    def _prepare_scheduled_requests_for_interval(self, interval):
        now = datetime.datetime.utcnow()

        # first, submit a scan request where the scheduled time has come
        condition = {'$and': [
            {'freq': interval},
            {'scheduled_timestamp': {'$lte': now}}
        ]}
        matches = self.scheduled_scans_collection.find(condition) \
            .sort('scheduled_timestamp', pymongo.ASCENDING)
        for match in matches:
            self._submit_scan_request_for_schedule(match, interval, now)
            self._set_scheduled_requests_next_run(match, interval, now)

        # now set scheduled time where it was not set yet (new scheduled scans)
        condition = {'$and': [
            {'freq': interval},
            {'scheduled_timestamp': {'$exists': False}}
        ]}
        matches = self.scheduled_scans_collection.find(condition)
        for match in matches:
            self._set_scheduled_requests_next_run(match, interval, now)

    def _prepare_scheduled_requests(self):
        # see if any scheduled request is waiting to be submitted
        for interval in self.INTERVALS.keys():
            self._prepare_scheduled_requests_for_interval(interval)

    def handle_scans(self):
        self._prepare_scheduled_requests()

        # Find a pending request that is waiting the longest time
        results = self.scans_collection \
            .find({'status': ScanStatus.PENDING.value,
                   'submit_timestamp': {'$ne': None}}) \
            .sort("submit_timestamp", pymongo.ASCENDING) \
            .limit(1)

        # If no scans are pending, sleep for some time
        if results.count() == 0:
            time.sleep(self.interval)
        else:
            scan_request = results[0]
            env = scan_request.get('environment')
            scan_feature = EnvironmentFeatures.SCANNING
            if not self.inv.is_feature_supported(env, scan_feature):
                self.log.error("Scanning is not supported for env '{}'"
                               .format(scan_request.get('environment')))
                self._fail_scan(scan_request)
                return

            scan_request['start_timestamp'] = datetime.datetime.utcnow()
            scan_request['status'] = ScanStatus.RUNNING.value
            self._update_document(scan_request)

            # Prepare scan arguments and run the scan with them
            try:
                scan_args = self._build_scan_args(scan_request)

                self.log.info("Starting scan for '{}' environment"
                              .format(scan_args.get('env')))
                self.log.debug("Scan arguments: {}".format(scan_args))
                result, message = ScanController().run(scan_args)
            except ScanArgumentsError as e:
                self.log.error("Scan request '{id}' "
                               "has invalid arguments. "
                               "Errors:\n{errors}"
                               .format(id=scan_request['_id'],
                                       errors=e))
                self._fail_scan(scan_request)
            except Exception as e:
                self.log.exception(e)
                self.log.error("Scan request '{}' has failed."
                               .format(scan_request['_id']))
                self._fail_scan(scan_request)
            else:
                # Check is scan returned success
                if not result:
                    self.log.error(message)
                    self.log.error("Scan request '{}' has failed."
                                   .format(scan_request['_id']))
                    self._fail_scan(scan_request)
                    return

                # update the status and timestamps.
                self.log.info("Request '{}' has been scanned. ({})"
                              .format(scan_request['_id'], message))
                end_time = datetime.datetime.utcnow()
                scan_request['end_timestamp'] = end_time
                self._complete_scan(scan_request, message)

    def do_action(self):
        self._clean_up()
        try:
            while True:
                self.handle_scans()
        finally:
            self._clean_up()


if __name__ == "__main__":
    ScanManager().run()
