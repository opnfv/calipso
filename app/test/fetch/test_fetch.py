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
from test.fetch.api_fetch.test_data.api_access import CORRECT_AUTH_CONTENT
from test.fetch.config.test_config import MONGODB_CONFIG, ENV_CONFIG, COLLECTION_CONFIG
from test.fetch.api_fetch.test_data.regions import REGIONS
from test.fetch.api_fetch.test_data.configurations import CONFIGURATIONS
from unittest.mock import MagicMock, patch, Mock
from utils.inventory_mgr import InventoryMgr
from utils.mongo_access import MongoAccess
from utils.ssh_connection import SshConnection
from utils.ssh_conn import SshConn


class TestFetch(unittest.TestCase):

    def setUp(self):
        self._mongo_connect = MongoAccess.mongo_connect
        self._mongo_db = MongoAccess.db
        self._db_access_conn = DbAccess.conn
        self._ssh_connect = SshConnection.connect
        self._ssh_conn_check_defs = SshConnection.check_definitions
        self._ssh_check_defs = SshConn.check_definitions

        self.req_patcher = patch("discover.fetchers.api.api_access.requests")
        self.requests = self.req_patcher.start()
        self.response = MagicMock()
        self.response.codes.ok = 200
        self.response.json = Mock(return_value=CORRECT_AUTH_CONTENT)
        self.response.status_code = self.requests.codes.ok
        self.requests.get.return_value = self.response
        self.requests.post.return_value = self.response

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
        self._regions = fetcher.regions
        fetcher.regions = REGIONS

    def reset_regions_for_fetcher(self, fetcher):
        fetcher.regions = self._regions

    def tearDown(self):
        MongoAccess.mongo_connect = self._mongo_connect
        MongoAccess.db = self._mongo_db
        DbAccess.conn = self._db_access_conn
        SshConnection.connect = self._ssh_connect
        SshConnection.check_definitions = self._ssh_conn_check_defs
        SshConn.check_definitions = self._ssh_check_defs
        self.req_patcher.stop()