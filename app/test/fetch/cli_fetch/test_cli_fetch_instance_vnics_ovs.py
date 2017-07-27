###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.cli_fetch_instance_vnics_ovs import CliFetchInstanceVnicsOvs
from test.fetch.test_fetch import TestFetch
from test.fetch.cli_fetch.test_data.cli_fetch_instance_vnics import *
from unittest.mock import MagicMock


class TestCliFetchInstanceVnicsOvs(TestFetch):

    def setUp(self):
        self.configure_environment()
        self.fetcher = CliFetchInstanceVnicsOvs()
        self.fetcher.set_env(self.env)

    def test_set_vnic_properties(self):
        # store original method
        original_set = self.fetcher.inv.set
        self.fetcher.inv.set = MagicMock()

        self.fetcher.set_vnic_properties(VNIC, INSATNCE)
        # reset method
        self.fetcher.inv.set = original_set

        self.assertIn("source_bridge", VNIC, "Can't set source_bridge for ovs vnic")

    def test_get_vnic_name(self):
        name = self.fetcher.get_vnic_name(VNIC, INSATNCE)
        self.assertNotEqual(name, None, "Can't get vnic name")