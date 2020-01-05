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

from scan.fetchers.kube.kube_fetch_nodes import KubeFetchNodes
from scan.test.fetch.kube_fetch.kube_test_base import KubeTestBase
from scan.test.fetch.kube_fetch.test_data.kube_access import KUBE_CONFIG
from scan.test.fetch.kube_fetch.test_data.kube_fetch_nodes import EMPTY_RESPONSE, \
    NODES_RESPONSE, CLI_LINES, EXPECTED_NODES


class TestKubeFetchNodes(KubeTestBase):

    def setUp(self):
        super().setUp()

        self.conf_patcher = patch(
            'utils.cli_access.Configuration'
        )
        self.conf_class = self.conf_patcher.start()

        self.fetcher = KubeFetchNodes(KUBE_CONFIG)

    @staticmethod
    def _run_lines(cmd, ssh_to_host="", enable_cache=True, use_sudo=True):
        if cmd:
            pass
        if enable_cache:
            pass
        if use_sudo:
            pass
        return CLI_LINES.get(ssh_to_host, [])

    def test_get(self):
        response = self._get_response(payload=NODES_RESPONSE,
                                      response_type='V1NodeList')
        self.api.list_node = MagicMock(return_value=response)
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        self.fetcher.run_fetch_lines = MagicMock(side_effect=self._run_lines)
        original_details_fetcher_set_interface_data = \
            self.fetcher.details_fetcher.set_interface_data
        self.fetcher.details_fetcher.set_interface_data = MagicMock()

        nodes = self.fetcher.get(None)
        self.assertEqual(3, len(nodes))
        self.assertListsContain(EXPECTED_NODES, nodes)

        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.fetcher.details_fetcher.set_interface_data = \
            original_details_fetcher_set_interface_data

    def test_get_no_nodes(self):
        response = self._get_response(payload=EMPTY_RESPONSE,
                                      response_type='V1NodeList')
        self.api.list_node = MagicMock(return_value=response)
        nodes = self.fetcher.get(None)
        self.assertEqual(0, len(nodes))

    def tearDown(self):
        self.conf_patcher.stop()
        super().tearDown()
