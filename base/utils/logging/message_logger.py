###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.utils.logging.logger import Logger
from base.utils.logging.mongo_logging_handler import MongoLoggingHandler
from base.utils.origins import Origin


class MessageLogger(Logger):

    def __init__(self, name: str = None, env: str = None,
                 origin: Origin = None, level: str = None):
        super().__init__(logger_name=name if name else "{}-Message".format(self.PROJECT_NAME),
                         level=level)
        self.env = env
        self.origin = origin
        self.add_handler(MongoLoggingHandler(env=env, origin=self.origin,
                                             level=self.level))

    def set_env(self, env):
        self.env = env

        if self.log.handlers:
            self.log.handlers[0].env = env
        else:
            self.add_handler(MongoLoggingHandler(env, self.level))

    def setup(self, **kwargs):
        env = kwargs.get('env')
        if env and self.env != env:
            self.set_env(env)
