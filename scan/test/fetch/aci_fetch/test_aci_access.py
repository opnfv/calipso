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

import requests
from copy import deepcopy

import scan.test.fetch.aci_fetch.test_data.aci_access as test_data
from scan.fetchers.aci.aci_access import AciAccess
from scan.test.fetch.aci_fetch.aci_test_base import AciTestBase


class TestAciAccess(AciTestBase):

    def test_login(self):

        self.aci_access.login()
        new_token = deepcopy(AciAccess.cookie_token)
        AciAccess.reset_token()

        self.assertEqual(test_data.VALID_COOKIE_TOKEN, new_token)

    def test_refresh_no_token(self):

        self.aci_access.refresh_token()
        new_token = deepcopy(AciAccess.cookie_token)
        AciAccess.reset_token()

        self.assertEqual(test_data.VALID_COOKIE_TOKEN, new_token)

    def test_refresh_ok_token(self):

        AciAccess.cookie_token = test_data.VALID_COOKIE_TOKEN
        self.aci_access.refresh_token()
        new_token = deepcopy(AciAccess.cookie_token)
        AciAccess.reset_token()

        self.assertEqual(test_data.VALID_COOKIE_TOKEN, new_token)

    def test_refresh_expired_token(self):

        AciAccess.cookie_token = test_data.VALID_COOKIE_TOKEN
        refresh_response_expired = MagicMock()
        refresh_response_expired.status_code = requests.codes.forbidden
        self.requests.get.return_value = refresh_response_expired
        self.aci_access.refresh_token()
        new_token = deepcopy(AciAccess.cookie_token)
        AciAccess.reset_token()

        self.assertEqual(test_data.VALID_COOKIE_TOKEN, new_token)
