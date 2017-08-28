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
from unittest.mock import patch, Mock

from test.event_based_scan.test_data.test_config \
    import ENV_CONFIG, COLLECTION_CONFIG
from utils.logging.console_logger import ConsoleLogger


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.log = ConsoleLogger()
        self.env = ENV_CONFIG
        self.collection = COLLECTION_CONFIG
        self.item_ids = []

        self.inv_patcher = patch('discover.events.event_base.InventoryMgr')
        self.inv_class = self.inv_patcher.start()
        self.inv = self.inv_class.return_value

        self.log_patcher = patch('discover.fetcher.FullLogger')
        self.log_patcher.start()

    def tearDown(self):
        self.inv_patcher.stop()
        self.log_patcher.stop()
