###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import patch

from api.test.api.responders_test.test_data import aggregates
from api.test.api.responders_test.test_data import base
from api.test.api.test_base import TestBase


class TestAggregates(TestBase):

    def test_get_aggregate_without_type(self):
        self.validate_get_request(aggregates.URL,
                                  params={},
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_aggregate_with_wrong_filter(self):
        self.validate_get_request(aggregates.URL,
                                  params={
                                      "unknown": "unknown"
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_environment_aggregates_without_env_name(self):
        self.validate_get_request(aggregates.URL,
                                  params={
                                      "type": aggregates.ENV_TYPE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    def test_get_environment_aggregates_with_unknown_env_name(self,
                                                              check_env_name):
        self.validate_get_request(aggregates.URL,
                                  params={
                                      "type": aggregates.ENV_TYPE,
                                      "env_name": base.UNKNOWN_ENV
                                  },
                                  mocks={
                                      check_env_name: False
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_AGGREGATE)
    def test_get_environment_aggregates_with_env_name(self, aggregates_method,
                                                      check_env_name):
        self.validate_get_request(aggregates.URL,
                                  params={
                                      "type": aggregates.ENV_TYPE,
                                      "env_name": base.ENV_NAME
                                  },
                                  mocks={
                                      check_env_name: True,
                                      aggregates_method:
                                          aggregates.ENVIRONMENT_AGGREGATES
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=
                                  aggregates.ENVIRONMENT_AGGREGATES_RESPONSE
                                  )

    @patch(base.RESPONDER_BASE_AGGREGATE)
    def test_get_message_aggregates(self, aggregate):
        self.validate_get_request(aggregates.URL,
                                  params={
                                      "type": aggregates.MESSAGE_TYPE
                                  },
                                  side_effects={aggregate: [
                                      aggregates.MESSAGE_ENV_AGGREGATES,
                                      aggregates.MESSAGE_LEVEL_AGGREGATES]
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=
                                  aggregates.MESSAGE_AGGREGATES_RESPONSE
                                  )

    @patch(base.RESPONDER_BASE_AGGREGATE)
    def test_get_constant_aggregates(self, aggregate):
        self.validate_get_request(aggregates.URL,
                                  params={
                                      "type": aggregates.CONSTANT_TYPE
                                  },
                                  mocks={
                                      aggregate: aggregates.CONSTANT_AGGREGATES
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=
                                  aggregates.CONSTANT_AGGREGATES_RESPONSE
                                  )

    def test_get_unknown_aggregates(self):
        self.validate_get_request(aggregates.URL,
                                  params={
                                      "type": aggregates.UNKNOWN_TYPE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)
