#!/usr/bin/env python3
###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

# Scan an object and insert/update in the inventory

# phase 2: either scan default environment, or scan specific object

import argparse
import sys

from base.fetcher import Fetcher
from base.utils.configuration import Configuration
from base.utils.constants import EnvironmentFeatures
from base.utils.exceptions import ScanArgumentsError
from base.utils.inventory_mgr import InventoryMgr
from base.utils.mongo_access import MongoAccess
from base.utils.origins import ScanOrigins, ScanOrigin
from base.utils.ssh_connection import SshConnection
from base.utils.util import setup_args
from monitoring.setup.monitoring_setup_manager import MonitoringSetupManager
from scan.fetchers.aci.aci_access import AciAccess
from scan.fetchers.api.api_access import ApiAccess
from scan.fetchers.db.db_access import DbAccess
from scan.scan_error import ScanError
from scan.scanner import Scanner
from scan.validators import validators


class ScanPlan:
    """
    @DynamicAttrs
    """

    # Each tuple of COMMON_ATTRIBUTES consists of:
    # attr_name, arg_name and def_key
    #
    # attr_name - name of class attribute to be set
    # arg_name - corresponding name of argument (equal to attr_name if not set)
    # def_key - corresponding key in DEFAULTS (equal to attr_name if not set)
    COMMON_ATTRIBUTES = (("loglevel",),
                         ("inventory_only",),
                         ("processors_only",),
                         ("links_only",),
                         ("cliques_only",),
                         ("monitoring_setup_only",),
                         ("clear",),
                         ("clear_all",),
                         ("object_type", "type", "type"),
                         ("env",),
                         ("object_id", "id", "env"),
                         ("parent_id",),
                         ("type_to_scan", "parent_type", "parent_type"),
                         ("id_field",),
                         ("scan_self",),
                         ("child_type", "type", "type"))

    def __init__(self, args=None):
        self.obj = None
        self.scanner_type = None
        self.args = args
        for attribute in self.COMMON_ATTRIBUTES:
            setattr(self, attribute[0], None)

        if isinstance(args, dict):
            self._init_from_dict()
        else:
            self._init_from_args()
        self._validate_args()

    def _validate_args(self):
        errors = []
        if sum((self.inventory_only, self.processors_only, self.links_only, self.cliques_only)) > 1:
            errors.append("Only one of (inventory_only, processors_only, links_only, cliques_only) can be True.")
        if errors:
            raise ScanArgumentsError("\n".join(errors))

    def _set_arg_from_dict(self, attribute_name, arg_name=None,
                           default_key=None):
        default_attr = default_key if default_key else attribute_name
        setattr(self, attribute_name,
                self.args.get(arg_name if arg_name else attribute_name,
                              ScanController.DEFAULTS[default_attr]))

    def _set_arg_from_cmd(self, attribute_name, arg_name=None):
        setattr(self,
                attribute_name,
                getattr(self.args, arg_name if arg_name else attribute_name))

    def _set_arg_from_form(self, attribute_name, arg_name=None,
                           default_key=None):
        default_attr = default_key if default_key else attribute_name
        setattr(self,
                attribute_name,
                self.args.getvalue(arg_name if arg_name else attribute_name,
                                   ScanController.DEFAULTS[default_attr]))

    def _init_from_dict(self):
        for arg in self.COMMON_ATTRIBUTES:
            self._set_arg_from_dict(*arg)
        self.child_id = None

    def _init_from_args(self):
        for arg in self.COMMON_ATTRIBUTES:
            self._set_arg_from_cmd(*arg[:2])
        self.child_id = None


class ScanController(Fetcher):
    DEFAULTS = {
        "_id": None,
        "env": "",
        "mongo_config": "",
        "type": "",
        "inventory": "inventory",
        "scan_self": False,
        "parent_id": "",
        "parent_type": "",
        "id_field": "id",
        "loglevel": "INFO",
        "inventory_only": False,
        "processors_only": False,
        "links_only": False,
        "cliques_only": False,
        "monitoring_setup_only": False,
        "clear": False,
        "clear_all": False,
        "origin": ScanOrigin(origin_type=ScanOrigins.MANUAL),
        "logger": None
    }

    def __init__(self):
        super().__init__()
        self.conf = None
        self.inv = None

    def get_args(self):
        # try to read scan plan from command line parameters
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--mongo_config", nargs="?", type=str,
                            default=self.DEFAULTS["mongo_config"],
                            help="name of config file " +
                                 "with MongoDB server access details")
        parser.add_argument("-e", "--env", nargs="?", type=str,
                            default=self.DEFAULTS["env"],
                            help="name of environment to scan \n"
                                 "(default: " + self.DEFAULTS["env"] + ")")
        parser.add_argument("-t", "--type", nargs="?", type=str,
                            default=self.DEFAULTS["type"],
                            help="type of object to scan \n"
                                 "(default: environment)")
        parser.add_argument("-y", "--inventory", nargs="?", type=str,
                            default=self.DEFAULTS["inventory"],
                            help="name of inventory collection \n"
                                 "(default: 'inventory')")
        parser.add_argument("-s", "--scan_self", action="store_true",
                            help="scan changes to a specific object \n"
                                 "(default: False)")
        parser.add_argument("-i", "--id", nargs="?", type=str,
                            default=self.DEFAULTS["env"],
                            help="ID of object to scan (when scan_self=true)")
        parser.add_argument("-p", "--parent_id", nargs="?", type=str,
                            default=self.DEFAULTS["parent_id"],
                            help="ID of parent object (when scan_self=true)")
        parser.add_argument("-a", "--parent_type", nargs="?", type=str,
                            default=self.DEFAULTS["parent_type"],
                            help="type of parent object (when scan_self=true)")
        parser.add_argument("-f", "--id_field", nargs="?", type=str,
                            default=self.DEFAULTS["id_field"],
                            help="name of ID field (when scan_self=true) \n"
                                 "(default: 'id', use 'name' for projects)")
        parser.add_argument("-l", "--loglevel", nargs="?", type=str,
                            default=self.DEFAULTS["loglevel"],
                            help="logging level \n(default: '{}')"
                                 .format(self.DEFAULTS["loglevel"]))
        parser.add_argument("--clear", action="store_true",
                            help="clear all data related to "
                                 "the specified environment prior to scanning\n"
                                 "(default: False)")
        parser.add_argument("--clear_all", action="store_true",
                            help="clear all data prior to scanning\n"
                                 "(default: False)")
        parser.add_argument("--monitoring_setup_only", action="store_true",
                            help="do only monitoring setup deployment \n"
                                 "(default: False)")

        # At most one of these arguments may be present
        scan_only_group = parser.add_mutually_exclusive_group()
        scan_only_group.add_argument("--inventory_only", action="store_true",
                                     help="do only scan to inventory\n" +
                                          "(default: False)")
        scan_only_group.add_argument("--processors_only", action="store_true",
                                     help="do only post-scan processors \n" +
                                          "(default: False)")
        scan_only_group.add_argument("--links_only", action="store_true",
                                     help="do only links creation \n" +
                                          "(default: False)")
        scan_only_group.add_argument("--cliques_only", action="store_true",
                                     help="do only cliques creation \n" +
                                          "(default: False)")

        return parser.parse_args()

    def get_scan_plan(self, args):
        # PyCharm type checker can't reliably check types of document
        # noinspection PyTypeChecker
        return self.prepare_scan_plan(ScanPlan(args))

    def prepare_scan_plan(self, plan):
        # Find out object type if not specified in arguments
        if not plan.object_type:
            if not plan.object_id:
                plan.object_type = "environment"
            else:
                # If we scan a specific object, it has to exist in initial_data
                scanned_object = self.inv.get_by_id(plan.env, plan.object_id)
                if not scanned_object:
                    exc_msg = "No object found with specified id: '{}'" \
                        .format(plan.object_id)
                    raise ScanArgumentsError(exc_msg)
                plan.object_type = scanned_object["type"]
                plan.parent_id = scanned_object["parent_id"]
                plan.type_to_scan = scanned_object["parent_type"]

        class_module = plan.object_type
        if not plan.scan_self:
            plan.scan_self = plan.object_type != "environment"

        plan.object_type = plan.object_type.title().replace("_", "")

        if not plan.scan_self:
            plan.child_type = None
        else:
            plan.child_id = plan.object_id
            plan.object_id = plan.parent_id
            if plan.type_to_scan.endswith("_folder"):
                class_module = plan.child_type + "s_root"
            else:
                class_module = plan.type_to_scan
            plan.object_type = class_module.title().replace("_", "")

        if class_module == "environment":
            plan.obj = {"id": plan.env}
        else:
            # fetch object from inventory
            obj = self.inv.get_by_id(plan.env, plan.object_id)
            if not obj:
                raise ValueError("No match for object ID: {}"
                                 .format(plan.object_id))
            plan.obj = obj

        plan.scanner_type = "Scan" + plan.object_type
        return plan

    @staticmethod
    def reset_connections(ignore_errors=False):
        ApiAccess.reset()
        AciAccess().logout(ignore_errors=ignore_errors)
        DbAccess.close_connection()
        SshConnection.disconnect_all()

    def validate_results(self, env):
        self.log.info("Running post-scan validations")
        result = True
        errors = []
        for validator_class in validators:
            self.log.info("Running validator: {}".format(validator_class.__name__))
            v_result, v_errors = validator_class(env).run()
            if v_result is False:
                result = False
            errors.extend(v_errors)
            self.log.info("Validator '{}' finished. {} detected".format(validator_class.__name__,
                                                                        "Errors" if v_errors else "No errors"))
        return result, errors

    def run(self, args: dict = None):
        args = setup_args(args, self.DEFAULTS, self.get_args)
        # After this setup we assume args dictionary has all keys
        # defined in self.DEFAULTS
        if args.get('logger'):
            self.log = args['logger']
        self.log.set_loglevel(args['loglevel'])

        try:
            MongoAccess.set_config_file(args['mongo_config'])
            self.inv = InventoryMgr()
            self.inv.log.set_loglevel(args['loglevel'])
            self.inv.set_collections(args['inventory'])
            self.conf = Configuration()
        except FileNotFoundError as e:
            return False, 'Mongo configuration file not found: {}'\
                .format(str(e))

        #validation_result, validation_errors = self.validate_results(args['env'])
        #return validation_result, 'validation errors detected' if validation_errors else 'ok'

        scan_plan = self.get_scan_plan(args)
        if scan_plan.clear or scan_plan.clear_all:
            self.inv.clear(scan_plan)
        self.conf.log.set_loglevel(scan_plan.loglevel)

        env_name = scan_plan.env
        self.conf.use_env(env_name)

        # Reset active connections
        self.reset_connections(ignore_errors=True)

        # generate ScanObject Class and instance.
        scanner = Scanner()
        scanner.log.set_loglevel(args['loglevel'])
        scanner.setup(env=env_name, origin=args['origin'])
        scanner.found_errors[env_name] = False

        # decide what scanning operations to do
        inventory_only = scan_plan.inventory_only
        processors_only = scan_plan.processors_only
        links_only = scan_plan.links_only
        cliques_only = scan_plan.cliques_only
        monitoring_setup_only = scan_plan.monitoring_setup_only
        run_all = not any((inventory_only, processors_only, links_only, cliques_only, monitoring_setup_only))

        # setup monitoring server
        monitoring = \
            self.inv.is_feature_supported(env_name,
                                          EnvironmentFeatures.MONITORING)
        if monitoring:
            self.inv.monitoring_setup_manager = \
                MonitoringSetupManager(env_name)
            if run_all or inventory_only:
                self.inv.monitoring_setup_manager.server_setup()

        # do the actual scanning
        try:
            if inventory_only or run_all:
                scanner.run_scan(
                    scan_plan.scanner_type,
                    scan_plan.obj,
                    scan_plan.id_field,
                    scan_plan.child_id,
                    scan_plan.child_type)
            if processors_only or run_all:
                scanner.run_processors()
            if links_only or run_all:
                scanner.scan_links()
            if cliques_only or run_all:
                scanner.scan_cliques()
            if monitoring:
                if monitoring_setup_only:
                    self.inv.monitoring_setup_manager.simulate_track_changes()
                if not any((inventory_only, processors_only, links_only, cliques_only)):
                    scanner.deploy_monitoring_setup()
        except ScanError as e:
            return False, "Scan error: {}".format(e)
        finally:
            self.reset_connections()

        status = 'ok' if not scanner.found_errors.get(env_name, False) \
            else 'errors detected'
        if status == 'ok' and scan_plan.object_type == "environment":
            self.mark_env_scanned(scan_plan.env)
        self.log.info('Scan completed, status: {}'.format(status))

        # self.log.info('Starting ES upload')
        # es = ElasticAccess()
        # es.dump_collections(args['env'])
        # es.dump_tree(args['env'])
        # self.log.info('ES upload successful')
        # return True, ""

        validation_result, validation_errors = self.validate_results(env_name)
        return validation_result, 'validation errors detected' if validation_errors else status

    def mark_env_scanned(self, env):
        environments_collection = self.inv.collection['environments_config']
        environments_collection \
            .update_one(filter={'name': env},
                        update={'$set': {'scanned': True}})


if __name__ == '__main__':
    scan_controller = ScanController()
    ret, msg = scan_controller.run()
    if not ret:
        scan_controller.log.error(msg)
    sys.exit(0 if ret else 1)
