###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import patch, MagicMock

from base.utils.mongo_access import MongoAccess
from scan.fetchers.kube.kube_fetch_vnics_vpp import KubeFetchVnicsVpp
from scan.test.fetch.kube_fetch.test_data.kube_fetch_vnics_vpp import HOST_DOC, \
    EXPECTED_VNIC, run_fetch_lines_mock
from scan.test.fetch.logger_patcher import LoggerPatcher


class TestKubeFetchVnicsVpp(LoggerPatcher):

    def setUp(self):
        super().setUp()

        self.inv_patcher = patch(
            'discover.fetchers.kube.kube_fetch_vnics_vpp.InventoryMgr'
        )
        self.inv_class = self.inv_patcher.start()
        self.inv = self.inv_class.return_value

        self.old_mongo_connect = MongoAccess.mongo_connect
        MongoAccess.mongo_connect = MagicMock()

        self.fetcher = KubeFetchVnicsVpp()

    def test_get(self):
        self.inv.get_by_id.return_value = HOST_DOC
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        if_details_fetcher_run_fetch_lines = \
            self.fetcher.if_details_fetcher.run_fetch_lines
        self.fetcher.run_fetch_lines = run_fetch_lines_mock
        self.fetcher.if_details_fetcher.run_fetch_lines = run_fetch_lines_mock
        vnics = self.fetcher.get(HOST_DOC['id'])
        self.assertEqual(1, len(vnics))
        self.assertDictContains(EXPECTED_VNIC, vnics[0])
        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.fetcher.if_details_fetcher.run_fetch_lines = \
            if_details_fetcher_run_fetch_lines

    def tearDown(self):
        MongoAccess.mongo_connect = self.old_mongo_connect
        self.inv_patcher.stop()
        super().tearDown()
