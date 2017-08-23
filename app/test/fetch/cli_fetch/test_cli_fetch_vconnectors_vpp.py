###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.cli.cli_fetch_vconnectors_vpp import CliFetchVconnectorsVpp
from test.fetch.test_fetch import TestFetch
from unittest.mock import MagicMock
from test.fetch.cli_fetch.test_data.cli_fetch_vconnectors_vpp import *


class TestCliFetchVconnectorsVpp(TestFetch):

    def setUp(self):
        super().setUp()
        self.configure_environment()
        self.fetcher = CliFetchVconnectorsVpp()
        self.fetcher.set_env(self.env)

    def test_get_vconnectors(self):
        # store original method
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        original_get_interface_details = self.fetcher.get_interface_details

        # mock methods
        self.fetcher.run_fetch_lines = MagicMock(return_value=MODE_RESULT)
        self.fetcher.get_interface_details = MagicMock(return_value=None)

        result = self.fetcher.get_vconnectors(HOST)

        # reset methods
        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.fetcher.get_interface_details = original_get_interface_details

        self.assertNotEqual(result, {}, "Can't get vconnectors info")

    def test_set_interface_details(self):
        # store original methods
        original_run_fetch_lines = self.fetcher.run_fetch_lines

        # mock method
        self.fetcher.run_fetch_lines = MagicMock(return_value=INTERFACE_LINES)

        result = self.fetcher.get_interface_details(HOST, INTERFACE_NAME)
        # restore method
        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.assertNotEqual(result, None, "Can't get the interface details")