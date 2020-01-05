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

from scan.fetchers.kube.kube_fetch_oteps_flannel \
    import KubeFetchOtepsFlannel
from scan.test.fetch.kube_fetch.test_data.kube_fetch_oteps_flannel \
    import HOST_DOC, OTEPS_PARENT, OTEPS_LIST, EXPECTED_OTEP
from scan.test.fetch.logger_patcher import LoggerPatcher


class TestKubeFetchOtepsFlannel(LoggerPatcher):

    def setUp(self):
        super().setUp()

        self.inv_patcher = patch(
            'discover.fetchers.kube.kube_fetch_oteps_flannel.InventoryMgr'
        )
        self.inv_class = self.inv_patcher.start()
        self.inv = self.inv_class.return_value

        self.fetcher = KubeFetchOtepsFlannel()

    def test_get(self):
        self.inv.get_by_id.return_value = HOST_DOC
        self.inv.get_by_field.return_value = OTEPS_LIST
        oteps = self.fetcher.get(OTEPS_PARENT)
        self.assertEqual(1, len(oteps))
        self.assertDictContains(EXPECTED_OTEP, oteps[0])

    def test_get_no_vedge(self):
        self.inv.get_by_id.return_value = None
        oteps = self.fetcher.get('wrong_folder')
        self.assertEqual(0, len(oteps))

    def tearDown(self):
        self.inv_patcher.stop()
        super().tearDown()
