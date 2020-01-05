###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import MagicMock

from scan.fetchers.api.api_fetch_availability_zones import ApiFetchAvailabilityZones
from scan.test.fetch.api_fetch.test_data.api_fetch_availability_zones import *
from scan.test.fetch.api_fetch.test_data.token import TOKEN
from scan.test.fetch.test_fetch import TestFetch


class TestApiFetchAvailabilityZones(TestFetch):

    def setUp(self):
        super().setUp()
        self.configure_environment()

        self._v2_auth_pwd = ApiFetchAvailabilityZones.v2_auth_pwd
        ApiFetchAvailabilityZones.v2_auth_pwd = MagicMock(return_value=TOKEN)

        self.fetcher = ApiFetchAvailabilityZones()
        self.set_regions_for_fetcher(self.fetcher)

    def test_get_for_region(self):
        # mock the endpoint url
        self.fetcher.get_region_url_nover = MagicMock(return_value=ENDPOINT)
        # mock the response from OpenStack Api
        self.fetcher.get_url = MagicMock(return_value=AVAILABILITY_ZONE_RESPONSE)

        result = self.fetcher.get_for_region(PROJECT, REGION_NAME, TOKEN)
        self.assertNotEqual(result, [], "Can't get availability zone info")

    def test_get_for_region_with_wrong_response(self):
        # mock the endpoint url
        self.fetcher.get_region_url_nover = MagicMock(return_value=ENDPOINT)
        # mock the wrong response from OpenStack Api
        self.fetcher.get_url = MagicMock(return_value=WRONG_RESPONSE)

        result = self.fetcher.get_for_region(PROJECT, REGION_NAME, TOKEN)
        self.assertEqual(result, [], "Can't get [] when the response is wrong")

    def test_get_for_region_without_avz_response(self):
        # mock the endpoint url
        self.fetcher.get_region_url_nover = MagicMock(return_value=ENDPOINT)
        # mock the response from OpenStack Api
        # the response doesn't contain availability zone info
        self.fetcher.get_url = MagicMock(return_value=RESPONSE_WITHOUT_AVAILABILITY_ZONE)

        result = self.fetcher.get_for_region(PROJECT, REGION_NAME, TOKEN)
        self.assertEqual(result, [], "Can't get [] when the response doesn't " +
                                     "contain availability zone")

    def test_get(self):
        # store original get_tenants_for_region method
        original_method = self.fetcher.get_for_region
        # mock the result from get_tenants_for_region method
        self.fetcher.get_for_region = MagicMock(return_value=GET_REGION_RESULT)

        result = self.fetcher.get(PROJECT)

        # reset get_tenants_for_region method
        self.fetcher.get_for_region = original_method

        self.assertNotEqual(result, [], "Can't get availability zone info")

    def test_get_without_token(self):
        # mock the empty token
        self.fetcher.v2_auth_pwd = MagicMock(return_value=None)
        result = self.fetcher.get(PROJECT)
        self.fetcher.v2_auth_pwd = MagicMock(return_value=TOKEN)
        self.assertEqual(result, [], "Can't get [] when the token is invalid")

    def tearDown(self):
        super().tearDown()
        ApiFetchAvailabilityZones.v2_auth_pwd = self._v2_auth_pwd
        self.reset_regions_for_fetcher(self.fetcher)
