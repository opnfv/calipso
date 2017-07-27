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

from utils.util import generate_object_ids


class Cliques(ResponderBase):
    def __init__(self):
        super().__init__()
        self.COLLECTION = "cliques"
        self.ID = '_id'
        self.PROJECTION = {
            self.ID: True,
            "focal_point_type": True,
            "environment": True
        }

    def on_get(self, req, resp):
        self.log.debug("Getting cliques")

        filters = self.parse_query_params(req)
        focal_point_types = self.get_constants_by_name("object_types")
        link_types = self.get_constants_by_name("link_types")
        filters_requirements = {
            'env_name': self.require(str, mandatory=True),
            'id': self.require(ObjectId, True),
            'focal_point': self.require(ObjectId, True),
            'focal_point_type': self.require(str, validate=DataValidate.LIST,
                                             requirement=focal_point_types),
            'link_type': self.require(str, validate=DataValidate.LIST,
                                      requirement=link_types),
            'link_id': self.require(ObjectId, True),
            'page': self.require(int, True),
            'page_size': self.require(int, True)
        }
        self.validate_query_data(filters, filters_requirements)
        page, page_size = self.get_pagination(filters)
        query = self.build_query(filters)

        if self.ID in query:
            clique = self.get_object_by_id(self.COLLECTION, query,
                                           [ObjectId], self.ID)
            self.set_successful_response(resp, clique)
        else:
            cliques_ids = self.get_objects_list(self.COLLECTION, query,
                                                page, page_size, self.PROJECTION)
            self.set_successful_response(resp, {"cliques": cliques_ids})

    def build_query(self, filters):
        query = {}
        filters_keys = ['focal_point', 'focal_point_type']
        self.update_query_with_filters(filters, filters_keys, query)
        link_type = filters.get('link_type')
        if link_type:
            query['links_detailed.link_type'] = link_type
        link_id = filters.get('link_id')
        if link_id:
            query['links_detailed._id'] = link_id
        _id = filters.get('id')
        if _id:
            query[self.ID] = _id
        query['environment'] = filters['env_name']
        return query
