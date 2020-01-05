###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import unittest
from unittest.mock import patch, MagicMock

import re
import requests

import scan.test.fetch.aci_fetch.test_data.aci_access as test_data
from scan.fetchers.aci.aci_access import AciAccess


class AciTestBase(unittest.TestCase):

    RESPONSES = {}

    def setUp(self):
        super().setUp()

        self.req_patcher = patch("discover.fetchers.aci.aci_access.requests")
        self.requests = self.req_patcher.start()
        self.requests.codes = requests.codes
        self.response = MagicMock()
        self.response.json.return_value = test_data.LOGIN_RESPONSE
        self.requests.get.return_value = self.response
        self.requests.post.return_value = self.response

        self.aci_access = AciAccess(config=test_data.ACI_CONFIG)

    def _requests_get(self, url, *args, **kwargs):
        response = MagicMock()
        return_value = next((resp
                             for endpoint, resp in self.RESPONSES.items()
                             if re.match(".*{}.*".format(endpoint), url)),
                            None)
        response.json.return_value = return_value
        return response

    def tearDown(self):
        self.req_patcher.stop()
        super().tearDown()

