###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import abc

from base.utils.inventory_mgr import InventoryMgr


class ValidatorBase(metaclass=abc.ABCMeta):
    def __init__(self, env):
        self.env = env
        self.inv = InventoryMgr()

    @abc.abstractmethod
    def run(self) -> (bool, list):
        return True, []
