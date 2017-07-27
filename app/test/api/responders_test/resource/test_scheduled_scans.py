###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json

from test.api.responders_test.test_data import base
from test.api.test_base import TestBase
from test.api.responders_test.test_data import scheduled_scans
from unittest.mock import patch


class TestScheduledScans(TestBase):
    def test_get_scheduled_scans_list_without_env_name(self):
        self.validate_get_request(scheduled_scans.URL,
                                  params={},
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_scheduled_scans_list_with_invalid_filter(self):
        self.validate_get_request(scheduled_scans.URL,
                                  params={
                                      "environment": base.ENV_NAME,
                                      "invalid": "invalid"
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_scheduled_scans_list_with_non_int_page(self):
        self.validate_get_request(scheduled_scans.URL,
                                  params={
                                      "environment": base.ENV_NAME,
                                      "page": base.NON_INT_PAGE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_scheduled_scans_list_with_int_page(self, read):
        self.validate_get_request(scheduled_scans.URL,
                                  params={
                                      "environment": base.ENV_NAME,
                                      "page": base.INT_PAGE
                                  },
                                  mocks={
                                      read: scheduled_scans.SCHEDULED_SCANS
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=scheduled_scans.
                                      SCHEDULED_SCANS_RESPONSE
                                  )

    def test_get_scheduled_scans_list_with_non_int_pagesize(self):
        self.validate_get_request(scheduled_scans.URL,
                                  params={
                                      "environment": base.ENV_NAME,
                                      "page_size": base.NON_INT_PAGESIZE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_scheduled_scans_list_with_int_pagesize(self, read):
        self.validate_get_request(scheduled_scans.URL,
                                  params={
                                      "environment": base.ENV_NAME,
                                      "page_size": base.INT_PAGESIZE
                                  },
                                  mocks={
                                      read: scheduled_scans.SCHEDULED_SCANS
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=scheduled_scans.
                                      SCHEDULED_SCANS_RESPONSE
                                  )

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_scheduled_scans_list_with_unknown_env(self, read, check_env_name):
        self.validate_get_request(scheduled_scans.URL,
                                  params={
                                      "environment": base.UNKNOWN_ENV
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: False
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_scheduled_scans_list_with_wrong_freq(self):
        self.validate_get_request(scheduled_scans.URL,
                                  params={
                                      "environment": base.ENV_NAME,
                                      "freq": scheduled_scans.WRONG_FREQ
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_scheduled_scans_list_with_freq(self, read):
        self.validate_get_request(scheduled_scans.URL,
                                  params={
                                      "environment": base.ENV_NAME,
                                      "freq": scheduled_scans.CORRECT_FREQ
                                  },
                                  mocks={
                                      read: scheduled_scans.
                                            SCHEDULED_SCAN_WITH_SPECIFIC_FREQ,
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=scheduled_scans.
                                      SCHEDULED_SCAN_WITH_SPECIFIC_FREQ_RESPONSE
                                  )

    def test_get_scheduled_scan_with_wrong_id(self):
        self.validate_get_request(scheduled_scans.URL,
                                  params={
                                      "environment": base.ENV_NAME,
                                      "id": scheduled_scans.WRONG_ID
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_scan_with_nonexistent_id(self, read, check_env_name):
        self.validate_get_request(scheduled_scans.URL,
                                  params={
                                      "environment": base.ENV_NAME,
                                      "id": scheduled_scans.NONEXISTENT_ID
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: True
                                  },
                                  expected_code=base.NOT_FOUND_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_scheduled_scan_with_unknown_env_and_nonexistent_id(self, read,
                                                                    check_env_name):
        self.validate_get_request(scheduled_scans.URL,
                                  params={
                                      "environment": base.UNKNOWN_ENV,
                                      "id": scheduled_scans.NONEXISTENT_ID
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: False
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_scheduled_scan_with_id(self, read):
        self.validate_get_request(scheduled_scans.URL,
                                  params={
                                      "environment": base.ENV_NAME,
                                      "id": scheduled_scans.CORRECT_ID
                                  },
                                  mocks={
                                      read: scheduled_scans.
                                            SCHEDULED_SCAN_WITH_SPECIFIC_ID
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=scheduled_scans.
                                      SCHEDULED_SCAN_WITH_SPECIFIC_ID[0]
                                  )

    def test_post_scheduled_scan_with_non_dict_scheduled_scan(self):
        self.validate_post_request(scheduled_scans.URL,
                                   body=json.dumps(scheduled_scans.
                                                   NON_DICT_SCHEDULED_SCAN),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_bad_scheduled_scans(self):
        test_cases = [
            {
                "body": scheduled_scans.
                    SCHEDULED_SCAN_WITHOUT_ENV
            },
            {
                "body": scheduled_scans.
                    SCHEDULED_SCAN_WITHOUT_FREQ
            },
            {
                "body": scheduled_scans.
                    SCHEDULED_SCAN_WITH_WRONG_FREQ
            },
            {
                "body": scheduled_scans.
                    SCHEDULED_SCAN_WITH_WRONG_LOG_LEVEL
            },
            {
                "body": scheduled_scans.
                    SCHEDULED_SCAN_WITHOUT_SUBMIT_TIMESTAMP
            },
            {
                "body": scheduled_scans.
                    SCHEDULED_SCAN_WITH_WRONG_SUBMIT_TIMESTAMP
            },
            {
                "body": scheduled_scans.
                    SCHEDULED_SCAN_WITH_NON_BOOL_CLEAR
            },
            {
                "body": scheduled_scans.
                    SCHEDULED_SCAN_WITH_NON_BOOL_SCAN_ONLY_LINKS
            },
            {
                "body": scheduled_scans.
                    SCHEDULED_SCAN_WITH_NON_BOOL_SCAN_ONLY_CLIQUES
            },
            {
                "body": scheduled_scans.
                    SCHEDULED_SCAN_WITH_NON_BOOL_SCAN_ONLY_INVENTORY
            },
            {
                "body": scheduled_scans.
                    SCHEDULED_SCAN_WITH_EXTRA_SCAN_ONLY_FLAGS
            }
        ]
        for test_case in test_cases:
            self.validate_post_request(scheduled_scans.URL,
                                       body=json.dumps(test_case["body"]),
                                       expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    def test_post_scheduled_scan_with_unknown_env_name(self,
                                                       check_environment_name):
        self.validate_post_request(scheduled_scans.URL,
                                   mocks={
                                       check_environment_name: False
                                   },
                                   body=json.dumps(scheduled_scans.
                                                   SCHEDULED_SCAN_WITH_UNKNOWN_ENV),
                                   expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_WRITE)
    def test_post_scheduled_scan(self, write, check_env_name):
        self.validate_post_request(scheduled_scans.URL,
                                   mocks={
                                       check_env_name: True,
                                       write: None
                                   },
                                   body=json.dumps(scheduled_scans.
                                                   SCHEDULED_SCAN),
                                   expected_code=base.CREATED_CODE)
