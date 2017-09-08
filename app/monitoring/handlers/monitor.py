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

# handle monitoring events

import argparse
import json
import sys

from utils.inventory_mgr import InventoryMgr
from utils.mongo_access import MongoAccess
from utils.util import ClassResolver


class Monitor:
    DEFAULTS = {
        'env': 'WebEX-Mirantis@Cisco',
        'inventory': 'inventory',
        'loglevel': 'WARNING'
    }

    def __init__(self):
        self.args = self.get_args()
        MongoAccess.set_config_file(self.args.mongo_config)
        self.inv = InventoryMgr()
        self.inv.set_collections(self.args.inventory)
        self.input_text = None

    def get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--mongo_config", nargs="?", type=str,
                            default="",
                            help="name of config file with MongoDB server " +
                            "access details")
        parser.add_argument("-e", "--env", nargs="?", type=str,
                            default=self.DEFAULTS['env'],
                            help="name of environment to scan \n" +
                            "(default: {})".format(self.DEFAULTS['env']))
        parser.add_argument("-y", "--inventory", nargs="?", type=str,
                            default=self.DEFAULTS['inventory'],
                            help="name of inventory collection \n" +
                            "(default: {}".format(self.DEFAULTS['inventory']))
        parser.add_argument('-i', '--inputfile', nargs='?', type=str,
                            default='',
                            help="read input from the specifed file \n" +
                            "(default: from stdin)")
        parser.add_argument("-l", "--loglevel", nargs="?", type=str,
                            default=self.DEFAULTS["loglevel"],
                            help="logging level \n(default: '{}')"
                            .format(self.DEFAULTS["loglevel"]))
        args = parser.parse_args()
        return args

    def get_type_list(self, type_name) -> list:
        types_list = []
        docs = self.inv.find_items({'name': type_name}, collection='constants')
        for types_list in docs:
            types_list = [t['value'] for t in types_list['data']]
        if not types_list:
            raise ValueError('Unable to fetch {}'
                             .format(type_name.replace('_', ' ')))
        return types_list

    def match_object_types(self, check_name: str) -> list:
        object_types = self.get_type_list('object_types')
        matches = [t for t in object_types if check_name.startswith(t + '_')]
        return matches

    def match_link_types(self, check_name: str) -> list:
        object_types = self.get_type_list('link_types')
        matches = [t for t in object_types
                   if check_name.startswith('link_' + t + '_')]
        return matches

    def find_object_type_and_id(self, check_name: str):
        # if we have multiple matching host types, then take the longest
        # of these. For example, if matches are ['host', 'host_pnic'],
        # then take 'host_pnic'.
        # To facilitate this, we sort the matches by reverse order.
        is_link_check = check_name.startswith('link_')
        check_type = 'link' if is_link_check else 'object'
        if is_link_check:
            matching_types = sorted(self.match_link_types(check_name),
                                    reverse=True)
        else:
            matching_types = sorted(self.match_object_types(check_name),
                                    reverse=True)
        if not matching_types:
            raise ValueError('Unable to match check name "{}" with {} type'
                             .format(check_name, check_type))
        obj_type = matching_types[0]
        postfix_len = len('link_') if is_link_check else 0
        obj_id = (obj_type + '_' if is_link_check else '') + \
            check_name[len(obj_type)+1+postfix_len:]
        return check_type, obj_type, obj_id

    def read_input(self):
        if self.args.inputfile:
            try:
                with open(self.args.inputfile, 'r') as input_file:
                    self.input_text = input_file.read()
            except Exception as e:
                raise FileNotFoundError("failed to open input file {}: {}"
                                        .format(self.args.inputfile, str(e)))
        else:
            self.input_text = sys.stdin.read()
            if not self.input_text:
                raise ValueError("No input provided on stdin")

    def get_handler_by_type(self, check_type, obj_type):
        module_name = 'handle_link' if check_type == 'link' \
                else 'handle_' + obj_type
        package = 'monitoring.handlers'
        handler = ClassResolver.get_instance_single_arg(self.args,
                                                        module_name=module_name,
                                                        package_name=package)
        return handler

    def get_handler(self, check_type, obj_type):
        basic_handling_types = ['vedge', 'vservice']
        if obj_type not in basic_handling_types:
            return self.get_handler_by_type(check_type, obj_type)
        from monitoring.handlers.basic_check_handler \
            import BasicCheckHandler
        return BasicCheckHandler(self.args)

    def process_input(self):
        check_result_full = json.loads(self.input_text)
        check_client = check_result_full['client']
        check_result = check_result_full['check']
        check_result['id'] = check_result_full['id']
        name = check_result['name']
        check_type, object_type, object_id = \
            monitor.find_object_type_and_id(name)
        if 'environment' in check_client:
            self.args.env = check_client['environment']

        check_handler = self.get_handler(check_type, object_type)
        if check_handler:
            check_handler.handle(object_id, check_result)

    def process_check_result(self):
        self.read_input()
        self.process_input()

monitor = Monitor()
monitor.process_check_result()
