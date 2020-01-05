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

from scan.fetchers.kube.kube_fetch_pods import KubeFetchPods
from scan.test.fetch.kube_fetch.kube_test_base import KubeTestBase
from scan.test.fetch.kube_fetch.test_data.kube_access import KUBE_CONFIG, HOST_DOC
from scan.test.fetch.kube_fetch.test_data.kube_fetch_pods import PODS_RESPONSE, \
    NAMESPACE_DOC, EXPECTED_POD


class TestKubeFetchPods(KubeTestBase):

    def setUp(self):
        super().setUp()
        self.fetcher = KubeFetchPods(KUBE_CONFIG)

    def test_get(self):
        self.inv.get_by_id.return_value = HOST_DOC
        self.inv.find_one.return_value = NAMESPACE_DOC
        response = self._get_response(payload=PODS_RESPONSE,
                                      response_type='V1PodList')

        self.api.list_pod_for_all_namespaces = MagicMock(return_value=response)
        pods = self.fetcher.get(HOST_DOC['id'])
        self.assertEqual(1, len(pods))
        self.assertDictContains(EXPECTED_POD, pods[0])

    def test_get_no_host(self):
        self.inv.get_by_id.return_value = None
        pods = self.fetcher.get('wrong_host')
        self.assertEqual(0, len(pods))

    def test_get_no_namespace(self):
        self.inv.get_by_id.return_value = HOST_DOC
        self.inv.find_one.return_value = None
        response = self._get_response(payload=PODS_RESPONSE,
                                      response_type='V1PodList')

        self.api.list_pod_for_all_namespaces = MagicMock(return_value=response)
        pods = self.fetcher.get(HOST_DOC['id'])
        self.assertEqual(1, len(pods))
