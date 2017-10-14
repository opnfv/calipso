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


class CliqueTypes(ResponderBase):

    COLLECTION = "clique_types"
    ID = "_id"
    PROJECTION = {
        ID: True,
        "focal_point_type": True,
        "link_types": True,
        "environment": True,
        "name": True
    }
    RESERVED_NAMES = ["ANY"]

    def on_get(self, req, resp):
        self.log.debug("Getting clique types")

        filters = self.parse_query_params(req)
        focal_point_types = self.get_constants_by_name("object_types")
        link_types = self.get_constants_by_name("link_types")
        filters_requirements = {
            'env_name': self.require(str, mandatory=True),
            'id': self.require(ObjectId, convert_to_type=True),
            'focal_point_type': self.require(str,
                                             validate=DataValidate.LIST,
                                             requirement=focal_point_types),
            'link_type': self.require([list, str],
                                      validate=DataValidate.LIST,
                                      requirement=link_types),
            'name': self.require(str),
            'page': self.require(int, convert_to_type=True),
            'page_size': self.require(int, convert_to_type=True)
        }

        self.validate_query_data(filters, filters_requirements)
        page, page_size = self.get_pagination(filters)
        query = self.build_query(filters)
        if self.ID in query:
            clique_type = self.get_object_by_id(self.COLLECTION, query,
                                                [ObjectId], self.ID)
            self.set_successful_response(resp, clique_type)
        else:
            clique_types_ids = self.get_objects_list(self.COLLECTION,
                                                     query,
                                                     page, page_size, self.PROJECTION)
            self.set_successful_response(resp,
                                         {"clique_types": clique_types_ids})

    def on_post(self, req, resp):
        self.log.debug("Posting new clique_type")
        error, clique_type = self.get_content_from_request(req)
        if error:
            self.bad_request(error)
        focal_point_types = self.get_constants_by_name("object_types")
        link_types = self.get_constants_by_name("link_types")
        clique_type_requirements = {
            'environment': self.require(str, mandatory=True),
            'focal_point_type': self.require(str,
                                             mandatory=True,
                                             validate=DataValidate.LIST,
                                             requirement=focal_point_types),
            'link_types': self.require(list,
                                       mandatory=True,
                                       validate=DataValidate.LIST,
                                       requirement=link_types),
            'name': self.require(str, mandatory=True)
        }

        self.validate_query_data(clique_type, clique_type_requirements)

        env_name = clique_type['environment']
        if not self.check_environment_name(env_name):
            self.bad_request("Unknown environment: {}".format(env_name))
        elif env_name.upper() in self.RESERVED_NAMES:
            self.bad_request("Environment name '{}' is reserved".format(env_name))

        self.write(clique_type, self.COLLECTION)
        self.set_successful_response(resp,
                                     {"message": "created a new clique_type "
                                                 "for environment {0}"
                                                 .format(env_name)},
                                     "201")

    def build_query(self, filters):
        query = {}
        filters_keys = ['name', 'focal_point_type']
        self.update_query_with_filters(filters, filters_keys, query)
        link_types = filters.get('link_type')
        if link_types:
            if type(link_types) != list:
                link_types = [link_types]
            query['link_types'] = {'$all': link_types}
        _id = filters.get('id')
        if _id:
            query[self.ID] = _id

        query['environment'] = filters['env_name']
        return query
