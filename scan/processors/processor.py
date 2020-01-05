###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.fetcher import Fetcher
from base.utils.inventory_mgr import InventoryMgr


class Processor(Fetcher):

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def run(self):
        self.log.info("Running processor: {}".format(self.__class__.__name__))

    def find_by_type(self, object_type):
        return self.inv.find_items({"environment": self.env, "type": object_type})
