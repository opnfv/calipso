###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re

from scan.fetchers.cli.cli_fetcher import CliFetcher


# Fetch Interface details from output of 'ip address show' ('ip a show')


class CliFetchInterfaceDetails(CliFetcher):
    def __init__(self):
        super().__init__()
        self.ethtool_attr = re.compile('^\s+([^:]+):\s(.*)$')
        self.regexps = [
            {'name': 'mac_address', 're': '^.*\slink/ether\s(\S+)\s',
             'description': 'MAC address'},
            {'name': 'IP Address', 're': '^\s*inet ([0-9.]+)/',
             'description': 'IP Address v4'},
            {'name': 'IPv6 Address', 're': '^\s*inet6 (\S+) .* global ',
             'description': 'IPv6 Address'}
        ]

    def get_interface_details(self, host_id, interface_name, ip_lines, ethtool_lines) -> dict:
        interface = None
        status_up = None
        for line in [l1 for l1 in ip_lines if l1 != '']:
            tokens = None
            if interface is None:
                tokens = line.split()
                line_remainder = line.split(":")[2].strip()
                interface = {
                    "host": host_id,
                    "index": line[:line.index(":")],
                    "name": interface_name,
                    "local_name": interface_name,
                    "lines": []
                }
                self.handle_line(interface, line_remainder)
                if '<UP,' in line or ',UP,' in line:
                    status_up = True
            if status_up is None:
                if tokens is None:
                    tokens = line.split()
                if 'BROADCAST' in tokens:
                    status_up = 'UP' in tokens
            if interface:
                self.handle_line(interface, line)
        self.set_interface_data(interface, ethtool_lines)
        interface['state'] = 'UP' if status_up else 'DOWN'
        if 'id' not in interface:
            interface['id'] = interface_name + '-unknown_mac'
        return interface

    def handle_line(self, interface, line):
        self.find_matching_regexps(interface, line, self.regexps)
        if 'mac_address' in interface:
            interface["id"] = interface["name"] + "-" + interface["mac_address"]
        interface["lines"].append(line.strip())

    def set_interface_data(self, interface, ethtool_lines):
        if not interface:
            return
        interface["data"] = "\n".join(interface["lines"])
        interface.pop("lines", None)
        attr = None
        for line in ethtool_lines[1:]:
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
