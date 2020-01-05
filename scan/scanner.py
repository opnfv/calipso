###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
# base class for scanners

import json
import queue
import traceback

import os

from base.fetcher import Fetcher
from base.utils.configuration import Configuration
from base.utils.exceptions import CredentialsError, HostAddressError
from base.utils.inventory_mgr import InventoryMgr
from base.utils.ssh_connection import SshError
from scan.clique_finder import CliqueFinder
from scan.link_finders.find_links_metadata_parser import FindLinksMetadataParser
from scan.processors.processors_metadata_parser import ProcessorsMetadataParser
from scan.scan_error import ScanError
from scan.scan_metadata_parser import ScanMetadataParser


class Scanner(Fetcher):

    metadata_files_path = "scan/config"

    config = None
    environment = None
    env = None
    root_patern = None
    scan_queue = queue.Queue()
    scan_queue_track = {}

    # keep errors indication per environment
    found_errors = {}

    def __init__(self):
        """
        Scanner is the base class for scanners.
        """
        super().__init__()
        self.config = Configuration()
        self.inv = InventoryMgr()
        self.scanners_package = None
        self.scanners = {}
        self.processors = []
        self.link_finders = []
        self.load_scanners_metadata()
        self.load_processors_metadata()
        self.load_link_finders_metadata()

    def scan(self, scanner_type, obj, id_field="id",
             limit_to_child_id=None, limit_to_child_type=None):
        types_to_fetch = self.get_scanner(scanner_type)
        types_children = []
        if not limit_to_child_type:
            limit_to_child_type = []
        elif isinstance(limit_to_child_type, str):
            limit_to_child_type = [limit_to_child_type]
        try:
            for t in types_to_fetch:
                if limit_to_child_type and t["type"] not in limit_to_child_type:
                    continue
                children = self.scan_type(t, obj, id_field)
                if limit_to_child_id:
                    children = [c for c in children
                                if c[id_field] == limit_to_child_id]
                    if not children:
                        continue
                types_children.append({"type": t["type"],
                                      "children": children})
        except (SshError, CredentialsError, HostAddressError):
            # mark the error
            self.found_errors[self.get_env()] = True
        except ValueError as e:
            raise ScanError(e)
        if limit_to_child_id and len(types_children) > 0:
            t = types_children[0]
            children = t["children"]
            return children[0]
        return obj

    @staticmethod
    def _match_condition_values(values, condition):
        if not values:
            return False
        elif not condition:
            return True
        else:
            condition_list = condition if isinstance(condition, list) else [condition]
            conf_list = values if isinstance(values, list) else [values]
            for item in conf_list:
                if item in condition_list:
                    return True
        return False

    @classmethod
    def _match_conditions(cls, conf, condition):
        for attr, required_val in condition.items():
            if cls._match_condition_values(conf[attr], required_val) is False:
                return False
        return True

    @staticmethod
    def _match_restriction_values(values, restriction):
        if not values:
            return False
        if not restriction:
            return False
        else:
            restriction_list = restriction if isinstance(restriction, list) else [restriction]
            conf_list = values if isinstance(values, list) else [values]
            for item in restriction_list:
                if item in conf_list:
                    return True
        return False

    @classmethod
    def _match_restrictions(cls, conf, restriction):
        for attr, restricted_val in restriction.items():
            if cls._match_restriction_values(conf[attr], restricted_val) is False:
                return False
        return True

    def check_type_env(self, type_to_fetch):
        # check if type is to be run in this environment
        basic_cond = {'environment_type': self.ENV_TYPE_OPENSTACK}

        env_conditions = type_to_fetch.get("environment_condition")
        if env_conditions is None:
            env_conditions = [basic_cond]
        elif isinstance(env_conditions, dict):
            env_conditions = [env_conditions]
        elif not isinstance(env_conditions, list) \
                or not all(isinstance(c, dict) for c in env_conditions):
            self.log.warn('Illegal environment_condition given '
                          'for type {type}'.format(type=type_to_fetch['type']))
            return True

        for env_condition in env_conditions:
            if 'environment_type' not in env_condition:
                env_condition.update(basic_cond)

        conf = self.config.get_env_config()
        if 'environment_type' not in conf:
            conf.update(basic_cond)

        # If any condition dict matches configuration, we're good.
        if env_conditions:
            if all(self._match_conditions(conf, condition) is False
                   for condition in env_conditions):
                return False

        env_restrictions = type_to_fetch.get("environment_restriction")
        if env_restrictions is not None:
            if isinstance(env_restrictions, dict):
                env_restrictions = [env_restrictions]
            elif not isinstance(env_restrictions, list) \
                    or not all(isinstance(r, dict) for r in env_restrictions):
                self.log.warn('Illegal environment_restriction given '
                              'for type {type}'.format(type=type_to_fetch['type']))
                return True

            # If any restriction dict matches configuration, scanner is discarded
            if env_restrictions:
                if any(self._match_restrictions(conf, restriction) is True
                       for restriction in env_restrictions):
                    return False

        # no check failed
        return True

    def scan_type(self, type_to_fetch, parent, id_field):
        # check if type is to be run in this environment
        if not self.check_type_env(type_to_fetch):
            return []

        if not parent:
            obj_id = None
        else:
            obj_id = str(parent[id_field])
            if not obj_id or not obj_id.rstrip():
                raise ValueError("Object missing " + id_field + " attribute")

        # get Fetcher instance
        fetcher = type_to_fetch["fetcher"]
        if not isinstance(fetcher, Fetcher):
            type_to_fetch['fetcher'] = fetcher()  # make it an instance
            fetcher = type_to_fetch["fetcher"]
        fetcher.setup(env=self.get_env(), origin=self.origin)

        # get children_scanner instance
        children_scanner = type_to_fetch.get("children_scanner")

        escaped_id = fetcher.escape(str(obj_id)) if obj_id else obj_id
        self.log.info(
            "Scanning: "
            "fetcher={fetcher}, "
            "type={type}, "
            "parent: (type={parent_type}, "
            "name={parent_name}, "
            "id={parent_id})".format(fetcher=fetcher.__class__.__name__,
                                     type=type_to_fetch["type"],
                                     parent_type=parent.get('type', 'environment'),
                                     parent_name=parent.get('name', ''),
                                     parent_id=escaped_id))

        # fetch OpenStack data from environment by CLI, API or MySQL
        # or physical devices data from ACI API
        # It depends on the Fetcher's config.
        try:
            db_results = fetcher.get(escaped_id)
        except (SshError, CredentialsError, HostAddressError):
            self.found_errors[self.get_env()] = True
            return []
        except Exception as e:
            self.log.error(
                "Error while scanning: fetcher={fetcher}, type={type}, "
                "parent: (type={parent_type}, name={parent_name}, "
                "id={parent_id}), "
                "error: {error}".format(fetcher=fetcher.__class__.__name__,
                                        type=type_to_fetch["type"],
                                        parent_type="environment"
                                                    if "type" not in parent
                                                    else parent["type"],
                                        parent_name=""
                                                    if "name" not in parent
                                                    else parent["name"],
                                        parent_id=escaped_id,
                                        error=e))

            traceback.print_exc()
            raise ScanError(str(e))

        # format results
        if isinstance(db_results, dict):
            results = db_results["rows"] if db_results["rows"] else [db_results]
        elif isinstance(db_results, str):
            results = json.loads(db_results)
        else:
            results = db_results

        # get child_id_field
        try:
            child_id_field = type_to_fetch["object_id_to_use_in_child"]
        except KeyError:
            child_id_field = "id"

        environment = self.get_env()
        children = []

        for o in results:
            if not isinstance(o, dict):
                self.found_errors[self.get_env()] = True
                continue
            saved = self.inv.save_inventory_object(o,
                                                   parent=parent,
                                                   environment=environment,
                                                   type_to_fetch=type_to_fetch)

            if saved:
                # add objects into children list.
                children.append(o)

                # put children scanner into queue
                if children_scanner:
                    self.queue_for_scan(o, child_id_field, children_scanner)
        return children

    # scanning queued items, rather than going depth-first (DFS)
    # this is done to allow collecting all required data for objects
    # before continuing to next level
    # for example, get host ID from API os-hypervisors call, so later
    # we can use this ID in the "os-hypervisors/<ID>/servers" call
    @staticmethod
    def queue_for_scan(o, child_id_field, children_scanner):
        if o["id"] in Scanner.scan_queue_track:
            return
        Scanner.scan_queue_track[o["type"] + ";" + o["id"]] = 1
        Scanner.scan_queue.put({"object": o,
                                "child_id_field": child_id_field,
                                "scanner": children_scanner})

    def run_scan(self, scanner_type, obj, id_field, child_id, child_type):
        results = self.scan(scanner_type, obj, id_field, child_id, child_type)

        # run children scanner from queue.
        self.scan_from_queue()
        return results

    def scan_from_queue(self):
        while not Scanner.scan_queue.empty():
            item = Scanner.scan_queue.get()
            scanner_type = item["scanner"]

            # scan the queued item
            self.scan(scanner_type, item["object"], item["child_id_field"])
        self.log.info("Scan complete")

    def run_processors(self):
        self.log.info("Running post-scan processors")
        for processor in self.processors:
            processor.setup(env=self.get_env(), origin=self.origin)
            processor.run()

    def scan_links(self):
        self.log.info("Scanning for links")
        for fetcher in self.link_finders:
            fetcher.setup(env=self.get_env(), origin=self.origin)
            fetcher.add_links()

    def scan_cliques(self):
        clique_scanner = CliqueFinder()
        clique_scanner.setup(env=self.get_env(), origin=self.origin)
        clique_scanner.find_cliques()

    def deploy_monitoring_setup(self):
        ret = self.inv.monitoring_setup_manager.handle_pending_setup_changes()
        if not ret:
            self.found_errors[self.get_env()] = True

    def get_run_app_path(self):
        conf = self.config.get_env_config()
        run_app_path = conf.get('run_app_path', '')
        if not run_app_path:
            run_app_path = conf.get('app_path', '/etc/calipso')
        return run_app_path

    def load_scanners_metadata(self):
        parser = ScanMetadataParser(self.inv)
        scanners_file = os.path.join(self.get_run_app_path(),
                                     self.metadata_files_path,
                                     ScanMetadataParser.SCANNERS_FILE)

        metadata = parser.parse_metadata_file(scanners_file)
        self.scanners_package = metadata[ScanMetadataParser.SCANNERS_PACKAGE]
        self.scanners = metadata[ScanMetadataParser.SCANNERS]

    def load_processors_metadata(self):
        parser = ProcessorsMetadataParser()
        processors_file = os.path.join(self.get_run_app_path(),
                                       self.metadata_files_path,
                                       ProcessorsMetadataParser.PROCESSORS_FILE)
        metadata = parser.parse_metadata_file(processors_file)
        self.processors = metadata[ProcessorsMetadataParser.PROCESSORS]

    def load_link_finders_metadata(self):
        parser = FindLinksMetadataParser()
        finders_file = os.path.join(self.get_run_app_path(),
                                    self.metadata_files_path,
                                    FindLinksMetadataParser.FINDERS_FILE)
        metadata = parser.parse_metadata_file(finders_file)
        self.link_finders = metadata[FindLinksMetadataParser.LINK_FINDERS]

    def get_scanner_package(self):
        return self.scanners_package

    def get_scanner(self, scanner_type: str) -> dict:
        return self.scanners.get(scanner_type)
