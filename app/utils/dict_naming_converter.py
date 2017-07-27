###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
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
    def change_dict_naming_convention(d, cf):
        new = {}
        if not d:
            return d
        if isinstance(d, str):
            return d
        if isinstance(d, ObjectId):
            return d
        for k, v in d.items():
            new_v = v
            if isinstance(v, dict):
                new_v = DictNamingConverter.change_dict_naming_convention(v, cf)
            elif isinstance(v, list):
                new_v = list()
                for x in v:
                    new_v.append(DictNamingConverter.change_dict_naming_convention(x, cf))
            new[cf(k)] = new_v
        return new
