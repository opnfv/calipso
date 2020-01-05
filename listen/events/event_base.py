###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from abc import abstractmethod, ABC

from base.fetcher import Fetcher
from base.utils.inventory_mgr import InventoryMgr
from base.utils.origins import ScanOrigin, ScanOrigins


class EventResult:
    def __init__(self,
                 result: bool, retry: bool = False, message: str = None,
                 related_object: str = None,
                 display_context: str = None):
        self.result = result
        self.retry = retry
        self.message = message
        self.related_object = related_object
        self.display_context = display_context
        self.origin = ScanOrigin(origin_id=None,
                                 origin_type=ScanOrigins.EVENT)


class EventBase(Fetcher, ABC):

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    @abstractmethod
    def handle(self, env, values) -> EventResult:
        pass
