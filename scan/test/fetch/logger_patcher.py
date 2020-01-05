###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import patch

from scan.test.test_base import TestBase


class LoggerPatcher(TestBase):

    def setUp(self):
        super().setUp()

        self.logger_patcher = patch(
            'discover.fetcher.FullLogger'
        )
        self.logger_class = self.logger_patcher.start()

    def tearDown(self):
        self.logger_patcher.stop()
        super().tearDown()
