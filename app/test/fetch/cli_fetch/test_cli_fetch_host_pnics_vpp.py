###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.cli.cli_fetch_host_pnics_vpp import CliFetchHostPnicsVpp
from test.fetch.test_fetch import TestFetch
from unittest.mock import MagicMock
from test.fetch.cli_fetch.test_data.cli_fetch_host_pnics_vpp import *


class TestCliFetchHostPnicsVpp(TestFetch):

    def setUp(self):
        self.configure_environment()
        self.fetcher = CliFetchHostPnicsVpp()
        self.fetcher.set_env(self.env)

    def test_get(self):
        # store original method
        original_find_items = self.fetcher.inv.find_items

        # mock the method
        self.fetcher.inv.find_items = MagicMock(return_value=VEDGES)

        result = self.fetcher.get(ID)
        # reset the method
        self.fetcher.inv.find_items = original_find_items

        self.assertNotEqual(result, [], "Can't get the pnics info")