#!/usr/bin/env python3
###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from abc import ABC, abstractmethod

from utils.logging.file_logger import FileLogger
from utils.logging.full_logger import FullLogger
from utils.mongo_access import MongoAccess


class Manager(ABC):

    MIN_INTERVAL = 0.1  # To prevent needlessly frequent scans

    def __init__(self, log_directory: str = None,
                 mongo_config_file: str = None):
        super().__init__()
        if log_directory:
            FileLogger.LOG_DIRECTORY = log_directory
        MongoAccess.config_file = mongo_config_file
        self.log = FullLogger()
        self.conf = None
        self.inv = None
        self.collection = None
        self._update_document = None
        self.interval = self.MIN_INTERVAL

    @abstractmethod
    def configure(self):
        pass

    @abstractmethod
    def do_action(self):
        pass

    def run(self):
        self.configure()
        self.do_action()
