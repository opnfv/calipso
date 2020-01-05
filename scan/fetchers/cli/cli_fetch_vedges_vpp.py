###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.utils.inventory_mgr import InventoryMgr
from scan.fetchers.cli.cli_fetcher import CliFetcher


class CliFetchVedgesVpp(CliFetcher):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def get(self, parent_id):
        host_id = parent_id.replace('-vedges', '')
        vedge = {
            'host': host_id,
            'id': host_id + '-VPP',
            'name': 'VPP-' + host_id,
            'agent_type': 'VPP',
            'vedge_type': 'VPP'
        }
        ver = self.run_fetch_lines('vppctl show ver', host_id)
        if ver:
            ver = ver[0]
            vedge['binary'] = ver[:ver.index(' ', ver.index(' ') + 1)]
        host = self.inv.get_by_id(self.get_env(), host_id)
        if not host:
            self.log.error("unable to find host in inventory: %s", host_id)
            return []
        host_types = host["host_type"]
        if "Network" not in host_types and "Compute" not in host_types:
            return []
        interfaces = self.run_fetch_lines('vppctl show int', host_id)
        vedge['ports'] = self.fetch_ports(interfaces)
        self.set_folder_parent(vedge, 'vedge', parent_text='vEdges',
                               master_parent_type='host',
                               master_parent_id=host_id)
        return [vedge]

    @staticmethod
    def fetch_ports(interfaces):
        ports = []
        for i in interfaces:
            if not i or i.startswith(' '):
                continue
            parts = i.split()
            port = {
                'id': parts[1],
                'state': parts[2],
                'name': parts[0]
            }
            ports.append(port)
        return ports
