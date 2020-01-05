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

    def link_items(self, source: dict=None, target: dict=None,
                   link_type: str=None,
                   link_name: str=None,
                   host: str=None,
                   state: str=None,
                   switch: str=None,
                   extra_attributes: dict=None):
        if not source or not target:
            return
        host = source.get('host', target.get('host')) \
            if host is None \
            else host
        if not link_type:
            link_type = '{}-{}'.format(source['type'], target['type'])
        if not link_name:
            link_name = '{}-{}'.format(source['object_name'],
                                       target['object_name'])
        if not state:
            state = 'up'  # TBD
        link_weight = 0  # TBD
        self.create_link(self.get_env(),
                         source['_id'], source['id'],
                         target['_id'], target['id'],
                         link_type,
                         link_name, state, link_weight,
                         host=host,
                         switch=switch,
                         extra_attributes=extra_attributes)
