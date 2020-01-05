###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import os
from abc import ABC, abstractmethod

from base.utils.logging.file_logger import FileLogger
from base.utils.logging.full_logger import FullLogger
from base.utils.logging.logger import Logger
from listen.events.event_base import EventResult


class ListenerBase(ABC):

    SOURCE_SYSTEM = "Listener"
    COMMON_METADATA_FILE = ""

    LOG_FILENAME = "listener_base.log"
    LOG_LEVEL = Logger.WARNING

    def __init__(self, environment=None):
        super().__init__()
        self.environment = environment
        self.log_file = os.path.join(FileLogger.LOG_DIRECTORY,
                                     self.LOG_FILENAME)
        logger_name = "{}-{}-logger".format(self.__class__.__name__, environment)
        self.log = FullLogger(name=logger_name, level=self.LOG_LEVEL,
                              env=environment)

    @abstractmethod
    def handle_event(self, event_type: str, notification: dict) -> EventResult:
        pass

    @staticmethod
    @abstractmethod
    def listen(self):
        pass
