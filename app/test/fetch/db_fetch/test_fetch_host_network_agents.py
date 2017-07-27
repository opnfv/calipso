import copy

from discover.fetchers.db.db_fetch_host_network_agents import DbFetchHostNetworkAgents
from test.fetch.test_fetch import TestFetch
from test.fetch.db_fetch.test_data.db_fetch_host_network_agents import *
from unittest.mock import MagicMock


class TestFetchHostNetworkAgents(TestFetch):

    def setUp(self):
        self.configure_environment()
        self.fetcher = DbFetchHostNetworkAgents()

    def check_get_result(self,
                         config,
                         network_agent_res,
                         expected_result,
                         err_msg):
        self.fetcher.env_config = config
        self.fetcher.get_objects_list_for_id =\
            MagicMock(return_value=network_agent_res)
        result = self.fetcher.get(NETWORK_AGENT_FOLDER_ID)
        self.assertEqual(result, expected_result, err_msg)

    def test_get(self):
        test_cases = [
            {
                'config': CONFIG_WITH_MECHANISM_DRIVERS,
                'network_agent_res': copy.deepcopy(NETWORK_AGENT),
                'expected_result':
                    NETWORK_AGENT_WITH_MECHANISM_DRIVERS_IN_CONFIG_RESULTS,
                'err_msg': "Can't get correct result when the " +
                           "mechanism drivers exists in the config"
            },
            {
                'config': CONFIG_WITHOUT_MECHANISM_DRIVERS,
                'network_agent_res': copy.deepcopy(NETWORK_AGENT),
                'expected_result':
                    NETWORK_AGENT_WITHOUT_MECHANISM_DRIVERS_IN_CONFIG_RESULTS,
                'err_msg': "Can't get correct result when the " +
                           "mechanism drivers doesn't exist in the config"
            },
            {
                'config': CONFIG_WITH_MECHANISM_DRIVERS,
                'network_agent_res': [],
                'expected_result': [],
                'err_msg': "Can't get [] when the network agent result " +
                           "is empty"
            }
        ]

        for test_case in test_cases:
            self.check_get_result(test_case['config'],
                                  test_case['network_agent_res'],
                                  test_case['expected_result'],
                                  test_case['err_msg'])
