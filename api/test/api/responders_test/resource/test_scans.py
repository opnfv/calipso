###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json
from unittest.mock import patch

from api.test.api.responders_test.test_data import base
from api.test.api.responders_test.test_data import scans
from api.test.api.test_base import TestBase


class TestScans(TestBase):
    
    def test_get_scans_list_without_env_name(self):
        self.validate_get_request(scans.URL,
                                  params={},
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_scans_list_with_invalid_filter(self):
        self.validate_get_request(scans.URL,
                                  params={
                                      "env_name": base.ENV_NAME,
                                      "invalid": "invalid"
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_scans_list_with_non_int_page(self):
        self.validate_get_request(scans.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "page": base.NON_INT_PAGE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_scans_list_with_int_page(self, read):
        self.validate_get_request(scans.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "page": base.INT_PAGE
                                  },
                                  mocks={
                                     read: scans.SCANS
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=scans.SCANS_RESPONSE)

    def test_get_scans_list_with_non_int_pagesize(self):
        self.validate_get_request(scans.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "page_size": base.NON_INT_PAGESIZE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_scans_list_with_int_pagesize(self, read):
        self.validate_get_request(scans.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "page_size": base.INT_PAGESIZE
                                  },
                                  mocks={
                                     read: scans.SCANS
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=scans.SCANS_RESPONSE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_scans_list_with_unknown_env(self, read, check_env_name):
        self.validate_get_request(scans.URL,
                                  params={
                                      "env_name": base.UNKNOWN_ENV
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: False
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_scans_list_with_base_object(self, read):
        self.validate_get_request(scans.URL,
                                  params={
                                      "env_name": base.ENV_NAME,
                                      "base_object": scans.BASE_OBJECT
                                  },
                                  mocks={
                                      read: scans.SCANS_WITH_SPECIFIC_BASE_OBJ
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=scans.
                                      SCANS_WITH_SPECIFIC_BASE_OBJ_RESPONSE
                                  )

    def test_get_scans_list_with_wrong_status(self):
        self.validate_get_request(scans.URL,
                                  params={
                                      "env_name": base.ENV_NAME,
                                      "status": scans.WRONG_STATUS
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_scans_list_with_status(self, read):
        self.validate_get_request(scans.URL,
                                  params={
                                      "env_name": base.ENV_NAME,
                                      "status": scans.CORRECT_STATUS
                                  },
                                  mocks={
                                      read: scans.SCANS_WITH_SPECIFIC_STATUS,
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=scans.
                                      SCANS_WITH_SPECIFIC_STATUS_RESPONSE
                                  )

    def test_get_scan_with_wrong_id(self):
        self.validate_get_request(scans.URL,
                                  params={
                                      "env_name": base.ENV_NAME,
                                      "id": scans.WRONG_ID
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_scan_with_nonexistent_id(self, read, check_env_name):
        self.validate_get_request(scans.URL,
                                  params={
                                      "env_name": base.ENV_NAME,
                                      "id": scans.NONEXISTENT_ID
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: True
                                  },
                                  expected_code=base.NOT_FOUND_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_scan_with_unknown_env_and_nonexistent_id(self, read, check_env_name):
        self.validate_get_request(scans.URL,
                                  params={
                                      "env_name": base.UNKNOWN_ENV,
                                      "id": scans.NONEXISTENT_ID
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: False
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_scan_with_id(self, read):
        self.validate_get_request(scans.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "id": scans.CORRECT_ID
                                  },
                                  mocks={
                                     read: scans.SCANS_WITH_SPECIFIC_ID
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=scans.SCANS_WITH_SPECIFIC_ID[0]
                                  )

    def test_post_scan_with_non_dict_scan(self):
        self.validate_post_request(scans.URL,
                                   body=json.dumps(scans.NON_DICT_SCAN),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_scan_without_env_name(self):
        self.validate_post_request(scans.URL,
                                   body=json.dumps(scans.SCAN_WITHOUT_ENV),
                                   expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    def test_post_scan_with_unknown_env_name(self, check_environment_name):
        self.validate_post_request(scans.URL,
                                   mocks={
                                       check_environment_name: False
                                   },
                                   body=json.dumps(scans.SCAN_WITH_UNKNOWN_ENV),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_scan_without_status(self):
        self.validate_post_request(scans.URL,
                                   body=json.dumps(scans.SCAN_WITHOUT_STATUS),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_scan_with_wrong_status(self):
        self.validate_post_request(scans.URL,
                                   body=json.dumps(scans.SCAN_WITH_WRONG_STATUS),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_scan_with_wrong_log_level(self):
        self.validate_post_request(scans.URL,
                                   body=json.dumps(scans.SCAN_WITH_WRONG_LOG_LEVEL),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_scan_with_non_bool_clear(self):
        self.validate_post_request(scans.URL,
                                   body=json.dumps(scans.SCAN_WITH_NON_BOOL_CLEAR),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_scan_with_non_bool_scan_only_inventory(self):
        self.validate_post_request(scans.URL,
                                   body=json.dumps(scans.SCAN_WITH_NON_BOOL_SCAN_ONLY_INVENTORY),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_scan_with_non_bool_scan_only_links(self):
        self.validate_post_request(scans.URL,
                                   body=json.dumps(scans.SCAN_WITH_NON_BOOL_SCAN_ONLY_LINKS),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_scan_with_non_bool_scan_only_cliques(self):
        self.validate_post_request(scans.URL,
                                   body=json.dumps(scans.SCAN_WITH_NON_BOOL_SCAN_ONLY_CLIQUES),
                                   expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_WRITE)
    def test_post_scan(self, write, check_env_name):
        self.validate_post_request(scans.URL,
                                   mocks={
                                      check_env_name: True,
                                      write: None
                                   },
                                   body=json.dumps(scans.SCAN),
                                   expected_code=base.CREATED_CODE)
