###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import copy

from discover.fetchers.db.db_fetch_oteps import DbFetchOteps
from test.fetch.test_fetch import TestFetch
from test.fetch.db_fetch.test_data.db_fetch_oteps import *
from unittest.mock import MagicMock


class TestDbFetchOteps(TestFetch):

    def setUp(self):
        super().setUp()
        self.configure_environment()
        self.fetcher = DbFetchOteps()
        self.fetcher.set_env(self.env)

    def check_get_oteps_results(self, vedge,
                                config,
                                host,
                                oteps_from_db,
                                expected_results,
                                err_msg):
        original_get_vconnector = self.fetcher.get_vconnector
        self.fetcher.get_vconnector = MagicMock()
        self.fetcher.inv.get_by_id = MagicMock(side_effect=[vedge, host])
        original_get_env_config = self.fetcher.config.get_env_config
        self.fetcher.config.get_env_config = MagicMock(return_value=config)
        self.fetcher.get_objects_list_for_id = MagicMock(return_value=oteps_from_db)
        results = self.fetcher.get(VEDGE_ID)
        self.assertEqual(results, expected_results, err_msg)
        self.fetcher.get_vconnector = original_get_vconnector
        self.fetcher.config.get_env_config = original_get_env_config

    def test_get(self):
        test_cases = [
            {
                "vedge": VEDGE_WITHOUT_CONFIGS,
                "config": NON_ICEHOUSE_CONFIGS,
                "host": None,
                "oteps_from_db": None,
                "expected_results": [],
                "err_msg": "Can't get [] when the vedge " +
                           "doesn't contains configurations"
            },
            {
                "vedge": VEDGE_WITHOUT_TUNNEL_TYPES,
                "config": NON_ICEHOUSE_CONFIGS,
                "host": None,
                "oteps_from_db": None,
                "expected_results": [],
                "err_msg": "Can't get [] when the vedge configurations " +
                           "doesn't contain tunnel_types"
            },
            {
                "vedge": VEDGE,
                "config": ICEHOUSE_CONFIGS,
                "host": HOST,
                "oteps_from_db": None,
                "expected_results": OTEPS_FOR_ICEHOUSE_DISTRIBUTION_RESULTS,
                "err_msg": "Can't get correct oteps result " +
                           "when the distribution is icehouse"
            },
            {
                "vedge": VEDGE,
                "config": NON_ICEHOUSE_CONFIGS,
                "host": None,
                "oteps_from_db": OTEPS,
                "expected_results": OTEPS_FOR_NON_ICEHOUSE_DISTRIBUTION_RESULTS,
                "err_msg": "Can't get correct oteps result " +
                           "when the distribution is not icehouse"
            }
        ]
        for test_case in test_cases:
            self.check_get_oteps_results(test_case["vedge"],
                                         test_case["config"],
                                         test_case["host"],
                                         test_case["oteps_from_db"],
                                         test_case["expected_results"],
                                         test_case["err_msg"])

    def test_get_vconnectors(self):
        self.fetcher.run_fetch_lines = \
            MagicMock(return_value=IP_ADDRESS_SHOW_LINES)
        otep_to_get_vconnector = copy.deepcopy(OTEP_FOR_GETTING_VECONNECTOR)
        self.fetcher.get_vconnector(otep_to_get_vconnector,
                                    HOST_ID, VEDGE)
        self.assertEqual(otep_to_get_vconnector, OTEP_WITH_CONNECTOR,
                         "Can't get vconnector from the config lines for otep")
