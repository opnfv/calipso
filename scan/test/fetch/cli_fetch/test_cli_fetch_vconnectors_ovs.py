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

from scan.fetchers.cli.cli_fetch_vconnectors_ovs import CliFetchVconnectorsOvs
from scan.test.fetch.cli_fetch.test_data.cli_fetch_vconnectors_ovs import *
from scan.test.fetch.test_fetch import TestFetch


class TestCliFetchVconnectorsOvs(TestFetch):

    def setUp(self):
        super().setUp()
        self.configure_environment()
        self.fetcher = CliFetchVconnectorsOvs()
        self.fetcher.set_env(self.env)

    def test_get_vconnectors(self):
        # store the original methods
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        original_find_items = self.fetcher.inv.find_items

        # mock the methods
        self.fetcher.run_fetch_lines = MagicMock(return_value=BRIDGE_RESULT)
        self.fetcher.inv.find_items = MagicMock(return_value=[])

        result = self.fetcher.get_vconnectors(NETWORK_NODE)

        # reset methods
        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.fetcher.inv.find_items = original_find_items

        self.assertNotEqual(result, [], "Can't get vconnectors with the host id")
