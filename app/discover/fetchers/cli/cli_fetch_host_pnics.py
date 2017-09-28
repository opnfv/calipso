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


class CliFetchHostPnics(CliAccess):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()
        self.ethtool_attr = re.compile('^\s+([^:]+):\s(.*)$')
        self.regexps = [
            {'name': 'mac_address', 're': '^.*\sHWaddr\s(\S+)(\s.*)?$',
             'description': 'MAC address with HWaddr'},
            {'name': 'mac_address', 're': '^.*\sether\s(\S+)(\s.*)?$',
             'description': 'MAC address with ether'},
            {'name': 'IP Address', 're': '^\s*inet addr:?(\S+)\s.*$',
             'description': 'IP Address with "inet addr"'},
            {'name': 'IP Address', 're': '^\s*inet ([0-9.]+)\s.*$',
             'description': 'IP Address with "inet"'},
            {'name': 'IPv6 Address', 're': '^\s*inet6 addr:\s*(\S+)(\s.*)?$',
             'description': 'IPv6 Address with "inet6 addr"'},
            {'name': 'IPv6 Address', 're': '^\s*inet6 \s*(\S+)(\s.*)?$',
             'description': 'IPv6 Address with "inet6"'}
        ]

    def get(self, id):
        host_id = id[:id.rindex("-")]
        cmd = 'ls -l /sys/class/net | grep ^l | grep -v "/virtual/"'
        host = self.inv.get_by_id(self.get_env(), host_id)
        if not host:
            self.log.error("CliFetchHostPnics: host not found: " + host_id)
            return []
        if "host_type" not in host:
            self.log.error("host does not have host_type: " + host_id +
                           ", host: " + str(host))
            return []
        host_types = host["host_type"]
        if "Network" not in host_types and "Compute" not in host_types:
            return []
        interface_lines = self.run_fetch_lines(cmd, host_id)
        interfaces = []
        for line in interface_lines:
            interface_name = line[line.rindex('/')+1:]
            interface_name = interface_name.strip()
            # run ifconfig with specific interface name,
            # since running it with no name yields a list without inactive pNICs
            interface = self.find_interface_details(host_id, interface_name)
            if interface:
                interfaces.append(interface)
        return interfaces

    def find_interface_details(self, host_id, interface_name):
        lines = self.run_fetch_lines("ifconfig " + interface_name, host_id)
        interface = None
        status_up = None
        for line in [l for l in lines if l != '']:
            tokens = None
            if interface is None:
                tokens = line.split()
                line_remainder = line.strip('-')[len(interface_name)+2:]
                line_remainder = line_remainder.strip(' :')
                interface = {
                    "host": host_id,
                    "name": interface_name,
                    "local_name": interface_name,
                    "lines": []
                }
                self.handle_line(interface, line_remainder)
                if '<UP,' in line:
                    status_up = True
            if status_up is None:
                if tokens is None:
                    tokens = line.split()
                if 'BROADCAST' in tokens:
                    status_up = 'UP' in tokens
            if interface:
                self.handle_line(interface, line)
        self.set_interface_data(interface)
        interface['state'] = 'UP' if status_up else 'DOWN'
        if 'id' not in interface:
            interface['id'] = interface_name + '-unknown_mac'
        return interface

    def handle_line(self, interface, line):
        self.find_matching_regexps(interface, line, self.regexps)
        if 'mac_address' in interface:
            interface["id"] = interface["name"] + "-" + interface["mac_address"]
        interface["lines"].append(line.strip())

    def set_interface_data(self, interface):
        if not interface:
            return
        interface["data"] = "\n".join(interface["lines"])
        interface.pop("lines", None)
        ethtool_ifname = interface["local_name"]
        if "@" in interface["local_name"]:
            pos = interface["local_name"].index("@")
            ethtool_ifname = ethtool_ifname[pos + 1:]
        cmd = "ethtool " + ethtool_ifname
        lines = self.run_fetch_lines(cmd, interface["host"])
        attr = None
        for line in lines[1:]:
            matches = self.ethtool_attr.match(line)
            if matches:
                # add this attribute to the interface
                attr = matches.group(1)
                value = matches.group(2)
                interface[attr] = value.strip()
            else:
                # add more values to the current attribute as an array
                if isinstance(interface[attr], str):
                    interface[attr] = [interface[attr], line.strip()]
                else:
                    interface[attr].append(line.strip())
