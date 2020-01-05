###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import importlib
import signal

import os
import re
from bson.objectid import ObjectId


class SignalHandler:

    def __init__(self, signals=(signal.SIGTERM, signal.SIGINT)):
        super().__init__()
        self.terminated = False
        for sig in signals:
            signal.signal(sig, self.handle)

    def handle(self, signum, frame):
        self.terminated = True


class ClassResolver:
    instances = {}

    # convert class name in camel case to module file name in underscores
    @staticmethod
    def get_module_file_by_class_name(class_name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
        module_file = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        return module_file

    # convert module file name in underscores to class name in camel case
    @staticmethod
    def get_class_name_by_module(module_name):
        name_parts = [word.capitalize() for word in module_name.split('_')]
        class_name = ''.join(name_parts)
        return class_name

    @staticmethod
    def get_fully_qualified_class(class_name: str = None,
                                  package_name: str = "discover",
                                  module_name: str = None):
        module_file = module_name if module_name \
            else ClassResolver.get_module_file_by_class_name(class_name)
        module_parts = [package_name, module_file]
        module_name = ".".join(module_parts)
        try:
            class_module = importlib.import_module(module_name)
        except ImportError as e:
            raise ValueError('could not import module {}: {}'
                             .format(module_name, str(e)))

        clazz = getattr(class_module, class_name)
        return clazz

    @staticmethod
    def prepare_class(class_name: str = None,
                      package_name: str = "discover",
                      module_name: str = None):
        if not class_name and not module_name:
            raise ValueError('class_name or module_name must be provided')
        if not class_name:
            class_name = ClassResolver.get_class_name_by_module(module_name)
        if class_name in ClassResolver.instances:
            return 'instance', ClassResolver.instances[class_name]
        clazz = ClassResolver.get_fully_qualified_class(class_name,
                                                        package_name,
                                                        module_name)
        return 'class', clazz

    @staticmethod
    def get_instance_of_class(class_name: str = None,
                              package_name: str = "discover",
                              module_name: str = None):
        val_type, clazz = \
            ClassResolver.prepare_class(class_name=class_name,
                                        package_name=package_name,
                                        module_name=module_name)
        if val_type == 'instance':
            return clazz
        instance = clazz()
        ClassResolver.instances[class_name] = instance
        return instance

    @staticmethod
    def get_instance_single_arg(arg: object,
                                class_name: str = None,
                                package_name: str = "discover",
                                module_name: str = None):
        val_type, clazz = \
            ClassResolver.prepare_class(class_name=class_name,
                                        package_name=package_name,
                                        module_name=module_name)
        if val_type == 'instance':
            return clazz
        instance = clazz(arg)
        ClassResolver.instances[class_name] = instance
        return instance


# TODO: translate the following comment
# when search in the mongo initial_data, need to
# generate the ObjectId with the string
def generate_object_ids(keys, obj):
    for key in keys:
        if key in obj:
            o = obj.pop(key)
            if o:
                try:
                    o = ObjectId(o)
                except Exception:
                    raise Exception("{0} is not a valid object id".
                                    format(o))
            obj[key] = o


# Get arguments from CLI or another source
# and convert them to dict to enforce uniformity.
# Throws a TypeError if arguments can't be converted to dict.
def setup_args(args: dict,
               defaults,
               get_cmd_args=None):
    if defaults is None:
        defaults = {}

    if args is None and get_cmd_args is not None:
        args = vars(get_cmd_args())
    elif not isinstance(args, dict):
        try:
            args = dict(args)
        except TypeError:
            try:
                args = vars(args)
            except TypeError:
                raise TypeError("Wrong arguments format")

    return dict(defaults, **args)


def encode_router_id(uuid: str):
    return '-'.join(['qrouter', uuid])


def decode_router_id(router_id: str):
    return router_id.split('qrouter-')[-1]


def get_extension(file_path: str) -> str:
    return os.path.splitext(file_path)[1][1:]


def encode_aci_dn(object_id):
    return object_id.replace("topology/", "").replace("/", "__")


def decode_aci_dn(object_id):
    return object_id.replace("__", "/")


def get_object_path_part(path: str, part_name: str):
    match = re.match(".*/{}/(.+?)/.*".format(part_name), path)
    return match.group(1) if match else None


def merge_dicts(*dicts):
    result = {}
    for dictionary in dicts:
        result.update(dictionary)
    return result


# required and optional parameters should be dicts
# of the following structure: {"target key name": "environment variable name"}
# empty_is_none parameter is used to fill missing optional keys with None value
# rather than omitting them
def read_environment_variables(required=None, optional=None, empty_is_none=False):
    errors = []
    results = {}

    for key, variable_name in required.items():
        if variable_name not in os.environ:
            errors.append(variable_name)
        else:
            results[key] = os.environ[variable_name]
    if errors:
        raise ValueError("Environment variables are missing: {}".format(errors))

    for key, variable_name in optional.items():
        if variable_name not in os.environ:
            if empty_is_none:
                results[key] = None
        else:
            results[key] = os.environ[variable_name]

    return results
