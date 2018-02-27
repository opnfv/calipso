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

from utils.origins import Origin
from utils.logging.logger import Logger
from utils.logging.mongo_logging_handler import MongoLoggingHandler


class FullLogger(Logger):

    def __init__(self, env: str = None, origin: Origin = None,
                 log_file: str = None, level: str = Logger.default_level):
        super().__init__(logger_name="{}-Full".format(self.PROJECT_NAME),
                         level=level)
        self.env = env
        self.origin = origin

        # Console handler
        self.add_handler(logging.StreamHandler())

        # Message handler
        self.add_handler(MongoLoggingHandler(env=env, origin=origin,
                                             level=self.level))

        # File handler
        if log_file:
            self.add_handler(logging.handlers.WatchedFileHandler(log_file))

    def _get_message_handler(self):
        defined_handlers = [h for h in self.log.handlers
                            if isinstance(h, MongoLoggingHandler)]
        return defined_handlers[0] if defined_handlers else None

    # Make sure we update MessageHandler with new env
    def set_env(self, env):
        self.env = env

        handler = self._get_message_handler()
        if handler:
            handler.env = env
        else:
            self.add_handler(MongoLoggingHandler(env, self.level))

    def set_origin(self, origin: Origin):
        self.origin = origin

        handler = self._get_message_handler()
        if handler:
            handler.origin = origin
        else:
            self.add_handler(MongoLoggingHandler(env=self.env,
                                                 level=self.level,
                                                 origin=origin))

    def setup(self, **kwargs):
        env = kwargs.get('env')
        if env and self.env != env:
            self.set_env(env)

        origin = kwargs.get('origin')
        if origin and self.origin != origin:
            self.set_origin(origin)