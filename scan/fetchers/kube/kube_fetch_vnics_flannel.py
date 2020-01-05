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


class KubeFetchVnicsFlannel(Fetcher):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def get(self, host_id: str) -> list:
        host = self.inv.get_by_id(self.get_env(), host_id)
        if not host:
            self.log.error('Failed to find host {}', host_id)
            return []
        interfaces = [i for i in host['interfaces'] if i['id'].startswith('veth')]
        ret = []
        for interface in interfaces:
            ret.append(self.process_interface(host_id, interface))
        return ret

    def process_interface(self, host_id, interface_details) -> dict:
        interface = dict(vnic_type='container_vnic', host=host_id,
                         containers=[])
        interface['id'] = '{}-{}'.format(host_id, interface_details.pop('id'))
        interface.update(interface_details)
        self.set_folder_parent(interface, 'vnic',
                               master_parent_type='host',
                               master_parent_id=host_id,
                               parent_text='vNICs')
        return interface
