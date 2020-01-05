###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from scan.fetchers.cli.cli_fetcher import CliFetcher


class CliFetchInterfaceHardwareDetailsVpp(CliFetcher):
    def __init__(self):
        super().__init__()

    def add_hardware_interfaces_details(self, host_id: str, interfaces: list):
        if not interfaces:
            return
        cmd = "vppctl show hardware-interfaces"
        lines = self.run_fetch_lines(cmd, ssh_to_host=host_id)
        for interface in interfaces:
            self.add_hardware_interface_details(interface, lines)

    def add_hardware_interface_details(self, interface: dict, lines: list):
        interface_lines = []
        # find the lines for this interface
        for l in lines:
            details = l.split()
            if not details:
                continue
            if details[0] == interface['name']:
                interface_lines = [lines[0], l]   # headers line & first line
                interface['index'] = details[1]
            elif not interface_lines:
                continue
            elif l.startswith(' '):
                interface_lines.append(l)
                if l.strip().startswith('Ethernet address'):
                    interface['mac_address'] = l.split()[-1]
            else:
                break
        if not interface_lines:
            return
        interface['hardware_details'] = '\n'.join(interface_lines)
