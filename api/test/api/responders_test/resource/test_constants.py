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

from api.test.api.responders_test.test_data import base
from api.test.api.responders_test.test_data import constants
from api.test.api.test_base import TestBase


class TestConstants(TestBase):

    def test_get_constant_without_name(self):
        self.validate_get_request(constants.URL,
                                  params={},
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_constant_with_unknown_filter(self):
        self.validate_get_request(constants.URL,
                                  params={
                                      "unknown": "unknown"
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_constant_with_unknown_name(self, read):
        self.validate_get_request(constants.URL,
                                  params={
                                      "name": constants.UNKNOWN_NAME
                                  },
                                  mocks={
                                      read: []
                                  },
                                  expected_code=base.NOT_FOUND_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_constant(self, read):
        self.validate_get_request(constants.URL,
                                  params={
                                      "name": constants.NAME
                                  },
                                  mocks={
                                      read: constants.CONSTANTS_WITH_SPECIFIC_NAME
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=constants.
                                      CONSTANTS_WITH_SPECIFIC_NAME[0]
                                  )
