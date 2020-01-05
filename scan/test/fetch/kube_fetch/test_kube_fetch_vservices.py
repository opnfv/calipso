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

from copy import deepcopy

from scan.fetchers.kube.kube_fetch_vservices import KubeFetchVservices
from scan.test.fetch.kube_fetch.kube_test_base import KubeTestBase
from scan.test.fetch.kube_fetch.test_data.kube_access import KUBE_CONFIG
from scan.test.fetch.kube_fetch.test_data.kube_fetch_vservices import \
    VSERVICES_FOLDER_DOC, NAMESPACE_DOC, VSERVICES_RESPONSE, EMPTY_RESPONSE, \
    VSERVICE_PODS, EXPECTED_VSERVICES


class TestKubeFetchVservices(KubeTestBase):

    def setUp(self):
        super().setUp()
        self.fetcher = KubeFetchVservices(KUBE_CONFIG)

    @staticmethod
    def _get_by_id(environment, item_id):
        if item_id == VSERVICES_FOLDER_DOC['id']:
            return VSERVICES_FOLDER_DOC
        elif item_id == NAMESPACE_DOC['id']:
            return NAMESPACE_DOC
        return None

    @staticmethod
    def _find_items(cond):
        return (
            deepcopy(VSERVICE_PODS[0])
            if cond.get('labels.app', None) == 'cisco-web'
            else deepcopy(VSERVICE_PODS[1])
        )

    def test_get(self):
        self.inv.get_by_id.side_effect = self._get_by_id
        self.inv.find_items.side_effect = self._find_items
        api_response = self._get_response(payload=VSERVICES_RESPONSE,
                                          response_type='V1ServiceList')
        self.api.list_namespaced_service = MagicMock(return_value=api_response)
        vservices = self.fetcher.get(VSERVICES_FOLDER_DOC['id'])
        self.assertEqual(2, len(vservices))
        self.assertListsContain(EXPECTED_VSERVICES, vservices)

    def test_get_empty_response(self):
        self.inv.get_by_id.side_effect = self._get_by_id
        api_response = self._get_response(payload=EMPTY_RESPONSE,
                                          response_type='V1ServiceList')
        self.api.list_namespaced_service = MagicMock(return_value=api_response)
        vservices = self.fetcher.get(VSERVICES_FOLDER_DOC['id'])
        self.assertEqual(0, len(vservices))

    def test_get_no_parent(self):
        self.inv.get_by_id.return_value = None
        vservices = self.fetcher.get(VSERVICES_FOLDER_DOC['id'])
        self.assertEqual(0, len(vservices))

    def test_get_no_namespace(self):
        self.inv.get_by_id.side_effect = [VSERVICES_FOLDER_DOC, None]
        vservices = self.fetcher.get(VSERVICES_FOLDER_DOC['id'])
        self.assertEqual(0, len(vservices))
