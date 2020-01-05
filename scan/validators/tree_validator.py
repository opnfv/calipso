###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from scan.validators.validator_base import ValidatorBase


class TreeValidator(ValidatorBase):
    def run(self) -> (bool, list):
        objects_list = self.inv.find(search={"environment": self.env},
                                     projection=['_id', 'id', 'type', 'parent_id', 'parent_type'])

        errors = []
        objects_dict = {}
        for obj in objects_list:
            if obj['id'] in objects_dict:
                errors.append("Duplicate id: '{}' for object: '{}' of type '{}'".format(obj['id'],
                                                                                        obj['_id'],
                                                                                        obj['type']))
            else:
                objects_dict[obj['id']] = obj

        for obj_id, obj in objects_dict.items():
            if obj['parent_id'] not in objects_dict and obj['parent_type'] != 'environment':
                errors.append("Missing parent object with id: '{}' for object: '{}' of type '{}'".format(obj['parent_id'],
                                                                                                         obj['_id'],
                                                                                                         obj['type']))

        # TODO: search for cycles?

        return not errors, errors
