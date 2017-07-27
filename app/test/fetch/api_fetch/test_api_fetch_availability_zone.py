from discover.fetchers.api.api_fetch_availability_zones import ApiFetchAvailabilityZones
from test.fetch.test_fetch import TestFetch
from test.fetch.api_fetch.test_data.api_fetch_availability_zones import *
from unittest.mock import MagicMock
from test.fetch.api_fetch.test_data.token import TOKEN


class TestApiFetchAvailabilityZones(TestFetch):

    def setUp(self):
        self.configure_environment()
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
        # store original get_for_region method
        original_method = self.fetcher.get_for_region
        # mock the result from get_for_region method
        self.fetcher.get_for_region = MagicMock(return_value=GET_REGION_RESULT)

        result = self.fetcher.get(PROJECT)

        # reset get_for_region method
        self.fetcher.get_for_region = original_method

        self.assertNotEqual(result, [], "Can't get availability zone info")

    def test_get_without_token(self):
        # mock the empty token
        self.fetcher.v2_auth_pwd = MagicMock(return_value=None)
        result = self.fetcher.get(PROJECT)
        self.fetcher.v2_auth_pwd = MagicMock(return_value=TOKEN)
        self.assertEqual(result, [], "Can't get [] when the token is invalid")
