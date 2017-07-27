from discover.fetchers.cli.cli_fetch_vconnectors import CliFetchVconnectors
from test.fetch.test_fetch import TestFetch
from test.fetch.cli_fetch.test_data.cli_fetch_vconnectors import *
from unittest.mock import MagicMock


class TestCliFetchVconnectors(TestFetch):

    def setUp(self):
        self.configure_environment()
        self.fetcher = CliFetchVconnectors()
        self.fetcher.set_env(self.env)

    def test_get(self):
        # store original methods
        original_get_by_id = self.fetcher.inv.get_by_id
        original_get_vconnectors = self.fetcher.get_vconnectors

        # mock methods
        self.fetcher.inv.get_by_id = MagicMock(return_value=HOST)
        self.fetcher.get_vconnectors = MagicMock(return_value=VCONNECTORS)

        result = self.fetcher.get(VCONNECTORS_FOLDER['id'])

        # reset methods
        self.fetcher.inv.get_by_id = original_get_by_id
        self.fetcher.get_vconnectors = original_get_vconnectors

        self.assertEqual(result, VCONNECTORS, "Can't get the vconnectors")

    def test_get_without_host(self):
        # store original methods
        original_get_by_id = self.fetcher.inv.get_by_id

        # mock methods
        self.fetcher.inv.get_by_id = MagicMock(return_value=[])

        result = self.fetcher.get(VCONNECTORS_FOLDER['id'])

        # reset methods
        self.fetcher.inv.get_by_id = original_get_by_id

        self.assertEqual(result, [], "Can't get empty array when the host doesn't exist")

    def test_get_with_wrong_host(self):
        # store original methods
        original_get_by_id = self.fetcher.inv.get_by_id

        # mock methods
        self.fetcher.inv.get_by_id = MagicMock(return_value=WRONG_HOST)

        result = self.fetcher.get(VCONNECTORS_FOLDER['id'])

        # reset methods
        self.fetcher.inv.get_by_id = original_get_by_id

        self.assertEqual(result, [], "Can't get empty array when the host doesn't contain host type")