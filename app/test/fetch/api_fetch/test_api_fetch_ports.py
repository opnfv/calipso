from discover.fetchers.api.api_fetch_ports import ApiFetchPorts
from test.fetch.test_fetch import TestFetch
from test.fetch.api_fetch.test_data.api_fetch_ports import *
from test.fetch.api_fetch.test_data.token import TOKEN
from unittest.mock import MagicMock


class TestApiFetchPorts(TestFetch):

    def setUp(self):
        self.configure_environment()
        ApiFetchPorts.v2_auth_pwd = MagicMock(return_value=TOKEN)
        self.fetcher = ApiFetchPorts()
        self.set_regions_for_fetcher(self.fetcher)

    def check_get_ports_for_region_result_is_correct(self, network,
                                                     tenant,
                                                     port_response,
                                                     expected_result,
                                                     error_msg):
        self.fetcher.get_region_url = MagicMock(return_value=ENDPOINT)
        self.fetcher.get_url = MagicMock(return_value=port_response)
        self.fetcher.inv.get_by_id = MagicMock(side_effect=[network, tenant])

        result = self.fetcher.get_ports_for_region(REGION_NAME, TOKEN)
        self.assertEqual(result, expected_result, error_msg)

    def test_get_ports_for_region(self):
        test_cases = [
            {
                "network": NETWORK,
                "tenant": None,
                "port_response": PORTS_RESPONSE,
                "expected_result": PORTS_RESULT_WITH_NET,
                "error_msg": "Can't get correct ports info "
                             "when network of the port exists"
            },
            {
                "network": None,
                "tenant": None,
                "port_response": PORTS_RESPONSE,
                "expected_result": PORTS_RESULT_WITHOUT_NET,
                "error_msg": "Can't get correct ports info "
                             "when network of the port doesn't exists"
            },
            {
                "network": NETWORK,
                "tenant": TENANT,
                "port_response": PORTS_RESPONSE,
                "expected_result": PORTS_RESULT_WITH_PROJECT,
                "error_msg": "Can't get correct ports info "
                             "when project of the port exists"
            },
            {
                "network": None,
                "tenant": None,
                "port_response": ERROR_PORTS_RESPONSE,
                "expected_result": [],
                "error_msg": "Can't get [] when ports response is wrong"
            },
        ]
        for test_case in test_cases:
            self.check_get_ports_for_region_result_is_correct(test_case["network"],
                                                              test_case["tenant"],
                                                              test_case["port_response"],
                                                              test_case["expected_result"],
                                                              test_case["error_msg"])

    def test_get(self):
        original_method = self.fetcher.get_ports_for_region
        self.fetcher.get_ports_for_region = MagicMock(return_value=PORTS_RESULT_WITH_NET)
        result = self.fetcher.get(REGION_NAME)
        self.fetcher.get_ports_for_region = original_method
        self.assertEqual(result, PORTS_RESULT_WITH_NET, "Can't get correct ports info")

    def test_get_with_wrong_token(self):
        self.fetcher.v2_auth_pwd = MagicMock(return_value=None)
        result = self.fetcher.get(REGION_NAME)
        self.fetcher.v2_auth_pwd = MagicMock(return_value=TOKEN)
        self.assertEqual(result, [], "Can't get [] when the token is invalid")
