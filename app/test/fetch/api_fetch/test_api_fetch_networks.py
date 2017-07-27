from unittest.mock import MagicMock
from discover.fetchers.api.api_fetch_networks import ApiFetchNetworks
from test.fetch.test_fetch import TestFetch
from test.fetch.api_fetch.test_data.api_fetch_networks import *
from test.fetch.api_fetch.test_data.token import TOKEN


class TestApiFetchNetworks(TestFetch):

    def setUp(self):
        self.configure_environment()
        ApiFetchNetworks.v2_auth_pwd = MagicMock(return_value=TOKEN)
        self.fetcher = ApiFetchNetworks()
        self.set_regions_for_fetcher(self.fetcher)

    def test_get_networks(self):
        self.fetcher.get_region_url_nover = MagicMock(return_value=ENDPOINT)
        self.fetcher.get_url = MagicMock(side_effect=[NETWORKS_RESPONSE,
                                                      SUBNETS_RESPONSE])
        self.fetcher.inv.get_by_id = MagicMock(return_value=PROJECT)
        result = self.fetcher.get_networks(REGION_NAME, TOKEN)
        self.assertEqual(result, NETWORKS_RESULT, "Can't get networks info")

    def test_get_networks_with_wrong_networks_response(self):
        self.fetcher.get_region_url_nover = MagicMock(return_value=ENDPOINT)
        self.fetcher.get_url = MagicMock(return_value=WRONG_NETWORK_RESPONSE)

        result = self.fetcher.get_networks(REGION_NAME, TOKEN)
        self.assertEqual(result, [], "Can't get [] when the networks " +
                                     "response is wrong")

    def test_get_networks_with_wrong_subnet_response(self):
        self.fetcher.get_region_url_nover = MagicMock(return_value=ENDPOINT)
        self.fetcher.get_url = MagicMock(side_effect=[NETWORKS_RESPONSE,
                                                      WRONG_SUBNETS_RESPONSE])
        self.fetcher.inv.get_by_id = MagicMock(return_value=PROJECT)

        result = self.fetcher.get_networks(REGION_NAME, TOKEN)

        self.assertNotEqual(result, [], "Can't get networks info when the " +
                                        "subnet response is wrong")

    def test_get(self):
        original_method = self.fetcher.get_networks
        self.fetcher.get_networks = MagicMock(return_value=NETWORKS_RESULT)
        result = self.fetcher.get(REGION_NAME)

        self.fetcher.get_networks = original_method
        self.assertEqual(result, NETWORKS_RESULT, "Can't get region networks info")

    def test_get_with_wrong_token(self):
        self.fetcher.v2_auth_pwd = MagicMock(return_value=None)
        result = self.fetcher.get(REGION_NAME)
        self.fetcher.v2_auth_pwd = MagicMock(return_value=TOKEN)
        self.assertEqual(result, [], "Can't get [] when the " +
                                     "token is invalid")
