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

from utils.mongo_access import MongoAccess
from utils.util import ClassResolver

DEFAULTS = {
    'env': 'WebEX-Mirantis@Cisco',
    'inventory': 'inventory',
    'loglevel': 'WARNING'
}



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mongo_config", nargs="?", type=str,
                        default="",
                        help="name of config file with MongoDB server " +
                        "access details")
    parser.add_argument("-e", "--env", nargs="?", type=str,
                        default=DEFAULTS['env'],
                        help="name of environment to scan \n" +
                        "(default: {})".format(DEFAULTS['env']))
    parser.add_argument("-y", "--inventory", nargs="?", type=str,
                        default=DEFAULTS['inventory'],
                        help="name of inventory collection \n" +
                        "(default: {}".format(DEFAULTS['inventory']))
    parser.add_argument('-i', '--inputfile', nargs='?', type=str,
                        default='',
                        help="read input from the specifed file \n" +
                        "(default: from stdin)")
    parser.add_argument("-l", "--loglevel", nargs="?", type=str,
                        default=DEFAULTS["loglevel"],
                        help="logging level \n(default: '{}')"
                        .format(DEFAULTS["loglevel"]))
    args = parser.parse_args()
    return args

input = None
args = get_args()
MongoAccess.set_config_file(args.mongo_config)
if args.inputfile:
    try:
        with open(args.inputfile, 'r') as input_file:
            input = input_file.read()
    except Exception as e:
        raise FileNotFoundError("failed to open input file: " + args.inputfile)
        exit(1)
else:
    input = sys.stdin.read()
    if not input:
        raise ValueError("No input provided on stdin")
        exit(1)

check_result_full = json.loads(input)
check_client = check_result_full['client']
check_result = check_result_full['check']
check_result['id'] = check_result_full['id']
name = check_result['name']
status = check_result['status']
object_type = name[:name.index('_')]
object_id = name[name.index('_')+1:]
if 'environment' in check_client:
    args.env = check_client['environment']

handler = None
basic_handling_types = ['vedge', 'vservice']
if object_type in basic_handling_types:
    from monitoring.handlers.basic_check_handler import BasicCheckHandler
    handler = BasicCheckHandler(args)
else:
    module_name = 'handle_' + object_type
    handler = ClassResolver.get_instance_single_arg(args,
                                                    module_name=module_name,
                                                    package_name='monitoring.handlers')
if handler:
    handler.handle(object_id, check_result)
