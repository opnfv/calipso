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

from scan.fetchers.kube.kube_fetch_vnics_flannel \
    import KubeFetchVnicsFlannel
from scan.test.fetch.kube_fetch.test_data.kube_fetch_vnics_flannel import HOST_DOC, \
    EXPECTED_VNIC
from scan.test.fetch.logger_patcher import LoggerPatcher


class TestKubeFetchVnicsFlannel(LoggerPatcher):

    def setUp(self):
        super().setUp()

        self.inv_patcher = patch(
            'discover.fetchers.kube.kube_fetch_vnics_flannel.InventoryMgr'
        )
        self.inv_class = self.inv_patcher.start()
        self.inv = self.inv_class.return_value

        self.fetcher = KubeFetchVnicsFlannel()

    def test_get(self):
        self.inv.get_by_id.return_value = HOST_DOC
        vnics = self.fetcher.get(HOST_DOC['id'])
        self.assertEqual(1, len(vnics))
        self.assertDictContains(EXPECTED_VNIC, vnics[0])

    def tearDown(self):
        self.inv_patcher.stop()
        super().tearDown()
