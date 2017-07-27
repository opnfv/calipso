###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.api.api_access import ApiAccess
from discover.fetchers.api.api_fetch_regions import ApiFetchRegions
from test.fetch.test_fetch import TestFetch
from test.fetch.api_fetch.test_data.api_fetch_regions import *
from test.fetch.api_fetch.test_data.token import TOKEN
from unittest.mock import MagicMock


class TestApiFetchRegions(TestFetch):

    def setUp(self):
        ApiFetchRegions.v2_auth_pwd = MagicMock(return_value=TOKEN)
        self.configure_environment()

    def test_get(self):
        fetcher = ApiFetchRegions()
        fetcher.set_env(ENV)

        ApiAccess.auth_response = AUTH_RESPONSE
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
