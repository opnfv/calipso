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

from base.utils.inventory_mgr import InventoryMgr
from scan.fetchers.cli.cli_fetch_interface_hardware_details_vpp \
    import CliFetchInterfaceHardwareDetailsVpp
from scan.fetchers.cli.cli_fetcher import CliFetcher

NAME_RE = '^\w*(?<!Virtual)Ethernet'
MAC_FIELD_RE = '^.*\sEthernet address\s(\S+)(\s.*)?$'
PNIC_WITH_NETWORK_RE = '.*\.([0-9]+)$'


class CliFetchHostPnicsVpp(CliFetcher):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()
        self.name_re = re.compile(NAME_RE)
        self.pnic_with_network_re = re.compile(PNIC_WITH_NETWORK_RE)
        self.if_details_fetcher = CliFetchInterfaceHardwareDetailsVpp()

    def set_env(self, env):
        super().set_env(env)
        self.if_details_fetcher.set_env(env)

    def get(self, parent_id):
        host_id = parent_id[:parent_id.rindex("-")]
        host_id = parent_id[:host_id.rindex("-")]
        vedges = self.inv.find_items({
            "environment": self.get_env(),
            "type": "vedge",
            "host": host_id
        })
        ret = []
        for vedge in vedges:
            pnic_ports = vedge['ports']
            for pnic in pnic_ports:
                pnic_name = pnic['name']
                if not self.name_re.search(pnic_name):
                    continue
                pnic['host'] = host_id
                pnic['id'] = host_id + "-pnic-" + pnic_name
                pnic['IP Address'] = ''
                pnic['type'] = 'host_pnic'
                pnic['object_name'] = pnic_name
                pnic['Link detected'] = 'yes' if pnic['state'] == 'up' else 'no'
                self.add_pnic_network(pnic)
                self.set_folder_parent(pnic, object_type='pnic',
                                       master_parent_type='host',
                                       master_parent_id=host_id,
                                       parent_text='pNICs')
                ret.append(pnic)
        self.if_details_fetcher.add_hardware_interfaces_details(host_id, ret)
        self.add_pnic_ip_addresses(host_id, ret)
        self.add_interfaces_bond_details(host_id, ret)
        return ret

    def add_pnic_ip_addresses(self, host_id, pnics: list):
        is_vpp = 'VPP' in self.configuration.environment['mechanism_drivers']
        is_vlan = self.configuration.environment['type_drivers'] == 'vlan'
        if is_vpp and is_vlan:
            return

        cmd = 'vppctl show int addr'
        lines = self.run_fetch_lines(cmd, host_id)
        for pnic in pnics:
            self.add_pnic_ip_address(pnic, lines)

    def add_pnic_ip_address(self, pnic, lines: list):
        for pos in range(0, len(lines)-2):
            line = lines[pos]
            pnic_name = pnic['name']
            if line.startswith('{} '.format(pnic_name)):
                self.log.debug('found IP address for pnic {}'.format(pnic_name))
                ip_address = lines[pos+1].strip()
                # remove netmask after '/'
                if '/' in ip_address:
                    ip_address = ip_address[:ip_address.index('/')]
                pnic['IP Address'] = ip_address

    def add_pnic_network(self, pnic):
        name_match = re.match(self.pnic_with_network_re, pnic['name'])
        if not name_match:
            return

        segment_id = int(name_match.groups()[0])
        network = self.inv.find_one({
            'type': 'network',
            'provider:segmentation_id': segment_id,
            'provider:network_type': 'vlan'
        })
        if not network:
            return

        pnic.update({
            'network': network['id'],
            'network_name': network['name'],
            'network_type': network['provider:network_type']
        })

    def add_interfaces_bond_details(self, host_id: str, interfaces: list):
        cmd = 'vppctl show bond'
        lines = self.run_fetch_lines(cmd, host_id)
        bond_keys = ["bond_master_interface", "sw_if_index", "mode", "local_balance", "active_slaves", "slaves"]
        bond_details = {}
        for line in lines:
            if "Bond" in line:
                bond_values = line.split()
                bond_details = dict(zip(bond_keys, bond_values))
        cmd = 'vppctl show bond details'
        lines = self.run_fetch_lines(cmd, host_id)
        members = []
        for interface in interfaces:
            for line in lines:
                if interface["name"] in line:
                    if "Bond" not in interface["name"]:
                        existing_member = next((member for member in members if member.get("name") == interface["name"]), None)
                        if not existing_member:
                            members.append({"name": interface["name"]})
                    interface["EtherChannel"] = True
                    interface["EtherChannel Master"] = bond_details["bond_master_interface"]
                    interface["EtherChannel Config"] = bond_details
                    details_cmd = 'vppctl show lacp details {} | grep -v "{}"'.format(interface["name"], interface["name"])
                    interface["EtherChannel Runtime"] = {"lines": self.run_fetch_lines(details_cmd, host_id)}
            interface["members"] = members




