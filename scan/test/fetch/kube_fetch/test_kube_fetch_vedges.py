###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import patch

from scan.fetchers.kube.kube_fetch_vedges import KubeFetchVedges
from scan.test.fetch.kube_fetch.test_data.kube_access import HOST_DOC
from scan.test.fetch.kube_fetch.test_data.kube_fetch_vedges import PODS_LIST, \
    EXPECTED_VEDGE
from scan.test.fetch.logger_patcher import LoggerPatcher


class TestKubeFetchVedges(LoggerPatcher):

    def setUp(self):
        super().setUp()

        self.inv_patcher = patch(
            'discover.fetchers.kube.kube_fetch_vedges.InventoryMgr'
        )
        self.inv_class = self.inv_patcher.start()
        self.inv = self.inv_class.return_value

        self.fetcher = KubeFetchVedges()

    def test_get(self):
        self.inv.get_by_id.return_value = HOST_DOC
        self.inv.find_items.return_value = PODS_LIST
        vedges = self.fetcher.get(HOST_DOC['id'])
        self.assertEqual(1, len(vedges))
        self.assertDictContains(EXPECTED_VEDGE, vedges[0])

    def test_get_no_host(self):
        self.inv.get_by_id.return_value = None
        vedges = self.fetcher.get(HOST_DOC['id'])
        self.assertEqual(0, len(vedges))

    def tearDown(self):
        self.inv_patcher.stop()
        super().tearDown()
