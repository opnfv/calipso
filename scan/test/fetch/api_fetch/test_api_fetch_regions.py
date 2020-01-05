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

from scan.fetchers.api.api_fetch_regions import ApiFetchRegions
from scan.test.fetch.api_fetch.test_data.api_fetch_regions import *
from scan.test.fetch.api_fetch.test_data.token import TOKEN
from scan.test.fetch.test_fetch import TestFetch


class TestApiFetchRegions(TestFetch):

    def setUp(self):
        super().setUp()

        self._v2_auth_pwd = ApiFetchRegions.v2_auth_pwd
        ApiFetchRegions.v2_auth_pwd = MagicMock(return_value=TOKEN)

        self.configure_environment()

    def test_get(self):
        fetcher = ApiFetchRegions()
        fetcher.set_env(ENV)

        fetcher.auth_response = AUTH_RESPONSE
        ret = fetcher.get("test_id")
        self.assertEqual(ret, REGIONS_RESULT,
                         "Can't get correct regions information")

    def test_get_without_token(self):
        fetcher = ApiFetchRegions()
        fetcher.v2_auth_pwd = MagicMock(return_value=[])
        fetcher.set_env(ENV)

        ret = fetcher.get("test_id")

        ApiFetchRegions.v2_auth_pwd = MagicMock(return_value=TOKEN)
        self.assertEqual(ret, [], "Can't get [] when the token is invalid")

    def tearDown(self):
        super().tearDown()
        ApiFetchRegions.v2_auth_pwd = self._v2_auth_pwd
