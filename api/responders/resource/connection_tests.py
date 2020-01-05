###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import datetime

from bson import ObjectId

from api.responders.resource.environment_configs import EnvironmentConfigs
from api.responders.responder_base import ResponderBase
from api.validation.data_validate import DataValidate


# The actual tests are run from tests/functest/connection_test.py
# this not under app/
class ConnectionTests(ResponderBase):

    COLLECTION = "connection_tests"
    ID = "_id"
    TARGETS = "test_targets"
    RESULTS = "test_results"
    CONFIGURATIONS = "targets_configuration"
    STATUSES = ["request", "response"]
    PROJECTION = {
        ID: True,
        TARGETS: True,
        RESULTS: True
    }

    def __init__(self):
        super().__init__()
        self.allowed_targets = \
            self.get_constants_by_name("configuration_targets")

    def build_query(self, filters):
        query = {}

        self.update_query_with_filters(filters, ["status"], query)

        if 'id' in filters:
            query[self.ID] = filters['id']
        elif 'env_name' in filters:
            query['environment'] = filters['env_name']
        else:
            self.bad_request(message="Either 'id' or 'env_name' "
                                     "field is required")

        return query

    def on_get(self, req, resp):
        self.log.debug("Getting a connection test")
        filters = self.parse_query_params(req)

        filters_requirements = {
            'env_name': self.require(str, mandatory=True),
            'id': self.require(ObjectId, convert_to_type=True),
            'status': self.require(str,
                                   requirement=self.STATUSES),
            self.TARGETS: self.require([list, str],
                                       validate=DataValidate.LIST,
                                       requirement=self.allowed_targets),
            self.RESULTS: self.require(bool, convert_to_type=True),
            'page': self.require(int, convert_to_type=True),
            'page_size': self.require(int, convert_to_type=True)
        }

        self.validate_query_data(filters, filters_requirements)

        query = self.build_query(filters)

        if self.ID in query:
            result = self.get_object_by_id(collection=self.COLLECTION,
                                           query=query,
                                           stringify_types=[ObjectId,
                                                            datetime.datetime],
                                           id=self.ID)

            test_targets = result.get(self.TARGETS, [])
            targets_config = result.get(self.CONFIGURATIONS, [])
            test_results = result.get(self.RESULTS, {})

            # Filter data by target names
            targets_filter = filters.get(self.TARGETS)
            if targets_filter:
                test_targets = [target
                                for target in test_targets
                                if target in targets_filter]
                targets_config = [config
                                  for config in targets_config
                                  if config['name'] in targets_filter]
                test_results = {target: result
                                for target, result in test_results.items()
                                if target in targets_filter}

            # Filter data by test results (success/failure)
            results_filter = filters.get(self.RESULTS)
            if results_filter is not None:
                test_results = {target: result
                                for target, result in test_results.items()
                                if result == results_filter}

                results_keys = test_results.keys()
                test_targets = [target
                                for target in test_targets
                                if target in results_keys]
                targets_config = [config
                                  for config in targets_config
                                  if config['name'] in results_keys]

            result[self.TARGETS] = test_targets
            result[self.CONFIGURATIONS] = targets_config
            result[self.RESULTS] = test_results

            self.set_ok_response(resp, result)
        else:
            page, page_size = self.get_pagination(filters)
            tests_ids = self.get_objects_list(collection=self.COLLECTION,
                                              query=query,
                                              page=page,
                                              page_size=page_size,
                                              projection=self.PROJECTION)
            self.set_ok_response(resp, {"connection_tests": tests_ids})

    def on_post(self, req, resp):
        self.log.debug("Posting a new connection test")
        error, connection_test = self.get_content_from_request(req)
        if error:
            self.bad_request(error)

        conn_test_requirements = {
            "environment": self.require(str, mandatory=True),
            self.TARGETS: self.require(list,
                                       mandatory=True,
                                       validate=DataValidate.LIST,
                                       requirement=self.allowed_targets),
            self.CONFIGURATIONS: self.require(list, mandatory=True)
        }
        self.validate_query_data(connection_test, conn_test_requirements)

        test_targets = connection_test[self.TARGETS]
        targets_configuration = connection_test[self.CONFIGURATIONS]
        env_name = connection_test["environment"]

        env_configs = EnvironmentConfigs()
        config_validation = env_configs.validate_environment_config(
            connection_test[self.CONFIGURATIONS],
            require_mandatory=False
        )
        if not config_validation['passed']:
            self.bad_request(config_validation['error_message'])

        for test_target in test_targets:
            if not env_configs.get_configuration_by_name(test_target,
                                                         targets_configuration):
                self.bad_request("targets_configuration should contain "
                                 "an entry for target '{}'".format(test_target))

        connection_test['submit_timestamp'] = datetime.datetime.now()

        result = self.write(connection_test, self.COLLECTION)
        response_body = {
            "message": "Created a new connection test for environment {0}".format(env_name),
            "id": str(result.inserted_id)
        }
        self.set_created_response(resp, response_body)
