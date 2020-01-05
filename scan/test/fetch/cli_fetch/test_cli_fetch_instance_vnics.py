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

from scan.fetchers.cli.cli_fetch_instance_vnics import CliFetchInstanceVnics
from scan.test.fetch.cli_fetch.test_data.cli_fetch_instance_vnics import *
from scan.test.fetch.test_fetch import TestFetch


class TestCliFetchInstanceVnics(TestFetch):

    def setUp(self):
        super().setUp()
        self.configure_environment()
        self.fetcher = CliFetchInstanceVnics()
        self.fetcher.set_env(self.env)

    def test_get(self):
        # store original methods
        original_get_by_id = self.fetcher.inv.get_by_id
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        original_get_vnics_from_dumpxml = self.fetcher.get_vnics_from_dumpxml

        # mock methods
        self.fetcher.inv.get_by_id = MagicMock(side_effect=[INSATNCE, COMPUTE_HOST])
        self.fetcher.run_fetch_lines = MagicMock(return_value=INSTANCES_LIST)
        self.fetcher.get_vnics_from_dumpxml = MagicMock(return_value=VNICS_FROM_DUMP_XML)

        result = self.fetcher.get(VNICS_FOLDER['id'])

        # reset methods
        self.fetcher.inv.get_by_id = original_get_by_id
        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.fetcher.get_vnics_from_dumpxml = original_get_vnics_from_dumpxml

        self.assertNotEqual(result, [], "Can't get vnics with VNICS folder id")

    def test_get_without_instance(self):
        # store original methods
        original_get_by_id = self.fetcher.inv.get_by_id

        # mock methods
        self.fetcher.inv.get_by_id = MagicMock(return_value=[])

        result = self.fetcher.get(VNICS_FOLDER['id'])

        # reset methods
        self.fetcher.inv.get_by_id = original_get_by_id

        self.assertEqual(result, [], "Can't get empty array when the instance can't be found")

    def test_get_without_host(self):
        # store original methods
        original_get_by_id = self.fetcher.inv.get_by_id

        # mock methods
        self.fetcher.inv.get_by_id = MagicMock(side_effect=[[], NETWORK_HOST])

        result = self.fetcher.get(VNICS_FOLDER['id'])

        # reset methods
        self.fetcher.inv.get_by_id = original_get_by_id

        self.assertEqual(result, [], "Can't get empty array when the host doesn't contain network host type")

    def test_get_vnics_from_dumpxml(self):
        # store original functions
        original_run = self.fetcher.run
        original_set_vnic_properties = self.fetcher.set_vnic_properties

        # mock the functions
        self.fetcher.run = MagicMock(return_value=DUMPXML)
        self.fetcher.set_vnic_properties = MagicMock()

        vnics = self.fetcher.get_vnics_from_dumpxml(ID, INSATNCE)
        # reset functions
        self.fetcher.run = original_run
        self.fetcher.set_vnic_properties = original_set_vnic_properties

        self.assertNotEqual(vnics, [], "Can't get vnics")

    def test_get_vnics_from_dumpxml_with_empty_command_result(self):
        # store original functions
        original_run = self.fetcher.run

        # mock the functions
        self.fetcher.run = MagicMock(return_value="  ")

        vnics = self.fetcher.get_vnics_from_dumpxml(ID, INSATNCE)
        # reset functions
        self.fetcher.run = original_run

        self.assertEqual(vnics, [], "Can't get empty array when the dumpxml is empty")

    def test_get_vnics_from_dumpxml_with_wrong_instance(self):
        # store original functions
        original_run = self.fetcher.run

        # mock the functions
        self.fetcher.run = MagicMock(return_value=WRONG_DUMPXML)

        vnics = self.fetcher.get_vnics_from_dumpxml(ID, INSATNCE)
        # reset functions
        self.fetcher.run = original_run

        self.assertEqual(vnics, [], "Can't get empty array when the instance is wrong")