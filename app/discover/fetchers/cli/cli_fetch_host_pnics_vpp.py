###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re

from discover.fetchers.cli.cli_access import CliAccess
from utils.inventory_mgr import InventoryMgr

NAME_RE = '^[a-zA-Z]*GigabitEthernet'
MAC_FIELD_RE = '^.*\sEthernet address\s(\S+)(\s.*)?$'

class CliFetchHostPnicsVpp(CliAccess):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()
        self.name_re = re.compile(NAME_RE)

    def get(self, id):
        host_id = id[:id.rindex("-")]
        host_id = id[:host_id.rindex("-")]
        vedges = self.inv.find_items({
            "environment": self.get_env(),
            "type": "vedge",
            "host": host_id
        })
        ret = []
        for vedge in vedges:
            pnic_ports = vedge['ports']
            for pnic_name in pnic_ports:
                if not self.name_re.search(pnic_name):
                    continue
                pnic = pnic_ports[pnic_name]
                pnic['host'] = host_id
                pnic['id'] = host_id + "-pnic-" + pnic_name
                pnic['type'] = 'host_pnic'
                pnic['object_name'] = pnic_name
                self.get_pnic_mac_address(pnic)
                pnic['Link detected'] = 'yes' if pnic['state'] == 'up' else 'no'
                ret.append(pnic)
        return ret

    def get_pnic_mac_address(self, pnic):
        cmd = 'vppctl show hardware-interfaces {}'.format(pnic['object_name'])
        output_lines = self.run_fetch_lines(cmd, ssh_to_host=pnic['host'])
        if output_lines:
            regexps = [{'name': 'mac_address', 're': MAC_FIELD_RE}]
            for line in output_lines:
                self.find_matching_regexps(pnic, line, regexps)
                if 'mac_address' in pnic:
                    break
