###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from datetime import datetime

from bson.objectid import ObjectId


class DictNamingConverter:

    # Convert a nested dictionary from one convention to another.
    # Args:
    #     d (dict): dictionary (nested or not) to be converted.
    #     cf (func): convert function - takes the string in one convention,
    #                returns it in the other one.
    # Returns:
    #     Dictionary with the new keys.
    @staticmethod
    def change_dict_naming_convention(d, cf, level: int=0):
        new = {}
        change_convention = DictNamingConverter.change_dict_naming_convention
        if not d:
            return d
        if isinstance(d, str) or isinstance(d, int) or isinstance(d, float) \
                or isinstance(d, bool) or isinstance(d, datetime):
            return d
        if isinstance(d, ObjectId):
            return d
        if isinstance(d, object) and not isinstance(d, dict):
            for k in dir(d):
                if k.startswith('_'):
                    continue
                v = getattr(d, k)
                if callable(v):
                    continue
                new[cf(k)] = change_convention(v, cf, level+1)
        if isinstance(d, dict):
            for k, v in d.items():
                new_v = v
                if isinstance(v, dict):
                    new_v = change_convention(v, cf, level+1)
                elif isinstance(v, list):
                    new_v = list()
                    for x in v:
                        list_val = change_convention(x, cf, level+1)
                        new_v.append(list_val)
                new[cf(k)] = new_v
        return new
