###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.cli.cli_fetch_vconnectors import CliFetchVconnectors


class CliFetchVconnectorsVpp(CliFetchVconnectors):
    def __init__(self):
        super().__init__()

    def get_vconnectors(self, host):
        lines = self.run_fetch_lines("vppctl show mode", host['id'])
        vconnectors = {}
        for l in lines:
            if not l.startswith('l2 bridge'):
                continue
            line_parts = l.split(' ')
            name = line_parts[2]
            bd_id = line_parts[4]
            if bd_id in vconnectors:
                vconnector = vconnectors[bd_id]
            else:
                vconnector = {
                    'host': host['id'],
                    'id': host['id'] + '-vconnector-' + bd_id,
                    'bd_id': bd_id,
                    'name': "bridge-domain-" + bd_id,
                    'interfaces': {},
                    'interfaces_names': []
                }
                vconnectors[bd_id] = vconnector
            interface = self.get_interface_details(host, name)
            if interface:
                vconnector['interfaces'][name] = interface
                vconnector['interfaces_names'].append(name)
        return list(vconnectors.values())

    def get_interface_details(self, host, name):
        # find vconnector interfaces
        cmd = "vppctl show hardware-int " + name
        interface_lines = self.run_fetch_lines(cmd, host['id'])
        # remove header line
        interface_lines.pop(0)
        interface = None
        for l in interface_lines:
            if not l.strip():
                continue  # ignore empty lines
            if not l.startswith(' '):
                details = l.split()
                interface = {
                    "name": details[0],
                    "hardware": details[3],
                    "state": details[2],
                    "id": details[1],
                }
            elif l.startswith('  Ethernet address '):
                interface['mac_address'] = l[l.rindex(' ') + 1:]
        return interface
