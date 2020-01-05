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

from base.utils.origins import Origin

from base.utils.inventory_mgr import InventoryMgr
from scan.fetchers.cli.cli_fetcher import CliFetcher


class CliFetchVserviceVnics(CliFetcher):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()
        self.if_header = re.compile('^\d+: ([^:]+): (.+)')
        self.regexps = [
            {'name': 'mac_address', 're': '^.*\slink/ether\s(\S+)\s'},
            {'name': 'IP Address', 're': '^\s*inet ([0-9.]+)/'},
            {'name': 'netmask', 're': '^\s*inet [0-9.]+/([0-9]+)'},
            {'name': 'IPv6 Address', 're': '^\s*inet6 ([^/]+)/.* global '}
        ]
        self.ports = None

    def setup(self, env, origin: Origin = None):
        super().setup(env, origin)
        self.ports = {}

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

        if host_id not in self.ports:
            self.ports[host_id] = self.inv.find({"environment": self.get_env(),
                                                 "type": "port",
                                                 "binding:host_id": host_id})

        lines = self.run_fetch_lines("ip netns list", host_id)
        ret = []

        for l in [l for l in lines
                  if l.startswith("qdhcp") or l.startswith("qrouter")]:
            service = l.strip()
            service = service if ' ' not in service \
                else service[:service.index(' ')]
            ret.extend(self.handle_service(host_id, service))
        return ret

    def handle_service(self, host, service, enable_cache=True):
        cmd = "ip netns exec " + service + " ip address show"
        lines = self.run_fetch_lines(cmd, host, enable_cache)
        interfaces = []
        current = None
        for line in lines:
            matches = self.if_header.match(line)
            if matches:
                if current:
                    self.set_vnic_data(current)
                name = matches.group(1).strip(":")
                # ignore 'lo' interface
                if name == 'lo':
                    current = None
                else:
                    line_remainder = matches.group(2)
                    vservice_id = "{}-{}".format(host, service)
                    current = {
                        "vnic_type": "vservice_vnic",
                        "host": host,
                        "object_name": name,
                        "vservice_id": vservice_id,
                        "lines": [],
                        "addresses": []
                    }
                    self.set_folder_parent(current, object_type="vnic",
                                           master_parent_type="vservice",
                                           master_parent_id=vservice_id,
                                           parent_text="vNICs")
                    interfaces.append(current)
                    self.handle_line(current, line_remainder)
            else:
                if current:
                    self.handle_line(current, line)
        if current:
            self.set_vnic_data(current)
        return interfaces

    def handle_line(self, interface, line):
        self.find_matching_regexps(interface, line, self.regexps)
        interface["lines"].append(line.strip())

    def set_vnic_names(self, vnic):
        vnic["id"] = "|".join((vnic["host"], vnic["object_name"]))
        vnic["name"] = "|".join((vnic["object_name"], vnic["mac_address"]))
        vnic["interface_name"] = vnic["object_name"]

    def set_vnic_data(self, vnic):
        self.set_vnic_names(vnic)
        if not vnic or 'IP Address' not in vnic or 'netmask' not in vnic:
            return

        address = {
            "IP Address": vnic.pop("IP Address"),
            "IPv6 Address": vnic.pop("IPv6 Address", None),
            "netmask": self.convert_netmask(vnic.pop("netmask")),
        }
        address["cidr"] = self.get_cidr_for_vnic(address["IP Address"], address["netmask"])

        vnic["addresses"].append(address)
        vnic["data"] = "\n".join(vnic.pop("lines", None))

        port = next((p for p in self.ports.get(vnic["host"], []) if p.get("mac_address") == vnic["mac_address"]), None)
        if port:
            vnic["port"] = port["id"]

        network = self.inv.get_by_field(self.get_env(), "network", "cidrs", address["cidr"], get_single=True)
        if not network:
            return

        vnic["network"] = network["id"]
        # set network for the vservice, to check network on clique creation
        vservice = self.inv.get_by_id(self.get_env(),
                                      vnic["master_parent_id"])
        network_id = network["id"]
        if "network" not in vservice:
            vservice["network"] = list()
        if network_id not in vservice["network"]:
            vservice["network"].append(network_id)
        self.inv.set(vservice)

    # find CIDR string by IP address and netmask
    @classmethod
    def get_cidr_for_vnic(cls, ip_address, netmask):
        ipaddr_parts = ip_address.split('.')
        netmask_parts = netmask.split('.')

        # calculate network start
        net_start = []
        for pos in range(0, 4):
            net_start.append(str(int(ipaddr_parts[pos]) & int(netmask_parts[pos])))

        cidr_string = '.'.join(net_start) + '/'
        cidr_string = cidr_string + cls.get_net_size(netmask_parts)
        return cidr_string

    @staticmethod
    def get_net_size(netmask):
        binary_str = ''
        for octet in netmask:
            binary_str += bin(int(octet))[2:].zfill(8)
        return str(len(binary_str.rstrip('0')))

    @staticmethod
    def convert_netmask(cidr):
        cidr = int(cidr)

        if cidr < 0 or cidr > 32:
            raise ValueError('can\'t convert to netmask: {}'.format(cidr))

        return '.'.join(
            str(sum(2 ** (7 - i) for i in range(0, min(8, max(cidr - part * 8, 0)))))
            for part in range(4)
        )
