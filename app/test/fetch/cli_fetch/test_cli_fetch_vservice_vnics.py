###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.cli.cli_fetch_vservice_vnics import CliFetchVserviceVnics
from test.fetch.test_fetch import TestFetch
from test.fetch.cli_fetch.test_data.cli_fetch_vservice_vnics import *
from unittest.mock import MagicMock


class TestCliFetchVserviceVnics(TestFetch):

    def setUp(self):
        self.configure_environment()
        self.fetcher = CliFetchVserviceVnics()
        self.fetcher.set_env(self.env)

    def test_get(self):
        # store original methods
        original_get_by_id = self.fetcher.inv.get_by_id
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        original_handle_service = self.fetcher.handle_service
        # mock methods
        self.fetcher.inv.get_by_id = MagicMock(return_value=NETWORK_NODE)
        self.fetcher.run_fetch_lines = MagicMock(return_value=NAME_SPACES)
        self.fetcher.handle_service = MagicMock(return_value=SERVICES)

        result = self.fetcher.get(NETWORK_NODE['id'])

        # reset methods
        self.fetcher.inv.get_by_id = original_get_by_id
        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.fetcher.handle_service = original_handle_service

        self.assertNotEqual(result, [], "Can't get vnics")

    def test_get_with_error_host(self):
        # store original methods
        original_get_by_id = self.fetcher.inv.get_by_id

        # mock methods
        self.fetcher.inv.get_by_id = MagicMock(return_value=ERROR_NODE)

        result = self.fetcher.get(NETWORK_NODE['id'])

        # reset methods
        self.fetcher.inv.get_by_id = original_get_by_id

        self.assertEqual(result, [], "Can't get empty array when the host doesn't contain host_type")

    def test_get_with_compute_host(self):
        # store original methods
        original_get_by_id = self.fetcher.inv.get_by_id

        # mock methods
        self.fetcher.inv.get_by_id = MagicMock(return_value=COMPUTE_NODE)

        result = self.fetcher.get(NETWORK_NODE['id'])

        # reset methods
        self.fetcher.inv.get_by_id = original_get_by_id

        self.assertEqual(result, [], "Can't get empty array when the host type doesn't contain network")

    def test_handle_service(self):
        # store original method
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        original_set_interface_data = self.fetcher.set_interface_data
        # mock the method
        self.fetcher.run_fetch_lines = MagicMock(return_value=IFCONFIG_RESULT)
        self.fetcher.set_interface_data = MagicMock()
        result = self.fetcher.handle_service(NETWORK_NODE['id'], SERVICE_ID)
        # reset method
        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.fetcher.set_interface_data = original_set_interface_data

        self.assertNotEqual(result, [], "Can't get interfaces data")

    def test_set_interface_data(self):
        # store original methods
        original_get_by_field = self.fetcher.inv.get_by_field
        original_get_by_id = self.fetcher.inv.get_by_id
        original_set = self.fetcher.inv.set

        # mock the methods
        self.fetcher.inv.get_by_field = MagicMock(return_value=NETWORK)
        self.fetcher.inv.get_by_id = MagicMock(return_value=VSERVICE)
        self.fetcher.inv.set = MagicMock()

        self.fetcher.set_interface_data(VNIC)

        # reset methods
        self.fetcher.inv.get_by_field = original_get_by_field
        self.fetcher.inv.get_by_id = original_get_by_id
        self.fetcher.inv.set = original_set

        self.assertIn("data", VNIC, "Can't set data")
        self.assertIn("cidr", VNIC, "Can't set cidr")
        self.assertIn("network", VNIC, "Can't set network")

    def test_handle_mac_address_line(self):
        self.fetcher.handle_line(RAW_VNIC, MAC_ADDRESS_LINE)
        self.assertEqual(RAW_VNIC['mac_address'], MAC_ADDRESS, "Can't get the correct mac address from the line")

    def test_handle_ipv4_address_line(self):
        self.fetcher.handle_line(RAW_VNIC, IPV4_ADDRESS_LINE)
        self.assertEqual(RAW_VNIC['IP Address'], IPV4_ADDRESS, "Can't get the correct ipv4 address from the line")

    def test_handle_ipv6_address_line(self):
        self.fetcher.handle_line(RAW_VNIC, IPV6_ADDRESS_LINE)
        self.assertEqual(RAW_VNIC['IPv6 Address'], IPV6_ADDRESS, "Can't get the correct ipv6 address from the line")

    def test_get_net_size(self):
        size = self.fetcher.get_net_size(NET_MASK_ARRAY)
        self.assertEqual(size, SIZE, "Can't get the size of network by netmask")

    def test_get_cidr_for_vnic(self):
        cidr = self.fetcher.get_cidr_for_vnic(VNIC)
        self.assertEqual(cidr, CIDR, "the cidr info is wrong")
