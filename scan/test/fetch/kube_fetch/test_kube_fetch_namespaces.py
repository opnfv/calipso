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

from scan.fetchers.kube.kube_fetch_namespaces import KubeFetchNamespaces
from scan.test.fetch.kube_fetch.kube_test_base import KubeTestBase
from scan.test.fetch.kube_fetch.test_data.kube_access import KUBE_CONFIG
from scan.test.fetch.kube_fetch.test_data.kube_fetch_namespaces import \
    NAMESPACES_RESPONSE, EMPTY_RESPONSE, EXPECTED_NAMESPACES


class TestKubeFetchNamespaces(KubeTestBase):

    def setUp(self):
        super().setUp()
        self.fetcher = KubeFetchNamespaces(KUBE_CONFIG)

    def test_get(self):
        response = self._get_response(payload=NAMESPACES_RESPONSE,
                                      response_type='V1NamespaceList')
        self.api.list_namespace = MagicMock(return_value=response)
        namespaces = self.fetcher.get(None)
        self.assertEqual(3, len(namespaces))
        self.assertListsContain(EXPECTED_NAMESPACES, namespaces)

    def test_get_no_namespaces(self):
        response = self._get_response(payload=EMPTY_RESPONSE,
                                      response_type='V1NamespaceList')
        self.api.list_namespace = MagicMock(return_value=response)
        namespaces = self.fetcher.get(None)
        self.assertEqual(0, len(namespaces))
