###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import MagicMock
from discover.fetchers.api.api_fetch_projects import ApiFetchProjects
from test.fetch.test_fetch import TestFetch
from test.fetch.api_fetch.test_data.api_fetch_projects import *
from test.fetch.api_fetch.test_data.regions import REGIONS
from test.fetch.api_fetch.test_data.token import TOKEN


class TestApiFetchProjects(TestFetch):

    def setUp(self):
        self.configure_environment()
        ApiFetchProjects.v2_auth_pwd = MagicMock(return_value=TOKEN)
        self.fetcher = ApiFetchProjects()
        self.set_regions_for_fetcher(self.fetcher)
        self.region = REGIONS[REGION_NAME]
        self.fetcher.get_region_url_nover = MagicMock(return_value=REGION_URL_NOVER)

    def test_get_for_region(self):
        # mock request endpoint
        self.fetcher.get_region_url_nover = MagicMock(return_value=REGION_URL_NOVER)
        self.fetcher.get_url = MagicMock(return_value=REGION_RESPONSE)

        result = self.fetcher.get_for_region(self.region, TOKEN)
        self.assertEqual(result, REGION_RESULT, "Can't get correct projects info")

    # TODO does this test case make sense?
    def test_get_for_region_with_error_region_response(self):
        self.fetcher.get_region_url_nover = MagicMock(return_value=REGION_URL_NOVER)
        self.fetcher.get_url = MagicMock(return_value=REGION_ERROR_RESPONSE)

        result = self.fetcher.get_for_region(self.region, TOKEN)
        self.assertEqual(result, [], "Can't get [] when the " +
                                     "region response is wrong")

    def test_get_projects_for_api_user(self):
        # mock the responses from OpenStack Api
        self.fetcher.get_url = MagicMock(return_value=PROJECTS_CORRECT_RESPONSE)

        result = self.fetcher.get_projects_for_api_user(self.region, TOKEN)
        self.assertEqual(result, PROJECT_RESULT, "Can't get correct " +
                                                 "projects info for api user")

    def test_get_projects_for_api_user_without_projects_response(self):
        # the projects info from OpenStack Api will be None
        self.fetcher.get_url = MagicMock(return_value=
                                         PROJECTS_RESPONSE_WITHOUT_PROJECTS)

        result = self.fetcher.get_projects_for_api_user(self.region, TOKEN)
        self.assertIs(result, None, "Can't get None when the project " +
                                    "response doesn't contain projects info")

    def check_get_result(self, projects_for_api_user,
                         region_result,
                         token,
                         expected_result, error_msg):
        self.fetcher.get_projects_for_api_user = MagicMock(return_value=
                                                           projects_for_api_user)
        original_method = self.fetcher.get_for_region
        # mock
        self.fetcher.get_for_region = MagicMock(return_value=region_result)
        self.fetcher.v2_auth_pwd = MagicMock(return_value=token)

        result = self.fetcher.get(PROJECT_ID)

        self.fetcher.get_for_region = original_method
        self.assertEqual(result, expected_result, error_msg)

    def test_get(self):
        # test get method with different test cases
        test_cases = [
            {
                "projects": PROJECT_RESULT,
                "regions": REGION_RESULT,
                "token": TOKEN,
                "expected_result": REGION_RESULT,
                "err_msg": "Can't get correct project result"
            },
            {
                "projects": PROJECT_RESULT,
                "regions": REGION_RESULT_WITH_NON_USER_PROJECT,
                "token": TOKEN,
                "expected_result": REGION_RESULT,
                "err_msg": "Can't get correct project result" +
                           "when the region result contains project " +
                           "that doesn't belong to the user"
            },
            {
                "projects": PROJECT_RESULT,
                "regions": REGION_RESULT,
                "token": None,
                "expected_result": [],
                "err_msg": "Can't get [] when the token is invalid"
            },
            {
                "projects": None,
                "regions": REGION_RESULT,
                "token": TOKEN,
                "expected_result": REGION_RESULT,
                "err_msg": "Can't get the region " +
                           "result if the projects " +
                           "for the user doesn't exist"
            }
        ]

        for test_case in test_cases:
            self.check_get_result(test_case["projects"],
                                  test_case["regions"],
                                  test_case["token"],
                                  test_case["expected_result"],
                                  test_case["err_msg"])
