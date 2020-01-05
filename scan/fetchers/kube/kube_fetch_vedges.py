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


class KubeFetchVedges(Fetcher):

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def get(self, host_id) -> list:
        ret = []
        host = self.inv.get_by_id(self.get_env(), host_id)
        if not host:
            self.log.error('failed to find host: {}'.format(host_id))
            return ret
        search_condition = {
            'environment': self.get_env(),
            'type': 'pod',
            'host': host['name'],
            # the following allows matching by several labels, tested:
            '$or': [{"labels.k8s-app": "flannel"}, {"labels.app": "flannel"}]
        }
        vedges = self.inv.find_items(search_condition)
        for o in vedges:
            o['id'] = '{}-vedge'.format(host_id)
            o['host'] = host_id
            o['agent_type'] = 'Flannel agent'
            self.set_folder_parent(o,
                                   object_type='vedge',
                                   master_parent_type='host',
                                   master_parent_id=host_id,
                                   parent_objects_name='vedges',
                                   parent_text='vEdges')
            ret.append(o)
        return ret
