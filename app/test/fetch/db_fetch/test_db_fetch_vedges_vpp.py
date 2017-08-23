###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.db.db_fetch_vedges_vpp import DbFetchVedgesVpp
from test.fetch.test_fetch import TestFetch
from test.fetch.db_fetch.test_data.db_fetch_vedges_vpp import *
from unittest.mock import MagicMock


class TestDbFetchVedgesVpp(TestFetch):

    def setUp(self):
        super().setUp()
        self.configure_environment()
        self.fetcher = DbFetchVedgesVpp()
        self.fetcher.set_env(self.env)

    def check_get_results(self, version,
                          interfaces, host,
                          expected_results, err_msg):
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        original_get_by_id = self.fetcher.inv.get_by_id

        self.fetcher.run_fetch_lines = MagicMock(side_effect=[version, interfaces])
        self.fetcher.inv.get_by_id = MagicMock(return_value=host)

        vedges = self.fetcher.get(VEDGE_FOLDER_ID)
        self.assertEqual(vedges, expected_results, err_msg)

        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.fetcher.inv.get_by_id = original_get_by_id

    def test_get(self):
        test_cases = [
            {
                "version": VERSION,
                "interfaces": INTERFACES,
                "host": HOST,
                "expected_results": VEDGE_RESULTS,
                "err_msg": "Can' get correct vedges"
            },
            {
                "version": [],
                "interfaces": INTERFACES,
                "host": HOST,
                "expected_results": VEDGE_RESULTS_WITHOUT_BINARY,
                "err_msg": "Can' get correct vedges when " +
                           "it can't get version info host"
            },
            {
                "version": VERSION,
                "interfaces": INTERFACES,
                "host": [],
                "expected_results": [],
                "err_msg": "Can't get [] when the host of the " +
                           "vedge doesn't exist in db"
            },
            {
                "version": VERSION,
                "interfaces": INTERFACES,
                "host": HOST_WITHOUT_REQUIRED_HOST_TYPE,
                "expected_results": [],
                "err_msg": "Can't get [] when the host of the " +
                           "vedge doesn't contains required host types"
            }
        ]

        for test_case in test_cases:
            self.check_get_results(test_case["version"],
                                   test_case["interfaces"],
                                   test_case["host"],
                                   test_case["expected_results"],
                                   test_case["err_msg"])

    def test_fetch_ports(self):
        ports = self.fetcher.fetch_ports(INTERFACES)
        self.assertEqual(ports, PORTS, "Can't get the correct ports info")