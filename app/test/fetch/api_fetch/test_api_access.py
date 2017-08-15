###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import patch, MagicMock, Mock

import requests

from discover.fetchers.api.api_access import ApiAccess
from test.fetch.api_fetch.test_data.api_access import *
from test.fetch.test_fetch import TestFetch
from test.fetch.api_fetch.test_data.regions import REGIONS


class TestApiAccess(TestFetch):

    def setUp(self):
        self.configure_environment()
        self.api_access = ApiAccess()
        self.set_regions_for_fetcher(self.api_access)
        self.response = MagicMock()
        self.response.status_code = requests.codes.ok

    def test_parse_time_without_dot_in_time(self):
        time = self.api_access.parse_time(TIME_WITHOUT_DOT)
        self.assertNotEqual(time, None, "Can't parse the time without dot")

    def test_parse_time_with_dot_in_time(self):
        time = self.api_access.parse_time(TIME_WITH_DOT)
        self.assertNotEqual(time, None, "Can't parse the time with dot")

    def test_parse_illegal_time(self):
        time = self.api_access.parse_time(ILLEGAL_TIME)
        self.assertEqual(time, None, "Can't get None when the time format is wrong")

    def test_get_existing_token(self):
        self.api_access.tokens = VALID_TOKENS
        token = self.api_access.get_existing_token(PROJECT)
        self.assertNotEqual(token, VALID_TOKENS[PROJECT], "Can't get existing token")

    def test_get_nonexistent_token(self):
        self.api_access.tokens = EMPTY_TOKENS
        token = self.api_access.get_existing_token(TEST_PROJECT)
        self.assertEqual(token, None, "Can't get None when the token doesn't " +
                                      "exist in tokens")

    @patch("requests.post")
    def test_v2_auth(self, mock_request):
        self.api_access.get_existing_token = MagicMock(return_value=None)
        self.response.json = Mock(return_value=CORRECT_AUTH_CONTENT)
        # mock authentication info from OpenStack Api
        mock_request.return_value = self.response
        token_details = self.api_access.v2_auth(TEST_PROJECT, TEST_HEADER, TEST_BODY)
        self.assertNotEqual(token_details, None, "Can't get the token details")

    @patch("requests.post")
    def test_v2_auth_with_error_content(self, mock_request):
        self.api_access.get_existing_token = MagicMock(return_value=None)
        self.response.json = Mock(return_value=ERROR_AUTH_CONTENT)
        # authentication content from OpenStack Api will be incorrect
        mock_request.return_value = self.response
        token_details = self.api_access.v2_auth(TEST_PROJECT, TEST_HEADER, TEST_BODY)
        self.assertIs(token_details, None, "Can't get None when the content is wrong")

    @patch("requests.post")
    def test_v2_auth_with_error_token(self, mock_request):
        self.response.status_code = requests.codes.bad_request
        self.response.json = Mock(return_value=ERROR_TOKEN_CONTENT)
        # authentication info from OpenStack Api will not contain token info
        mock_request.return_value = self.response
        token_details = self.api_access.v2_auth(TEST_PROJECT, TEST_HEADER, TEST_BODY)
        self.assertIs(token_details, None, "Can't get None when the content " +
                                           "doesn't contain any token info")

    @patch("requests.post")
    def test_v2_auth_with_error_expiry_time(self, mock_request):
        self.response.json = Mock(return_value=CORRECT_AUTH_CONTENT)
        mock_request.return_value = self.response

        # store original parse_time method
        original_method = self.api_access.parse_time
        # the time will not be parsed
        self.api_access.parse_time = MagicMock(return_value=None)

        token_details = self.api_access.v2_auth(TEST_PROJECT, TEST_HEADER, TEST_BODY)
        # reset original parse_time method
        self.api_access.parse_time = original_method

        self.assertIs(token_details, None, "Can't get None when the time in token " +
                                           "can't be parsed")

    @patch("requests.post")
    def test_v2_auth_pwd(self, mock_request):
        self.response.json = Mock(return_value=CORRECT_AUTH_CONTENT)
        # mock the authentication info from OpenStack Api
        mock_request.return_value = self.response
        token = self.api_access.v2_auth_pwd(PROJECT)
        self.assertNotEqual(token, None, "Can't get token")

    @patch("requests.get")
    def test_get_url(self, mock_request):
        self.response.json = Mock(return_value=GET_CONTENT)
        mock_request.return_value = self.response
        result = self.api_access.get_url(TEST_URL, TEST_HEADER)
        # check whether it returns content message when the response is correct
        self.assertNotEqual(result, None, "Can't get content when the "
                                          "response is correct")

    @patch("requests.get")
    def test_get_url_with_error_response(self, mock_request):
        self.response.status_code = requests.codes.bad_request
        self.response.json = Mock(return_value=None)
        self.response.text = "Bad request"
        # the response will be wrong
        mock_request.return_value = self.response
        result = self.api_access.get_url(TEST_URL, TEST_HEADER)
        self.assertEqual(result, None, "Result returned" +
                                       "when the response status is not 200")

    def test_get_region_url(self):
        region_url = self.api_access.get_region_url(REGION_NAME, SERVICE_NAME)

        self.assertNotEqual(region_url, None, "Can't get region url")

    def test_get_region_url_with_wrong_region_name(self):
        # error region name doesn't exist in the regions info
        region_url = self.api_access.get_region_url(ERROR_REGION_NAME, "")
        self.assertIs(region_url, None, "Can't get None with the region " +
                                        "name is wrong")

    def test_get_region_url_without_service_endpoint(self):
        # error service doesn't exist in region service endpoints
        region_url = self.api_access.get_region_url(REGION_NAME, ERROR_SERVICE_NAME)
        self.assertIs(region_url, None, "Can't get None with wrong service name")

    def test_region_url_nover(self):
        # mock return value of get_region_url, which has something starting from v2
        self.api_access.get_region_url = MagicMock(return_value=REGION_URL)
        region_url = self.api_access.get_region_url_nover(REGION_NAME, SERVICE_NAME)
        # get_region_nover will remove everything from v2
        self.assertNotIn("v2", region_url, "Can't get region url without v2 info")

    def test_get_service_region_endpoints(self):
        region = REGIONS[REGION_NAME]
        result = self.api_access.get_service_region_endpoints(region, SERVICE_NAME)
        self.assertNotEqual(result, None, "Can't get service endpoint")

    def test_get_service_region_endpoints_with_nonexistent_service(self):
        region = REGIONS[REGION_NAME]
        result = self.api_access.get_service_region_endpoints(region, ERROR_SERVICE_NAME)
        self.assertIs(result, None, "Can't get None when the service name " +
                                    "doesn't exist in region's services")
