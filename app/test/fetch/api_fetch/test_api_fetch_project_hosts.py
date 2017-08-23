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
from discover.fetchers.api.api_fetch_project_hosts import ApiFetchProjectHosts
from test.fetch.test_fetch import TestFetch
from test.fetch.api_fetch.test_data.api_fetch_host_project_hosts import *
from test.fetch.api_fetch.test_data.token import TOKEN
from test.fetch.api_fetch.test_data.regions import REGIONS


class TestApiFetchProjectHosts(TestFetch):

    def setUp(self):
        super().setUp()
        self.configure_environment()

        self._v2_auth_pwd = ApiFetchProjectHosts.v2_auth_pwd
        ApiFetchProjectHosts.v2_auth_pwd = MagicMock(return_value=TOKEN)

        self.fetcher = ApiFetchProjectHosts()
        self.set_regions_for_fetcher(self.fetcher)
        self.region = REGIONS[REGION_NAME]

    def test_add_host_type_with_nonexistent_type(self):
        # clear host type
        HOST_DOC["host_type"] = []
        self.fetcher.add_host_type(HOST_DOC, NONEXISTENT_TYPE, HOST_ZONE)
        self.assertIn(NONEXISTENT_TYPE, HOST_DOC["host_type"], "Can't put nonexistent " +
                                                               "type in host_type")

    def test_add_host_type_with_existent_host_type(self):
        # add nonexistent host type to host type
        HOST_DOC["host_type"] = [NONEXISTENT_TYPE]
        # try to add existing host type
        self.fetcher.add_host_type(HOST_DOC, NONEXISTENT_TYPE, HOST_ZONE)
        self.assertEqual(len(HOST_DOC['host_type']), 1, "Add duplicate host type")

    def test_add_compute_host_type(self):
        HOST_DOC['host_type'] = []
        # clear zone
        HOST_DOC['zone'] = None
        # add compute host type
        self.fetcher.add_host_type(HOST_DOC, COMPUTE_TYPE, HOST_ZONE)
        # for compute host type, zone information will be added
        self.assertEqual(HOST_DOC['zone'], HOST_ZONE, "Can't update zone " +
                                                      "name for compute node")
        self.assertEqual(HOST_DOC['parent_id'], HOST_ZONE, "Can't update parent_id " +
                                                           "for compute node")

    def test_fetch_compute_node_ip_address(self):
        # mock ip address information fetched from DB
        self.fetcher.get_objects_list_for_id = MagicMock(return_value=IP_ADDRESS_RESPONSE)

        self.fetcher.fetch_compute_node_ip_address(HOST_TO_BE_FETCHED_IP,
                                                   HOST_TO_BE_FETCHED_IP["host"])
        self.assertIn("ip_address", HOST_TO_BE_FETCHED_IP, "Can't update ip address " +
                                                           "for the compute host")

    def test_fetch_network_node_details(self):
        # mock NETWORKS_DETAILS_RESPONSE fetched from DB
        self.fetcher.get_objects_list = MagicMock(return_value=NETWORKS_DETAILS_RESPONSE)

        self.fetcher.fetch_network_node_details(HOSTS_TO_BE_FETCHED_NETWORK_DETAILS)
        # get the network node document from HOSTS
        NETWORK_NODE_DOC = [doc for doc in HOSTS_TO_BE_FETCHED_NETWORK_DETAILS
                            if doc['host'] == HOST_NAME][0]
        # check if the network node document has been updated
        self.assertIn("Network", NETWORK_NODE_DOC['host_type'], "Can't put Network in " +
                                                                "the network node host_type")
        self.assertIn("config", NETWORK_NODE_DOC, "Can't put config in the network node")

    def test_get_host_details(self):
        # test node have nova-conductor attribute, controller type will be added
        result = self.fetcher.get_host_details(AVAILABILITY_ZONE, HOST_NAME)
        self.assertIn("Controller", result['host_type'], "Can't put controller type " +
                                                         "in the compute node host_type")

    def test_get_hosts_from_az(self):
        result = self.fetcher.get_hosts_from_az(AVAILABILITY_ZONE)
        self.assertNotEqual(result, [], "Can't get hosts information from "
                                        "availability zone")

    def test_get_for_region(self):
        # mock region url for nova node
        self.fetcher.get_region_url = MagicMock(return_value=REGION_URL)
        # mock the response from OpenStack Api
        side_effect = [AVAILABILITY_ZONE_RESPONSE, HYPERVISORS_RESPONSE]
        self.fetcher.get_url = MagicMock(side_effect=side_effect)

        result = self.fetcher.get_for_region(self.region, TOKEN)
        self.assertNotEqual(result, [], "Can't get hosts information for region")

    def test_get_for_region_without_token(self):
        self.fetcher.get_region_url = MagicMock(return_value=REGION_URL)
        result = self.fetcher.get_for_region(self.region, None)
        self.assertEqual(result, [], "Can't get [] when the token is invalid")

    def test_get_for_region_with_error_availability_response(self):
        self.fetcher.get_region_url = MagicMock(return_value=REGION_URL)
        # mock error availability zone response from OpenStack Api
        side_effect = [AVAILABILITY_ERROR_RESPONSE, None]
        self.fetcher.get_url = MagicMock(side_effect=side_effect)

        result = self.fetcher.get_for_region(self.region, TOKEN)
        self.assertEqual(result, [], "Can't get [] when the response is wrong")

    def test_get_for_region_with_error_hypervisors_response(self):
        self.fetcher.get_region_url = MagicMock(return_value=REGION_URL)
        # mock error hypervisors response from OpenStack Api
        side_effect = [AVAILABILITY_ZONE_RESPONSE, HYPERVISORS_ERROR_RESPONSE]
        self.fetcher.get_url = MagicMock(side_effect=side_effect)

        result = self.fetcher.get_for_region(self.region, TOKEN)
        self.assertNotEqual(result, [], "Can't get hosts information when " +
                                        "the hypervisors response is wrong")

    def test_get(self):
        original_method = self.fetcher.get_for_region
        self.fetcher.get_for_region = MagicMock(return_value=GET_FOR_REGION_INFO)

        result = self.fetcher.get(PROJECT_NAME)

        self.fetcher.get_for_region = original_method

        self.assertNotEqual(result, [], "Can't get hosts info for the project")

    def test_get_with_wrong_project_name(self):
        result = self.fetcher.get(TEST_PROJECT_NAME)
        self.assertEqual(result, [], "Can't get [] when the project name is not admin")

    def test_get_with_wrong_token(self):
        self.fetcher.v2_auth_pwd = MagicMock(return_value=[])
        result = self.fetcher.get(PROJECT_NAME)
        self.assertEqual(result, [], "Can't get [] when the token is invalid")

    def tearDown(self):
        super().tearDown()
        ApiFetchProjectHosts.v2_auth_pwd = self._v2_auth_pwd
        self.reset_regions_for_fetcher(self.fetcher)
