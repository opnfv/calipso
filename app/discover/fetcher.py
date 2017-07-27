###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.configuration import Configuration
from utils.logging.full_logger import FullLogger


class Fetcher:

    def __init__(self):
        super().__init__()
        self.env = None
        self.log = FullLogger()
        self.configuration = None

    @staticmethod
    def escape(string):
        return string

    def set_env(self, env):
        self.env = env
        self.log.set_env(env)
        self.configuration = Configuration()

    def get_env(self):
        return self.env

    def get(self, object_id):
        return None
