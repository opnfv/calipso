from discover.fetchers.cli.cli_fetch_host_vservices import CliFetchHostVservices
from test.fetch.test_fetch import TestFetch
from test.fetch.cli_fetch.test_data.cli_fetch_host_verservices import *
from unittest.mock import MagicMock


class TestCliFetchHostVservices(TestFetch):

    def setUp(self):
        self.configure_environment()
        self.fetcher = CliFetchHostVservices()
        self.fetcher.set_env(self.env)

    def test_get(self):
        # store original get_single method
        original_get_single = self.fetcher.inv.get_single
        # mock the host data
        self.fetcher.inv.get_single = MagicMock(return_value=NETWORK_HOST)
        # store original run_fetch_lines method
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        # mock command line results
        self.fetcher.run_fetch_lines = MagicMock(return_value=NAMESPACES)

        # only test the logic on get method, mock the set_details method
        original_set_details = self.fetcher.set_details
        self.fetcher.set_details = MagicMock()

        result = self.fetcher.get(NETWORK_HOST['id'])
        # reset methods
        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.fetcher.set_details = original_set_details
        self.fetcher.inv.get_single = original_get_single

        self.assertNotEqual(result, [], "Can't get verservices")

    def test_get_with_wrong_host_type(self):
        # store original get_single method
        original_get_single = self.fetcher.inv.get_single
        # mock the host data
        self.fetcher.inv.get_single = MagicMock(return_value=COMPUTE_HOST)
        result = self.fetcher.get(COMPUTE_HOST['id'])

        self.fetcher.inv.get_single = original_get_single

        self.assertEqual(result, [], "Can't get empty array when the host_type doesn't contain Network")

    def test_set_details(self):
        # store orginal methods
        original_get_router_name = self.fetcher.get_router_name
        original_get_network_name = self.fetcher.get_network_name
        original_get_type = self.fetcher.agents_list.get_type

        # mock methods
        self.fetcher.get_network_name = MagicMock(return_value=ROUTER[0]['name'])
        self.fetcher.get_router_name = MagicMock(return_value=ROUTER[0]['name'])
        self.fetcher.agents_list.get_type = MagicMock(return_value=AGENT)

        self.fetcher.set_details(NETWORK_HOST['id'], LOCAL_SERVICES_IDS[0])

        # reset methods
        self.fetcher.get_network_name = original_get_network_name
        self.fetcher.get_router_name = original_get_router_name
        self.fetcher.agents_list.get_type = original_get_type

        self.assertIn("name", LOCAL_SERVICES_IDS[0], "Can't add name")
        self.assertIn("parent_id", LOCAL_SERVICES_IDS[0], "Can't add parent id")

    def test_get_network_name(self):
        # store original method
        original_get_objects_list_for_id = self.fetcher.get_objects_list_for_id
        # mock the result
        self.fetcher.get_objects_list_for_id = MagicMock(return_value=ROUTER)

        name = self.fetcher.get_network_name(ID_CLEAN)

        self.fetcher.get_objects_list_for_id = original_get_objects_list_for_id
        self.assertEqual(name, ROUTER[0]['name'], "Can't get network name")

    def test_get_network_without_router(self):
        # store original method
        original_get_objects_list_for_id = self.fetcher.get_objects_list_for_id
        # mock the result
        self.fetcher.get_objects_list_for_id = MagicMock(return_value=[])

        name = self.fetcher.get_network_name(ID_CLEAN)

        self.fetcher.get_objects_list_for_id = original_get_objects_list_for_id
        self.assertEqual(name, ID_CLEAN, "Can't use the id as the name when network info from database is empty")

    def test_get_router_name(self):
        # store original method
        original_get_objects_list_for_id = self.fetcher.get_objects_list_for_id
        # mock the result
        self.fetcher.get_objects_list_for_id = MagicMock(return_value=ROUTER)

        name = self.fetcher.get_router_name(LOCAL_SERVICES_IDS[0], ID_CLEAN)

        self.fetcher.get_objects_list_for_id = original_get_objects_list_for_id

        self.assertIn("name", LOCAL_SERVICES_IDS[0], "Can't get network name")
        self.assertEqual(name, ROUTER[0]['name'], "Can't get router name")

    def test_set_agent_type(self):
        # store original get_type method
        original_get_type = self.fetcher.agents_list.get_type
        self.fetcher.agents_list.get_type = MagicMock(return_value=AGENT)

        self.fetcher.set_agent_type(VSERVICE)
        # reset method
        self.fetcher.set_agent_type = original_get_type
        self.assertIn("parent_id", VSERVICE, "Can't add parent id to vservice document")

    def test_set_agent_type_without_agent(self):
        # store original get_type method
        original_get_type = self.fetcher.agents_list.get_type
        self.fetcher.agents_list.get_type = MagicMock(return_value={})

        self.fetcher.set_agent_type(VSERVICE)
        # reset method
        self.fetcher.set_agent_type = original_get_type
        self.assertIn("parent_id", VSERVICE, "Can't add parent id to vservice document")
        self.assertEqual(VSERVICE['parent_type'], "vservice_miscellenaous_folder",
                         "Can't add document to miscellenaous folder when it doesn't have agent")