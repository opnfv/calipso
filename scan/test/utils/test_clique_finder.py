###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import unittest
from unittest.mock import patch, MagicMock

from base.utils.inventory_mgr import InventoryMgr
from base.utils.mongo_access import MongoAccess
from scan.clique_finder import CliqueFinder
from scan.test.utils.test_data.clique_finder import CLIQUE_TYPES, ENVIRONMENT


class TestCliqueFinder(unittest.TestCase):

    def setUp(self):
        MongoAccess.mongo_connect = MagicMock()
        MongoAccess.db = MagicMock()

        self.inventory_collection = 'test_inventory'
        self.inv = InventoryMgr()
        self.inv.set_collections(self.inventory_collection)

        self.conf_patcher = patch('discover.fetcher.Configuration')
        self.conf_class = self.conf_patcher.start()
        self.configuration = self.conf_class.return_value
        self.configuration.environment = ENVIRONMENT

        self.clique_finder = CliqueFinder()
        self.clique_finder.set_env(ENVIRONMENT['name'])

    def tearDown(self):
        self.conf_patcher.stop()

    def test_get_priority_score(self):
        for ct in CLIQUE_TYPES:
            score = self.clique_finder.get_priority_score(ct['clique_type'])
            self.assertEqual(
                ct['score'], score,
                msg="Wrong clique type priority score "
                    "for clique type '{ct}': {score} "
                    "(should be {expected})".format(ct=ct['name'],
                                                    score=score,
                                                    expected=ct['score'])
            )
