###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import logging
import logging.handlers

from utils.logging.logger import Logger
from utils.logging.mongo_logging_handler import MongoLoggingHandler


class FullLogger(Logger):

    def __init__(self, env: str = None, log_file: str = None,
                 level: str = Logger.default_level):
        super().__init__(logger_name="{}-Full".format(self.PROJECT_NAME),
                         level=level)

        # Console handler
        self.add_handler(logging.StreamHandler())

        # Message handler
        self.add_handler(MongoLoggingHandler(env, self.level))

        # File handler
        if log_file:
            self.add_handler(logging.handlers.WatchedFileHandler(log_file))

    # Make sure we update MessageHandler with new env
    def set_env(self, env):
        super().set_env(env)

        defined_handler = [h for h in self.log.handlers
                           if isinstance(h, MongoLoggingHandler)]
        if defined_handler:
            defined_handler[0].env = env
        else:
            self.add_handler(MongoLoggingHandler(env, self.level))
