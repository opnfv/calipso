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

    def create_link(self, env, source, source_id, target, target_id,
                    link_type, link_name, state, link_weight,
                    host=None, switch=None,
                    implicit=False,
                    extra_attributes=None):
        if extra_attributes is None:
            extra_attributes = {}
        source_label = extra_attributes.get('source_label', '')
        target_label = extra_attributes.get('target_label', '')
        link = self.inv.create_link(env,
                                    source, source_id, target, target_id,
                                    link_type, link_name, state, link_weight,
                                    implicit=implicit,
                                    source_label=source_label,
                                    target_label=target_label,
                                    host=host, switch=switch,
                                    extra_attributes=extra_attributes)
        if self.inv.monitoring_setup_manager:
            self.inv.monitoring_setup_manager.create_setup(link)
        return link
