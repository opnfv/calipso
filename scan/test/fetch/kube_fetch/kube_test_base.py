###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json
from unittest.mock import patch

from kubernetes.client import ApiClient
from kubernetes.client.rest import RESTResponse
from urllib3 import HTTPResponse

from scan.test.fetch.logger_patcher import LoggerPatcher


class KubeTestBase(LoggerPatcher):
    RESPONSES = {}

    def setUp(self):
        super().setUp()

        self.inv_patcher = patch(
            'discover.fetchers.kube.kube_access.InventoryMgr'
        )
        self.inv_class = self.inv_patcher.start()
        self.inv = self.inv_class.return_value

        self.kube_client_patcher = patch(
            "discover.fetchers.kube.kube_access.kube_client"
        )
        self.kube_client = self.kube_client_patcher.start()
        self.api = self.kube_client.CoreV1Api()
        self.fetcher = None

    @staticmethod
    def _get_response(payload, response_type):
        urllib_response = HTTPResponse(status=200, body=json.dumps(payload))
        kube_response = ApiClient().deserialize(RESTResponse(urllib_response),
                                                response_type)
        return kube_response

    def tearDown(self):
        self.kube_client_patcher.stop()
        self.inv_patcher.stop()
        super().tearDown()
