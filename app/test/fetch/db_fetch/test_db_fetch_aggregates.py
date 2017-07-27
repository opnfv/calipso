from discover.fetchers.db.db_fetch_aggregates import DbFetchAggregates
from test.fetch.test_fetch import TestFetch
from test.fetch.db_fetch.test_data.db_fetch_aggregates import *
from unittest.mock import MagicMock


class TestDbFetchAggregates(TestFetch):

    def setUp(self):
        self.configure_environment()
        self.fetcher = DbFetchAggregates()

    def test_get(self):
        self.fetcher.get_objects_list = MagicMock(return_value=OBJECTS_LIST)
        result = self.fetcher.get(REGION_ID)
        self.assertEqual(result, OBJECTS_LIST, "Can't get correct " +
                                               "aggregates info")
