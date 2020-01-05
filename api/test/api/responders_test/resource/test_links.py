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
from api.test.api.responders_test.test_data import links
from api.test.api.test_base import TestBase


class TestLinks(TestBase):

    def test_get_links_list_without_env_name(self):
        self.validate_get_request(links.URL,
                                  params={},
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_links_list_with_invalid_filters(self):
        self.validate_get_request(links.URL,
                                  params={
                                      'invalid': 'invalid'
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_links_list_with_wrong_link_type(self):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'link_type': links.WRONG_TYPE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_links_list_with_correct_link_type(self, read):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'link_type': links.CORRECT_TYPE
                                  },
                                  mocks={
                                      read: links.LINKS_WITH_SPECIFIC_TYPE
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=links.
                                       LINKS_WITH_SPECIFIC_TYPE_RESPONSE
                                  )

    def test_get_links_list_with_wrong_state(self):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'state': links.WRONG_STATE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_links_list_with_correct_state(self, read):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'state': links.CORRECT_STATE
                                  },
                                  mocks={
                                      read: links.LINKS_WITH_SPECIFIC_STATE,
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=links.
                                      LINKS_WITH_SPECIFIC_STATE_RESPONSE
                                  )

    def test_get_link_with_env_name_and_wrong_link_id(self):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'id': links.WRONG_LINK_ID
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_link_with_env_name_and_link_id(self, read):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'id': links.LINK_ID
                                  },
                                  mocks={
                                      read: links.LINKS_WITH_SPECIFIC_ID
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=links.
                                      LINKS_WITH_SPECIFIC_ID[0]
                                  )

    def test_get_links_list_with_non_int_page(self):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'page': base.NON_INT_PAGE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_links_list_with_int_page(self, read):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'page': base.INT_PAGE
                                  },
                                  mocks={
                                      read: links.LINKS
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=links.LINKS_LIST_RESPONSE)

    def test_get_link_ids_with_non_int_page_size(self):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'page_size': base.NON_INT_PAGESIZE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_links_list_with_int_page_size(self, read):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'page_size': base.INT_PAGESIZE
                                  },
                                  mocks={
                                      read: links.LINKS
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=links.LINKS_LIST_RESPONSE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_links_list_with_env_name_and_unknown_host(self, read, check_env_name):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'host': links.UNKNOWN_HOST
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: True
                                  },
                                  expected_code=base.NOT_FOUND_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_links_list_with_unknown_env_name(self, read, check_env_name):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.UNKNOWN_ENV
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: False
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_link_with_env_name_and_nonexistent_link_id(self, read, check_env_name):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'id': links.NONEXISTENT_LINK_ID
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: True
                                  },
                                  expected_code=base.NOT_FOUND_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_link_with_unknown_env_name(self, read, check_env_name):
        self.validate_get_request(links.URL,
                                  params={
                                      'env_name': base.UNKNOWN_ENV
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: False
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)
