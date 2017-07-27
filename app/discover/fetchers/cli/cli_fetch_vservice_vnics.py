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


class CliFetchVserviceVnics(CliAccess):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()
        self.if_header = re.compile('^[-]?(\S+)\s+(.*)$')
        self.regexps = [
            {'name': 'mac_address', 're': '^.*\sHWaddr\s(\S+)(\s.*)?$'},
            {'name': 'mac_address', 're': '^.*\sether\s(\S+)(\s.*)?$'},
            {'name': 'netmask', 're': '^.*\sMask:\s?([0-9.]+)(\s.*)?$'},
            {'name': 'netmask', 're': '^.*\snetmask\s([0-9.]+)(\s.*)?$'},
            {'name': 'IP Address', 're': '^\s*inet addr:(\S+)\s.*$'},
            {'name': 'IP Address', 're': '^\s*inet ([0-9.]+)\s.*$'},
            {'name': 'IPv6 Address',
             're': '^\s*inet6 addr: ?\s*([0-9a-f:/]+)(\s.*)?$'},
            {'name': 'IPv6 Address',
             're': '^\s*inet6 \s*([0-9a-f:/]+)(\s.*)?$'}
        ]

    def get(self, host_id):
        host = self.inv.get_by_id(self.get_env(), host_id)
        if not host:
            self.log.error("host not found: " + host_id)
            return []
        if "host_type" not in host:
            self.log.error("host does not have host_type: " + host_id +
                           ", host: " + str(host))
            return []
        if "Network" not in host["host_type"]:
            return []
        lines = self.run_fetch_lines("ip netns", host_id)
        ret = []
        for l in [l for l in lines
                  if l.startswith("qdhcp") or l.startswith("qrouter")]:
            service = l.strip()
            service = service if ' ' not in service \
                else service[:service.index(' ')]
            ret.extend(self.handle_service(host_id, service))
        return ret

    def handle_service(self, host, service, enable_cache=True):
        cmd = "ip netns exec " + service + " ifconfig"
        lines = self.run_fetch_lines(cmd, host, enable_cache)
        interfaces = []
        current = None
        for line in lines:
            matches = self.if_header.match(line)
            if matches:
                if current:
                    self.set_interface_data(current)
                name = matches.group(1).strip(":")
                # ignore 'lo' interface
                if name == 'lo':
                    current = None
                else:
                    line_remainder = matches.group(2)
                    vservice_id = host + "-" + service
                    current = {
                        "id": host + "-" + name,
                        "type": "vnic",
                        "vnic_type": "vservice_vnic",
                        "host": host,
                        "name": name,
                        "master_parent_type": "vservice",
                        "master_parent_id": vservice_id,
                        "parent_type": "vnics_folder",
                        "parent_id": vservice_id + "-vnics",
                        "parent_text": "vNICs",
                        "lines": []
                    }
                    interfaces.append(current)
                    self.handle_line(current, line_remainder)
            else:
                if current:
                    self.handle_line(current, line)
        if current:
            self.set_interface_data(current)
        return interfaces

    def handle_line(self, interface, line):
        self.find_matching_regexps(interface, line, self.regexps)
        interface["lines"].append(line.strip())

    def set_interface_data(self, interface):
        if not interface or 'IP Address' not in interface or 'netmask' not in interface:
            return

        interface["data"] = "\n".join(interface.pop("lines", None))
        interface["cidr"] = self.get_cidr_for_vnic(interface)
        network = self.inv.get_by_field(self.get_env(), "network", "cidrs",
                                        interface["cidr"], get_single=True)
        if not network:
            return
        interface["network"] = network["id"]
        # set network for the vservice, to check network on clique creation
        vservice = self.inv.get_by_id(self.get_env(),
                                      interface["master_parent_id"])
        network_id = network["id"]
        if "network" not in vservice:
            vservice["network"] = list()
        if network_id not in vservice["network"]:
            vservice["network"].append(network_id)
        self.inv.set(vservice)

    # find CIDR string by IP address and netmask
    def get_cidr_for_vnic(self, vnic):
        if "IP Address" not in vnic:
            vnic["IP Address"] = "No IP Address"
            return "No IP Address"
        ipaddr = vnic["IP Address"].split('.')
        netmask = vnic["netmask"].split('.')

        # calculate network start
        net_start = []
        for pos in range(0, 4):
            net_start.append(str(int(ipaddr[pos]) & int(netmask[pos])))

        cidr_string = '.'.join(net_start) + '/'
        cidr_string = cidr_string + self.get_net_size(netmask)
        return cidr_string

    def get_net_size(self, netmask):
        binary_str = ''
        for octet in netmask:
            binary_str += bin(int(octet))[2:].zfill(8)
        return str(len(binary_str.rstrip('0')))
