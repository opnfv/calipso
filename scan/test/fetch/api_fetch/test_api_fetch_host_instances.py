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

from scan.fetchers.api.api_fetch_host_instances import ApiFetchHostInstances
from scan.test.fetch.api_fetch.test_data.api_fetch_host_instances import *
from scan.test.fetch.api_fetch.test_data.token import TOKEN
from scan.test.fetch.test_fetch import TestFetch


class TestApiFetchHostInstances(TestFetch):

    def setUp(self):
        super().setUp()
        self.configure_environment()

        self._v2_auth_pwd = ApiFetchHostInstances.v2_auth_pwd
        ApiFetchHostInstances.v2_auth_pwd = MagicMock(return_value=TOKEN)

        self.fetcher = ApiFetchHostInstances()
        self.set_regions_for_fetcher(self.fetcher)

    def test_get_projects(self):
        # mock the projects got from the database
        self.fetcher.inv.get = MagicMock(return_value=PROJECT_LIST)

        self.fetcher.get_projects()
        self.assertNotEqual(self.fetcher.projects, None, "Can't get projects info")

    def test_get_instances_from_api(self):
        self.fetcher.inv.get = MagicMock(return_value=PROJECT_LIST)
        # mock the response from the OpenStack Api
        self.fetcher.get_url = MagicMock(return_value=GET_SERVERS_RESPONSE)

        result = self.fetcher.get_instances_from_api(HOST_NAME)
        self.assertEqual(result, GET_INSTANCES_FROM_API, "Can't get correct " +
                                                         "instances info")

    def test_get_instances_from_api_with_wrong_auth(self):
        self.fetcher.v2_auth_pwd = MagicMock(return_value=None)

        result = self.fetcher.get_instances_from_api(HOST_NAME)
        self.assertEqual(result, [], "Can't get [] when the token is invalid")

    def test_get_instances_from_api_without_hypervisors_in_res(self):
        # mock the response without hypervisors info from OpenStack Api
        self.fetcher.get_url = MagicMock(return_value=RESPONSE_WITHOUT_HYPERVISORS)

        result = self.fetcher.get_instances_from_api(HOST_NAME)
        self.assertEqual(result, [], "Can't get [] when the response doesn't " +
                                     "contain hypervisors info")

    def test_get_instances_from_api_without_servers_in_res(self):
        # mock the response without servers info from OpenStack Api
        self.fetcher.get_url = MagicMock(return_value=RESPONSE_WITHOUT_SERVERS)

        result = self.fetcher.get_instances_from_api(HOST_NAME)
        self.assertEqual(result, [], "Can't get [] when the response doesn't " +
                                     "contain servers info")

    def test_get(self):
        self.fetcher.inv.get = MagicMock(return_value=PROJECT_LIST)
        self.fetcher.inv.get_by_id = MagicMock(return_value=HOST)

        original_method = self.fetcher.get_instances_from_api
        self.fetcher.get_instances_from_api = MagicMock(return_value=
                                                        GET_INSTANCES_FROM_API)

        self.fetcher.db_fetcher.get_instance_data = MagicMock()
        result = self.fetcher.get(INSTANCE_FOLDER_ID)
        self.assertNotEqual(result, [], "Can't get instances info")

        self.fetcher.get_instances_from_api = original_method

    def test_get_with_non_compute_node(self):
        self.fetcher.inv.get = MagicMock(return_value=PROJECT_LIST)
        self.fetcher.inv.get_by_id = MagicMock(return_value=NON_COMPUTE_HOST)

        result = self.fetcher.get(INSTANCE_FOLDER_ID)
        self.assertEqual(result, [], "Can't get [] when the host is " +
                                     "not compute node")

    def tearDown(self):
        super().tearDown()
        ApiFetchHostInstances.v2_auth_pwd = self._v2_auth_pwd
        self.reset_regions_for_fetcher(self.fetcher)
