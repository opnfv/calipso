###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import MagicMock, patch

from scan.fetchers.kube.kube_fetch_containers import KubeFetchContainers
from scan.test.fetch.kube_fetch.kube_test_base import KubeTestBase
from scan.test.fetch.kube_fetch.test_data.kube_access import KUBE_CONFIG
from scan.test.fetch.kube_fetch.test_data.kube_fetch_containers import \
    POD_DOCUMENT, CONTAINERS_FOLDER_ID, PODS_RESPONSE_NO_MATCH, \
    EXPECTED_CONTAINER_DOC
from scan.test.fetch.kube_fetch.test_data.kube_fetch_pods import PODS_RESPONSE, \
    EMPTY_RESPONSE


class TestKubeFetchContainers(KubeTestBase):

    class DummyConfig(object):
        def __init__(self, _environment):
            self.environment = _environment

    def setUp(self):
        super().setUp()

        self.conf_patcher = patch(
            'utils.cli_access.Configuration'
        )
        self.conf_class = self.conf_patcher.start()

        self.fetcher = KubeFetchContainers(KUBE_CONFIG)
        self.fetcher.configuration = TestKubeFetchContainers.DummyConfig({
            'environment_type': 'Kubernetes'
        })

    @staticmethod
    def _get_by_id(environment, item_id):
        if environment:
            pass
        if item_id == POD_DOCUMENT['id']:
            return POD_DOCUMENT
        return None

    def test_get_flannel(self):
        self.fetcher.configuration.environment['mechanism_drivers'] = \
            ['Flannel']
        self.inv.get_by_id.side_effect = self._get_by_id
        self.fetcher.run = MagicMock(return_value="[]")
        response = self._get_response(payload=PODS_RESPONSE,
                                      response_type='V1PodList')
        self.api.list_pod_for_all_namespaces = MagicMock(return_value=response)

        containers = self.fetcher.get(CONTAINERS_FOLDER_ID)
        self.assertEqual(1, len(containers))
        self.assertDictContains(EXPECTED_CONTAINER_DOC, containers[0])

    def test_get_no_db_pod(self):
        self.inv.get_by_id.return_value = None
        containers = self.fetcher.get(CONTAINERS_FOLDER_ID)
        self.assertEqual(0, len(containers))

    def test_get_no_kube_pods(self):
        self.inv.get_by_id.side_effect = self._get_by_id
        response = self._get_response(payload=EMPTY_RESPONSE,
                                      response_type='V1PodList')
        self.api.list_pod_for_all_namespaces = MagicMock(return_value=response)

        containers = self.fetcher.get(CONTAINERS_FOLDER_ID)
        self.assertEqual(0, len(containers))

    def test_get_no_matching_pod(self):
        self.inv.get_by_id.side_effect = self._get_by_id
        response = self._get_response(payload=PODS_RESPONSE_NO_MATCH,
                                      response_type='V1PodList')
        self.api.list_pod_for_all_namespaces = MagicMock(return_value=response)

        containers = self.fetcher.get(CONTAINERS_FOLDER_ID)
        self.assertEqual(0, len(containers))

    def tearDown(self):
        self.conf_patcher.stop()
        super().tearDown()
