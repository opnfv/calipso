###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re
import unittest

from discover.configuration import Configuration
from test.event_based_scan.config.test_config \
    import MONGODB_CONFIG, ENV_CONFIG, COLLECTION_CONFIG
from utils.inventory_mgr import InventoryMgr
from utils.logging.console_logger import ConsoleLogger
from utils.mongo_access import MongoAccess


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.log = ConsoleLogger()
        self.mongo_config = MONGODB_CONFIG
        self.env = ENV_CONFIG
        self.collection = COLLECTION_CONFIG

        MongoAccess.set_config_file(self.mongo_config)
        self.conf = Configuration()
        self.conf.use_env(self.env)

        self.inv = InventoryMgr()
        self.inv.set_collections(self.collection)
        self.item_ids = []

    def set_item(self, document):
        self.inv.set(document)
        self.item_ids.append(document['id'])

    def assert_empty_by_id(self, object_id):
        doc = self.inv.get_by_id(self.env, object_id)
        self.assertIsNone(doc)

    def tearDown(self):
        for item_id in self.item_ids:
            item = self.inv.get_by_id(self.env, item_id)
            # delete children
            if item:
                regexp = re.compile('^{}/'.format(item['id_path']))
                self.inv.delete('inventory', {'id_path': {'$regex': regexp}})

            # delete target item
            self.inv.delete('inventory', {'id': item_id})
            item = self.inv.get_by_id(self.env, item_id)
            self.assertIsNone(item)
