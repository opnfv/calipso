###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from abc import abstractmethod, ABCMeta

from base.utils.inventory_mgr import InventoryMgr
from base.utils.singleton import Singleton
from scan.fetchers.cli.cli_fetcher import CliFetcher


class ABCSingleton(ABCMeta, Singleton):
    pass


class CliFetchVconnectors(CliFetcher, metaclass=ABCSingleton):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    @abstractmethod
    def get_vconnectors(self, host):
        raise NotImplementedError("Subclass must override get_vconnectors()")

    def get(self, id):
        host_id = id[:id.rindex('-')]
        host = self.inv.get_by_id(self.get_env(), host_id)
        if not host:
            self.log.error("CliFetchVconnectors: host not found: " + host_id)
            return []
        if "host_type" not in host:
            self.log.error("host does not have host_type: " + host_id +
                           ", host: " + str(host))
            return []
        return self.get_vconnectors(host)
