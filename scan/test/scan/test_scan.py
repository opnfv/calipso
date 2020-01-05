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
from unittest.mock import MagicMock

from base.utils.configuration import Configuration
from base.utils.inventory_mgr import InventoryMgr
from base.utils.logging.full_logger import FullLogger
from base.utils.mongo_access import MongoAccess
from monitoring.setup.monitoring_setup_manager import MonitoringSetupManager
from scan.fetchers.db.db_access import DbAccess
from scan.test.scan.config.test_config \
    import ENV_CONFIG, COLLECTION_CONFIG
from scan.test.scan.test_data.configurations import CONFIGURATIONS


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

        DbAccess.get_neutron_db_name = MagicMock()
        DbAccess.get_neutron_db_name.return_value = "neutron"

    def setUp(self):
        self.configure_environment()
