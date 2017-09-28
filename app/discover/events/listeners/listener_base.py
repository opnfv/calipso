###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import os
from abc import ABC, abstractmethod

from utils.logging.console_logger import ConsoleLogger
from utils.logging.file_logger import FileLogger
from utils.logging.logger import Logger


class ListenerBase(ABC):

    LOG_FILENAME = "listener_base.log"
    LOG_LEVEL = Logger.WARNING

    def __init__(self):
        super().__init__()
        self.log_file = os.path.join(FileLogger.LOG_DIRECTORY,
                                     self.LOG_FILENAME)
        self.log = ConsoleLogger(level=Logger.INFO)

    @staticmethod
    @abstractmethod
    def listen(self):
        pass
