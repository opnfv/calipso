###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.cli.cli_fetch_vconnectors_ovs import CliFetchVconnectorsOvs
from test.fetch.test_fetch import TestFetch
from test.fetch.cli_fetch.test_data.cli_fetch_vconnectors_ovs import *
from unittest.mock import MagicMock


class TestCliFetchVconnectorsOvs(TestFetch):

    def setUp(self):
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
