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

from scan.fetchers.db.db_fetch_instances import DbFetchInstances
from scan.test.fetch.db_fetch.test_data.db_fetch_instances import *
from scan.test.fetch.test_fetch import TestFetch


class TestDbFetchInstances(TestFetch):

    def setUp(self):
        super().setUp()
        self.configure_environment()
        self.fetcher = DbFetchInstances()

    def test_get(self):
        self.fetcher.get_objects_list = MagicMock(return_value=
                                                  INSTANCES_FROM_DB)
        self.fetcher.get_instance_data(INSTANCES_FROM_API)

        self.assertEqual(INSTANCES_FROM_API, UPDATED_INSTANCES_DATA)

    def test_build_instance_details_with_network(self):
        self.fetcher.build_instance_details(INSTANCE_WITH_NETWORK)
        self.assertEqual(INSTANCE_WITH_NETWORK,
                         INSTANCE_WITH_NETWORK_RESULT)

    def test_build_instance_details_without_network(self):
        self.fetcher.build_instance_details(INSTANCE_WITHOUT_NETWORK)
        self.assertEqual(INSTANCE_WITHOUT_NETWORK,
                         INSTANCE_WITHOUT_NETWORK_RESULT)
