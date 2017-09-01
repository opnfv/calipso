###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
# base class for scanners

import json
import os
import queue
import traceback

from discover.clique_finder import CliqueFinder
from discover.configuration import Configuration
from discover.fetcher import Fetcher
from discover.link_finders.find_links_metadata_parser import \
    FindLinksMetadataParser
from discover.scan_error import ScanError
from discover.scan_metadata_parser import ScanMetadataParser
from utils.inventory_mgr import InventoryMgr
from utils.ssh_connection import SshError


class Scanner(Fetcher):
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
        self.link_finders = []
        self.load_scanners_metadata()
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
        except ValueError:
            return False
        except SshError:
            # mark the error
            self.found_errors[self.get_env()] = True
        if limit_to_child_id and len(types_children) > 0:
            t = types_children[0]
            children = t["children"]
            return children[0]
        return obj

    def check_type_env(self, type_to_fetch):
        # check if type is to be run in this environment
        if "environment_condition" not in type_to_fetch:
            return True
        env_cond = type_to_fetch.get("environment_condition", {})
        if not env_cond:
            return True
        if not isinstance(env_cond, dict):
            self.log.warn('illegal environment_condition given '
                          'for type {}'.format(type_to_fetch['type']))
            return True
        conf = self.config.get_env_config()
        for attr, required_val in env_cond.items():
            if attr == "mechanism_drivers":
                if "mechanism_drivers" not in conf:
                    self.log.warn('illegal environment configuration: '
                                  'missing mechanism_drivers')
                    return False
                if not isinstance(required_val, list):
                    required_val = [required_val]
                return bool(set(required_val) & set(conf["mechanism_drivers"]))
            elif attr not in conf or conf[attr] != required_val:
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
        fetcher.set_env(self.get_env())

        # get children_scanner instance
        children_scanner = type_to_fetch.get("children_scanner")

        escaped_id = fetcher.escape(str(obj_id)) if obj_id else obj_id
        self.log.info(
            "scanning : type=%s, parent: (type=%s, name=%s, id=%s)",
            type_to_fetch["type"],
            parent.get('type', 'environment'),
            parent.get('name', ''),
            escaped_id)

        # fetch OpenStack data from environment by CLI, API or MySQL
        # or physical devices data from ACI API
        # It depends on the Fetcher's config.
        try:
            db_results = fetcher.get(escaped_id)
        except SshError:
            self.found_errors[self.get_env()] = True
            return []
        except Exception as e:
            self.log.error("Error while scanning : " +
                           "fetcher=%s, " +
                           "type=%s, " +
                           "parent: (type=%s, name=%s, id=%s), " +
                           "error: %s",
                           fetcher.__class__.__name__,
                           type_to_fetch["type"],
                           "environment" if "type" not in parent
                           else parent["type"],
                           "" if "name" not in parent else parent["name"],
                           escaped_id,
                           e)
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

    def scan_links(self):
        self.log.info("scanning for links")
        for fetcher in self.link_finders:
            fetcher.set_env(self.get_env())
            fetcher.add_links()

    def scan_cliques(self):
        clique_scanner = CliqueFinder()
        clique_scanner.set_env(self.get_env())
        clique_scanner.find_cliques()

    def deploy_monitoring_setup(self):
        ret = self.inv.monitoring_setup_manager.handle_pending_setup_changes()
        if not ret:
            self.found_errors[self.get_env()] = True

    def load_scanners_metadata(self):
        parser = ScanMetadataParser(self.inv)
        conf = self.config.get_env_config()
        scanners_file = os.path.join(conf.get('app_path', '/etc/calipso'),
                                     'config',
                                     ScanMetadataParser.SCANNERS_FILE)

        metadata = parser.parse_metadata_file(scanners_file)
        self.scanners_package = metadata[ScanMetadataParser.SCANNERS_PACKAGE]
        self.scanners = metadata[ScanMetadataParser.SCANNERS]

    def load_link_finders_metadata(self):
        parser = FindLinksMetadataParser()
        conf = self.config.get_env_config()
        finders_file = os.path.join(conf.get('app_path', '/etc/calipso'),
                                    'config',
                                    FindLinksMetadataParser.FINDERS_FILE)
        metadata = parser.parse_metadata_file(finders_file)
        self.link_finders = metadata[FindLinksMetadataParser.LINK_FINDERS]

    def get_scanner_package(self):
        return self.scanners_package

    def get_scanner(self, scanner_type: str) -> dict:
        return self.scanners.get(scanner_type)
