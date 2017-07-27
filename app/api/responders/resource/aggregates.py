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


class Aggregates(ResponderBase):
    def __init__(self):
        super().__init__()
        self.AGGREGATE_TYPES = ["environment", "message", "constant"]
        self.AGGREGATES_MAP = {
            "environment": self.get_environments_aggregates,
            "message": self.get_messages_aggregates,
            "constant": self.get_constants_aggregates
        }

    def on_get(self, req, resp):
        self.log.debug("Getting aggregates information")

        filters = self.parse_query_params(req)
        filters_requirements = {
            "env_name": self.require(str),
            "type": self.require(str, validate=DataValidate.LIST,
                                 requirement=self.AGGREGATE_TYPES,
                                 mandatory=True,
                                 error_messages={"mandatory":
                                                 "type must be specified: " +
                                                 "environment/" +
                                                 " message/" +
                                                 "constant"})
        }
        self.validate_query_data(filters, filters_requirements)
        query = self.build_query(filters)
        query_type = query["type"]
        if query_type == "environment":
            env_name = query.get("env_name")
            if not env_name:
                self.bad_request("env_name must be specified")
            if not self.check_environment_name(env_name):
                self.bad_request("unknown environment: " + env_name)

        aggregates = self.AGGREGATES_MAP[query_type](query)
        self.set_successful_response(resp, aggregates)

    def build_query(self, filters):
        query = {}
        env_name = filters.get("env_name")
        query_type = filters["type"]
        query["type"] = filters["type"]
        if query_type == "environment":
            if env_name:
                query['env_name'] = env_name
            return query
        return query

    def get_environments_aggregates(self, query):
        env_name = query['env_name']
        aggregates = {
            "type": query["type"],
            "env_name": env_name,
            "aggregates": {
                "object_types": {

                }
            }
        }
        pipeline = [
            {
                '$match': {
                    'environment': env_name
                }
            },
            {
                '$group': {
                    '_id': '$type',
                    'total': {
                        '$sum': 1
                    }
                }
            }
        ]
        groups = self.aggregate(pipeline, "inventory")
        for group in groups:
            aggregates['aggregates']['object_types'][group['_id']] = \
                group['total']
        return aggregates

    def get_messages_aggregates(self, query):
        aggregates = {
            "type": query['type'],
            "aggregates": {
                "levels": {},
                "environments": {}
            }
        }
        env_pipeline = [
            {
                '$group': {
                    '_id': '$environment',
                    'total': {
                        '$sum': 1
                    }
                }
            }
        ]
        environments = self.aggregate(env_pipeline, "messages")
        for environment in environments:
            aggregates['aggregates']['environments'][environment['_id']] = \
                environment['total']
        level_pipeline = [
            {
                '$group': {
                    '_id': '$level',
                    'total': {
                        '$sum': 1
                    }
                }
            }
        ]
        levels = self.aggregate(level_pipeline, "messages")
        for level in levels:
            aggregates['aggregates']['levels'][level['_id']] = \
                level['total']

        return aggregates

    def get_constants_aggregates(self, query):
        aggregates = {
            "type": query['type'],
            "aggregates": {
                "names": {}
            }
        }
        pipeline = [
            {
                '$project': {
                    '_id': 0,
                    'name': 1,
                    'total': {
                        '$size': '$data'
                    }
                }
            }
        ]
        constants = self.aggregate(pipeline, "constants")
        for constant in constants:
            aggregates['aggregates']['names'][constant['name']] = \
                constant['total']

        return aggregates
