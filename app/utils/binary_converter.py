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


class BinaryConverter:

    def __init__(self):
        super().__init__()
        self.log = ConsoleLogger()

    def binary2str(self, txt):
        if not isinstance(txt, bytes):
            return str(txt)
        try:
            s = txt.decode("utf-8")
        except TypeError:
            s = str(txt)
        return s

