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

import copy

from scan.fetchers.cli.cli_fetch_interface_details \
    import CliFetchInterfaceDetails
from scan.test.fetch.cli_fetch.test_data.cli_fetch_interface_details import *
from scan.test.fetch.test_fetch import TestFetch


class TestCliFetchInterfaceDetails(TestFetch):

    def setUp(self):
        super().setUp()
        self.configure_environment()
        self.fetcher = CliFetchInterfaceDetails()
        self.fetcher.set_env(self.env)

    def test_get_interface_details(self):
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        original_handle_line = self.fetcher.handle_line
        original_set_interface_data = self.fetcher.set_interface_data

        self.fetcher.run_fetch_lines = MagicMock()
        self.fetcher.handle_line = MagicMock()
        self.fetcher.set_interface_data = MagicMock()

        result = self.fetcher.get_interface_details(HOST_ID, INTERFACE_NAME,
                                                    IFCONFIG_CM_RESULT)

        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.fetcher.handle_line = original_handle_line
        self.fetcher.set_interface_data = original_set_interface_data

        self.assertEqual(result, INTERFACE_DETAILS,
                         "Can't get interface details")

    def test_handle_mac_address_line(self):
        interface = copy.deepcopy(RAW_INTERFACE)
        self.fetcher.handle_line(interface, MAC_ADDRESS_LINE)
        self.assertEqual(interface["mac_address"], MAC_ADDRESS,
                         "Can't get the correct MAC address")

    # Test failed, defect, result: addr:
    # expected result: fe80::f816:3eff:fea1:eb73/64
    def test_handle_ipv6_address_line(self):
        interface = copy.deepcopy(RAW_INTERFACE)
        self.fetcher.handle_line(interface, IPV6_ADDRESS_LINE)
        self.assertEqual(interface['IPv6 Address'], IPV6_ADDRESS,
                         "Can't get the correct ipv6 address")

    def test_handle_ipv4_address_line(self):
        interface = copy.deepcopy(RAW_INTERFACE)
        self.fetcher.handle_line(interface, IPV4_ADDRESS_LINE)
        self.assertEqual(interface['IP Address'], IPV4_ADDRESS,
                         "Can't get the correct ipv4 address")

    def test_set_interface_data(self):
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        self.fetcher.run_fetch_lines = MagicMock(return_value=ETHTOOL_RESULT)
        self.fetcher.set_interface_data(INTERFACE_FOR_SET)
        self.assertEqual(INTERFACE_FOR_SET, INTERFACE_AFTER_SET,
                         "Can't get the attributes of the "
                         "interface from the CMD result")

        self.fetcher.run_fetch_lines = original_run_fetch_lines
