from discover.fetchers.db.db_fetch_aggregate_hosts import DbFetchAggregateHosts
from test.fetch.test_fetch import TestFetch
from test.fetch.db_fetch.test_data.db_fetch_aggregate_hosts import *
from unittest.mock import MagicMock


class TestDbFetchAggregateHosts(TestFetch):

    def setUp(self):
        self.configure_environment()
        self.fetcher = DbFetchAggregateHosts()

    def check_get_results_is_correct(self,
                                     objects_list,
                                     host_in_inventory,
                                     expected_result,
                                     err_msg):
        self.fetcher.get_objects_list_for_id = MagicMock(return_value=objects_list)
        self.inv.get_by_id = MagicMock(return_value=host_in_inventory)
        result = self.fetcher.get(AGGREGATE["id"])

        self.assertEqual(result, expected_result, err_msg)

    def test_get(self):
        test_cases = [
            {
                "objects_list": HOSTS,
                "host_in_inventory": HOST_IN_INVENTORY,
                "expected_result": HOSTS_RESULT,
                "err_msg": "Can't get correct hosts info"
            },
            {
                "objects_list": [],
                "host_in_inventory": None,
                "expected_result": [],
                "err_msg": "Can't get [] when the "
                           "returned objects list is empty"
            },
            {
                "objects_list": HOSTS,
                "host_in_inventory": [],
                "expected_result": HOSTS,
                "err_msg": "Can't get correct hosts info "
                           "when the host doesn't exist in the inventory"
            }
        ]
        for test_case in test_cases:
            self.check_get_results_is_correct(test_case["objects_list"],
                                              test_case["host_in_inventory"],
                                              test_case["expected_result"],
                                              test_case["err_msg"])
