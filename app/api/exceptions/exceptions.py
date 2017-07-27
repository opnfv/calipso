###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from utils.logging.console_logger import ConsoleLogger


class CalipsoApiException(Exception):
    log = ConsoleLogger()

    def __init__(self, status, body="", message=""):
        super().__init__(message)
        self.message = message
        self.status = status
        self.body = body

    @staticmethod
    def handle(ex, req, resp, params):
        CalipsoApiException.log.error(ex.message)
        resp.status = ex.status
        resp.body = ex.body
