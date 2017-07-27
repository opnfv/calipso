###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import unittest

from discover.configuration import Configuration
from discover.fetchers.db.db_access import DbAccess
from test.fetch.config.test_config import MONGODB_CONFIG, ENV_CONFIG, COLLECTION_CONFIG
from test.fetch.api_fetch.test_data.regions import REGIONS
from test.fetch.api_fetch.test_data.configurations import CONFIGURATIONS
from unittest.mock import MagicMock
from utils.inventory_mgr import InventoryMgr
from utils.mongo_access import MongoAccess
from utils.ssh_connection import SshConnection
from utils.ssh_conn import SshConn


class TestFetch(unittest.TestCase):

    def configure_environment(self):
        self.env = ENV_CONFIG
        self.inventory_collection = COLLECTION_CONFIG
        # mock the Mongo Access
        MongoAccess.mongo_connect = MagicMock()
        MongoAccess.db = MagicMock()

        self.conf = Configuration()
        self.conf.use_env = MagicMock()
        self.conf.environment = CONFIGURATIONS
        self.conf.configuration = CONFIGURATIONS["configuration"]

        self.inv = InventoryMgr()
        self.inv.set_collections(self.inventory_collection)
        DbAccess.conn = MagicMock()
        SshConnection.connect = MagicMock()
        SshConnection.check_definitions = MagicMock()
        SshConn.check_definitions = MagicMock()

    def set_regions_for_fetcher(self, fetcher):
        fetcher.regions = REGIONS
