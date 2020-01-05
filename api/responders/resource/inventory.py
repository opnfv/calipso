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

from api.responders.responder_base import ResponderBase
from api.validation.data_validate import DataValidate


class Inventory(ResponderBase):

    COLLECTION = 'inventory'
    ID = 'id'
    PROJECTION = {
        ID: True,
        "name": True,
        "name_path": True,
        "type": True,
        "environment": True
    }

    def __init__(self):
        super().__init__()
        self.object_types = self.get_constants_by_name("object_types")

    def on_get(self, req, resp):
        self.log.debug("Getting objects from inventory")

        filters = self.parse_query_params(req)
        filters_requirements = {
            'env_name': self.require(str),
            'id': self.require(str),
            'id_path': self.require(str),
            'type': self.require(str, validate=DataValidate.LIST, requirement=self.object_types),
            'parent_id': self.require(str),
            'parent_path': self.require(str),
            'sub_tree': self.require(bool, convert_to_type=True),
            'page': self.require(int, convert_to_type=True),
            'page_size': self.require(int, convert_to_type=True)
        }
        self.validate_query_data(filters, filters_requirements)
        page, page_size = self.get_pagination(filters)
        query = self.build_query(filters)
        if self.ID in query:
            obj = self.get_object_by_id(self.COLLECTION, query,
                                        [ObjectId, datetime], self.ID)
            self.set_ok_response(resp, obj)
        else:
            objects = self.get_objects_list(self.COLLECTION, query,
                                            page, page_size, self.PROJECTION)
            self.set_ok_response(resp, {"objects": objects})

    def build_query(self, filters):
        query = {}
        filters_keys = ['parent_id', 'id_path', 'id', 'type']
        self.update_query_with_filters(filters, filters_keys, query)
        parent_path = filters.get('parent_path')
        if parent_path:
            regular_expression = parent_path
            if filters.get('sub_tree', False):
                regular_expression += "[/]?"
            else:
                regular_expression += "/[^/]+$"
            query['id_path'] = {"$regex": regular_expression}
        if 'env_name' in filters:
            query['environment'] = filters['env_name']
        return query
