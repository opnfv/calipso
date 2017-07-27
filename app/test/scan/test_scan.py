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
from unittest.mock import MagicMock

from discover.configuration import Configuration
from monitoring.setup.monitoring_setup_manager import MonitoringSetupManager
from test.scan.config.test_config \
    import MONGODB_CONFIG, ENV_CONFIG, COLLECTION_CONFIG
from test.scan.test_data.configurations import CONFIGURATIONS
from utils.inventory_mgr import InventoryMgr
from utils.mongo_access import MongoAccess
from utils.logging.full_logger import FullLogger


class TestScan(unittest.TestCase):

    def configure_environment(self):
        self.env = ENV_CONFIG
        self.inventory_collection = COLLECTION_CONFIG
        # mock the mongo access
        MongoAccess.mongo_connect = MagicMock()
        MongoAccess.db = MagicMock()
        # mock log
        FullLogger.info = MagicMock()

        self.conf = Configuration()
        self.conf.use_env = MagicMock()
        self.conf.environment = CONFIGURATIONS
        self.conf.configuration = CONFIGURATIONS["configuration"]

        self.inv = InventoryMgr()
        self.inv.clear = MagicMock()
        self.inv.set_collections(self.inventory_collection)

        MonitoringSetupManager.server_setup = MagicMock()

    def setUp(self):
        self.configure_environment()
