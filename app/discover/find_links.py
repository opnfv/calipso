###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetcher import Fetcher
from utils.inventory_mgr import InventoryMgr


class FindLinks(Fetcher):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def create_link(self, env, host, source, source_id, target, target_id,
                    link_type, link_name, state, link_weight,
                    source_label="", target_label="",
                    extra_attributes=None):
        if extra_attributes is None:
            extra_attributes = {}
        link = self.inv.create_link(env, host,
                                    source, source_id, target, target_id,
                                    link_type, link_name, state, link_weight,
                                    extra_attributes=extra_attributes)
        if self.inv.monitoring_setup_manager:
            self.inv.monitoring_setup_manager.create_setup(link)
