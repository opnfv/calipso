###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from api.responders.responder_base import ResponderBase
from api.validation.data_validate import DataValidate
from bson.objectid import ObjectId


class Links(ResponderBase):
    def __init__(self):
        super().__init__()
        self.COLLECTION = 'links'
        self.ID = '_id'
        self.PROJECTION = {
            self.ID: True,
            "link_name": True,
            "link_type": True,
            "environment": True,
            "host": True
        }

    def on_get(self, req, resp):
        self.log.debug("Getting links from links")

        filters = self.parse_query_params(req)

        link_types = self.get_constants_by_name("link_types")
        link_states = self.get_constants_by_name("link_states")
        filters_requirements = {
            'env_name': self.require(str, mandatory=True),
            'id': self.require(ObjectId, convert_to_type=True),
            'host': self.require(str),
            'link_type': self.require(str,
                                      validate=DataValidate.LIST,
                                      requirement=link_types),
            'link_name': self.require(str),
            'source_id': self.require(str),
            'target_id': self.require(str),
            'state': self.require(str,
                                  validate=DataValidate.LIST,
                                  requirement=link_states),
            'page': self.require(int, convert_to_type=True),
            'page_size': self.require(int, convert_to_type=True)
        }

        self.validate_query_data(filters, filters_requirements, r'^attributes\:\w+$')
        filters = self.change_dict_naming_convention(filters, self.replace_colon_with_dot)
        page, page_size = self.get_pagination(filters)
        query = self.build_query(filters)
        if self.ID in query:
            link = self.get_object_by_id(self.COLLECTION, query,
                                         [ObjectId], self.ID)
            self.set_successful_response(resp, link)
        else:
            links_ids = self.get_objects_list(self.COLLECTION, query,
                                              page, page_size, self.PROJECTION)
            self.set_successful_response(resp, {"links": links_ids})

    def build_query(self, filters):
        query = {}
        filters_keys = ['host', 'link_type', 'link_name',
                        'source_id', 'target_id', 'state']
        self.update_query_with_filters(filters, filters_keys, query)
        # add attributes to the query
        for key in filters.keys():
            if key.startswith("attributes."):
                query[key] = filters[key]
        _id = filters.get('id')
        if _id:
            query[self.ID] = _id
        query['environment'] = filters['env_name']
        return query
