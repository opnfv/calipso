###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from api.validation.data_validate import DataValidate
from api.responders.responder_base import ResponderBase
from bson.objectid import ObjectId


class MonitoringConfigTemplates(ResponderBase):
    def __init__(self):
        super().__init__()
        self.ID = "_id"
        self.COLLECTION = "monitoring_config_templates"
        self.PROJECTION = {
            self.ID: True,
            "side": True,
            "type": True
        }

    def on_get(self, req, resp):
        self.log.debug("Getting monitoring config template")

        filters = self.parse_query_params(req)

        sides = self.get_constants_by_name("monitoring_sides")
        filters_requirements = {
            "id": self.require(ObjectId, convert_to_type=True),
            "order": self.require(int, convert_to_type=True),
            "side": self.require(str,
                                 validate=DataValidate.LIST,
                                 requirement=sides),
            "type": self.require(str),
            "page": self.require(int, convert_to_type=True),
            "page_size": self.require(int, convert_to_type=True)
        }

        self.validate_query_data(filters, filters_requirements)

        page, page_size = self.get_pagination(filters)
        query = self.build_query(filters)
        if self.ID in query:
            template = self.get_object_by_id(self.COLLECTION, query,
                                             [ObjectId], self.ID)
            self.set_successful_response(resp, template)
        else:
            templates = self.get_objects_list(self.COLLECTION, query,
                                              page, page_size, self.PROJECTION)
            self.set_successful_response(
                resp,
                {"monitoring_config_templates": templates}
            )

    def build_query(self, filters):
        query = {}
        filters_keys = ["order", "side", "type"]
        self.update_query_with_filters(filters, filters_keys, query)
        _id = filters.get('id')
        if _id:
            query[self.ID] = _id
        return query
