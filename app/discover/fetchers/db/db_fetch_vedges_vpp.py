###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.cli.cli_access import CliAccess
from discover.fetchers.db.db_access import DbAccess
from utils.inventory_mgr import InventoryMgr
from utils.singleton import Singleton


class DbFetchVedgesVpp(DbAccess, CliAccess, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def get(self, id):
        host_id = id[:id.rindex('-')]
        vedge = {
            'host': host_id,
            'id': host_id + '-VPP',
            'name': 'VPP-' + host_id,
            'agent_type': 'VPP'
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
        return [vedge]

    def fetch_ports(self, interfaces):
        ports = {}
        for i in interfaces:
            if not i or i.startswith(' '):
                continue
            parts = i.split()
            port = {
                'id': parts[1],
                'state': parts[2],
                'name': parts[0]
            }
            ports[port['name']] = port
        return ports
