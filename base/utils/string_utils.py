###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json
from datetime import datetime

from inflection import pluralize
from bson import ObjectId


def jsonify(obj, prettify=False):
    if prettify:
        return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        return json.dumps(obj)


# stringify datetime object
def stringify_datetime(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")


# stringify ObjectId
def stringify_object_id(object_id):
    return str(object_id)


stringify_map = {
    ObjectId: stringify_object_id,
    datetime: stringify_datetime
}


def stringify_object_values_by_type(obj, object_type):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, object_type):
                obj[key] = stringify_map[object_type](value)
            else:
                stringify_object_values_by_type(value, object_type)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            if isinstance(value, object_type):
                obj[index] = stringify_map[object_type](value)
            else:
                stringify_object_values_by_type(value, object_type)


# convert some values of the specific types of the object into string
# e.g convert all the ObjectId to string
#     convert all the datetime object to string
def stringify_object_values_by_types(obj, object_types=stringify_map.keys()):
    for object_type in object_types:
        stringify_object_values_by_type(obj, object_type)


def stringify_doc(doc):
    stringify_object_values_by_types(doc, stringify_map.keys())


def plural(name):
    return pluralize(name)
