###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import logging.handlers

from base.utils.logging.logger import Logger


class FileLogger(Logger):

    LOG_DIRECTORY = "/var/log/calipso/"

    def __init__(self, log_file: str, name: str = None,
                 level: str = Logger.default_level):
        super().__init__(logger_name=name if name else "{}-File".format(self.PROJECT_NAME),
                         level=level)
        self.add_handler(logging.handlers.WatchedFileHandler(log_file))

