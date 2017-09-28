###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from collections import deque

from discover.fetchers.cli.cli_access import CliAccess
from utils.inventory_mgr import InventoryMgr


class CliFetchBondHostPnics(CliAccess):
    BOND_DIR = '/proc/net/bonding/'
    SLAVE_INTERFACE_HEADER = 'Slave Interface: '

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def get(self, parent_id: str):
        self.log.info('CliFetchBondHostPnics: checking under {}'
                      .format(parent_id))
        host_id = parent_id[:parent_id.rindex('-')]
        cmd = 'ls -1 {} 2>&1'.format(self.BOND_DIR)
        host = self.inv.get_by_id(self.get_env(), host_id)
        if not host:
            self.log.error('CliFetchBondHostPnics: host not found: ' + host_id)
            return []
        host_types = host['host_type']
        if 'Network' not in host_types and 'Compute' not in host_types:
            return []
        lines = self.run_fetch_lines(cmd, host_id)
        if lines and 'No such file or directory' in lines[0]:
            return []  # no bonds so directory does not exist
        bonds = []
        for line in lines:
            bond = self.get_bond_details(host_id, line)
            if bond:
                bonds.append(bond)
        return bonds

    def get_bond_details(self, host_id: str, interface_name: str) -> dict:
        lines = self.run_fetch_lines('cat {}{}'
                                     .format(self.BOND_DIR, interface_name),
                                     host_id)
        status, mac_address = \
            self.get_bond_status_and_mac_address(host_id, interface_name)
        interface_id = '{}-{}'.format(interface_name, mac_address)
        interface = {
            'host': host_id,
            'name': interface_name,
            'id': interface_id,
            'local_name': interface_name,
            'mac_address': mac_address,
            'Link detected': 'yes' if status == 'up' else 'no',
            'EtherChannel': True,
            'EtherChannel Master': '',
            'members': {}
        }
        # keep stack of info objects to support multi-level info
        info_objects = deque([interface])
        for line in [line for line in lines if line != '']:
            if line.startswith(self.SLAVE_INTERFACE_HEADER):
                name = line[line.index(':')+1:].strip()
                slave = {
                    'name': name,
                    'EtherChannel Master': interface_id
                }
                # remove any pending info objects, keep only interface
                info_objects = deque([interface])
                info_objects.append(slave)
                interface['members'][name] = slave
            elif line.rstrip(':').lower().endswith('info'):
                # move to lower level info object
                info_name = line.rstrip(':')
                upper_info_obj = info_objects[-1]
                info_obj = {}
                upper_info_obj[info_name] = info_obj
                info_objects.append(info_obj)
            else:
                self.get_attribute_from_line(info_objects[-1], line)
        for slave in list(interface['members'].values()):
            self.set_slave_host_pnic_bond_attributes(host_id, slave,
                                                     interface_id)
        return interface

    def get_bond_status_and_mac_address(self, host_id: str, name: str):
        output = self.run_fetch_lines('ip link show {}'.format(name), host_id)
        status_line = output[0]
        status = status_line[status_line.index(' state ') + len(' state '):]
        status = status[:status.index(' ')]
        matches = [line.strip() for line in output if 'link/ether' in line]
        if not matches:
            self.log.error('Failed to find line with MAC address '
                           'for bond {} (host: {})'
                           .format(name, host_id))
        tokens = matches[0].split()
        if len(tokens) < 2:
            self.log.error('Failed to find MAC address in line: {}'
                           .format(matches[0]))
        mac_address = tokens[1]
        return status.lower(), mac_address

    def get_attribute_from_line(self, obj: dict, line: str):
        if ':' not in line:
            self.log.error('object {}: failed to find ":" in line: {}'
                           .format(obj['name'], line))
            return
        attr = line[:line.index(':')]
        value = line[len(attr)+1:]
        obj[attr.strip()] = value.strip()

    def set_slave_host_pnic_bond_attributes(self, host, slave, interface_id):
        pnic = self.inv.find_one({
            'environment': self.get_env(),
            'host': host,
            'type': 'host_pnic',
            'name': slave['name']
        })
        if not pnic:
            self.log.error('unable to find slave pNIC {} under bond {}'
                           .format(slave_id, interface_id))
            return
        mac_address = pnic['mac_address']
        slave_id = '{}-{}'.format(slave.get('name', ''), mac_address)
        slave['mac_address'] = mac_address
        slave['id'] = slave_id
        pnic['EtherChannel'] = True
        pnic['EtherChannel Master'] = interface_id
        self.inv.set(pnic)
