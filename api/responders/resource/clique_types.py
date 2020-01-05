###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from bson.objectid import ObjectId

from api.responders.responder_base import ResponderBase
from api.validation.data_validate import DataValidate


class CliqueTypes(ResponderBase):

    COLLECTION = "clique_types"
    ID = "_id"
    PROJECTION = {
        ID: True,
        "focal_point_type": True,
        "link_types": True,
        "environment": True,
        "name": True,
        "distribution": True,
        "distribution_version": True,
        "mechanism_drivers": True,
        "type_drivers": True,
        "use_implicit_links": True
    }
    RESERVED_NAMES = ["ANY"]

    def __init__(self):
        super().__init__()
        self.focal_point_types = self.get_constants_by_name("object_types")
        self.link_types = self.get_constants_by_name("link_types")
        self.mechanism_drivers = self.get_constants_by_name("mechanism_drivers")
        self.type_drivers = self.get_constants_by_name("type_drivers")

    def on_get(self, req, resp):
        self.log.debug("Getting clique types")

        filters = self.parse_query_params(req)
        filters_requirements = {
            'env_name': self.require(str),
            'id': self.require(ObjectId, convert_to_type=True),
            'distribution': self.require(str),
            'distribution_version': self.require(str),
            'mechanism_drivers': self.require(str,
                                              validate=DataValidate.LIST,
                                              requirement=self.mechanism_drivers),
            'type_drivers': self.require(str,
                                         validate=DataValidate.LIST,
                                         requirement=self.type_drivers),
            'focal_point_type': self.require(str,
                                             validate=DataValidate.LIST,
                                             requirement=self.focal_point_types),
            'link_type': self.require([list, str],
                                      validate=DataValidate.LIST,
                                      requirement=self.link_types),
            'name': self.require(str),
            'page': self.require(int, convert_to_type=True),
            'page_size': self.require(int, convert_to_type=True)
        }

        self.validate_query_data(filters, filters_requirements)
        if 'distribution_version' in filters and 'distribution' not in filters:
            self.bad_request("Distribution version without distribution "
                             "is not allowed")

        page, page_size = self.get_pagination(filters)
        query = self.build_query(filters)
        if self.ID in query:
            clique_type = self.get_object_by_id(self.COLLECTION, query,
                                                [ObjectId], self.ID)
            self.set_ok_response(resp, clique_type)
        else:
            clique_types_ids = self.get_objects_list(self.COLLECTION,
                                                     query,
                                                     page, page_size, self.PROJECTION)
            self.set_ok_response(resp, {"clique_types": clique_types_ids})

    def on_post(self, req, resp):
        self.log.debug("Posting new clique_type")
        error, clique_type = self.get_content_from_request(req)
        if error:
            self.bad_request(error)

        clique_type_requirements = {
            'environment': self.require(str),
            'focal_point_type': self.require(str,
                                             mandatory=True,
                                             validate=DataValidate.LIST,
                                             requirement=self.focal_point_types),
            'link_types': self.require(list,
                                       mandatory=True,
                                       validate=DataValidate.LIST,
                                       requirement=self.link_types),
            'name': self.require(str, mandatory=True),
            'distribution': self.require(str),
            'distribution_version': self.require(str),
            'mechanism_drivers': self.require(str,
                                              validate=DataValidate.LIST,
                                              requirement=self.mechanism_drivers),
            'type_drivers': self.require(str,
                                         validate=DataValidate.LIST,
                                         requirement=self.type_drivers),
            'use_implicit_links': self.require(bool)
        }

        self.validate_query_data(clique_type, clique_type_requirements)
        self.validate_required_fields(clique_type)
        self.validate_focal_point_type(clique_type)
        self.validate_duplicate_configuration(clique_type)

        result = self.write(clique_type, self.COLLECTION)
        response_body = {
            "message": "created a new clique_type",
            "id": str(result.inserted_id)
        }
        self.set_created_response(resp, response_body)

    def build_query(self, filters):
        query = {}
        filters_keys = ['name', 'focal_point_type',
                        'distribution', 'distribution_version',
                        'mechanism_drivers', 'type_drivers']
        self.update_query_with_filters(filters, filters_keys, query)

        link_types = filters.get('link_type')
        if link_types:
            if type(link_types) != list:
                link_types = [link_types]
            query['link_types'] = {'$all': link_types}
        _id = filters.get('id')
        if _id:
            query[self.ID] = _id

        env_name = filters.get('env_name')
        if env_name:
            query['environment'] = filters['env_name']
        return query

    def validate_required_fields(self, clique_type):
        env_name = clique_type.get('environment')
        distribution = clique_type.get('distribution')
        distribution_version = clique_type.get('distribution_version')
        if distribution_version and not distribution:
            self.bad_request("Distribution version without distribution "
                             "is not allowed")

        configuration_specified = ((distribution and distribution_version)
                                   or clique_type.get('mechanism_drivers')
                                   or clique_type.get('type_drivers'))
        if env_name:
            if configuration_specified:
                self.bad_request("Either environment or configuration "
                                 "should be specified (not both).")

            if not self.check_environment_name(env_name):
                self.bad_request("Unknown environment: {}".format(env_name))
            elif env_name.upper() in self.RESERVED_NAMES:
                self.bad_request(
                    "Environment name '{}' is reserved".format(env_name))
        elif not configuration_specified:
            self.bad_request("Either environment or configuration "
                             "should be specified.")

    def validate_focal_point_type(self, clique_type):
        focal_point_type = clique_type['focal_point_type']
        environment = clique_type.get('environment')
        if environment:
            env_match = self.read(
                matches={"environment": environment,
                         "focal_point_type": focal_point_type},
                collection="clique_types"
            )
            if env_match:
                self.bad_request("Clique type with focal point {} "
                                 "is already registered for environment {}"
                                 .format(focal_point_type, environment))
        else:
            pass

    def validate_duplicate_configuration(self, clique_type):
        if clique_type.get('environment'):
            return

        search = {'focal_point_type': clique_type['focal_point_type']}
        for field in ['distribution', 'mechanism_drivers', 'type_drivers']:
            value = clique_type.get(field)
            if value:
                search[field] = value
                if field == 'distribution':
                    dv = clique_type.get('distribution_version')
                    if dv:
                        search['distribution_version'] = dv
                # Got a match with higher score, no need to look further
                break

        env_match = self.read(matches=search,
                              collection="clique_types")
        if env_match:
            self.bad_request("Clique type with configuration '{}' "
                             "is already registered"
                             .format(search))
