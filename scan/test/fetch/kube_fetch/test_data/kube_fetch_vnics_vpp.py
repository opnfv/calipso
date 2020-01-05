###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from copy import deepcopy

from scan.test.fetch.kube_fetch.test_data.kube_access import HOST_DOC

_INTERFACE_ID = "tap1"
HOST_DOC = deepcopy(HOST_DOC)
HOST_DOC['interfaces'] = {
    _INTERFACE_ID: {
        "lines": [
            "7: {}@if3: <BROADCAST,MULTICAST,UP,LOWER_UP> "
            "mtu 1450 qdisc noqueue master cni0 state UP "
            "mode DEFAULT group default ",
            "    link/ether 66:3d:dc:96:6d:a1 brd ff:ff:ff:ff:ff:ff "
            "link-netnsid 0".format(_INTERFACE_ID)
        ],
        "id": _INTERFACE_ID,
        "mac_address": "66:3d:dc:96:6d:a1",
        "index": "7",
        "state": "UP",
        "mtu": "1450"
    },
    "docker0": {
        "lines": [
            "4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> "
            "mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default ",
            "    link/ether 02:42:c9:9c:d7:5d brd ff:ff:ff:ff:ff:ff"
        ],
        "id": "docker0",
        "mac_address": "02:42:c9:9c:d7:5d",
        "index": "4",
        "state": "DOWN",
        "mtu": "1500"
    },
}

VPPCTL_SHOW_IP_ARP_OUTPUT = [
    "  Time           IP4       Flags      Ethernet              Interface",
    "  1.6414  11.12.13.14    SN          {} {}"
    .format(HOST_DOC['interfaces'][_INTERFACE_ID]['mac_address'],
            _INTERFACE_ID)

]

VPPCTL_SHOW_HARDWARE_INTERFACES_OUTPUT = [
    "    Name                Idx   Link  Hardware",
    "tap1                               4     up   tap1",
    "  Ethernet address 66:3d:dc:96:6d:a1",
    "  VIRTIO interface",
    "     instance 1",
    "vxlan_tunnel0                      5     up   vxlan_tunnel0",
    "  VXLAN",
    "vxlan_tunnel1                      6     up   vxlan_tunnel1"
]

_INTERFACE = HOST_DOC['interfaces'][_INTERFACE_ID]
EXPECTED_VNIC = {
    'id': '{}-{}'.format(HOST_DOC['id'], _INTERFACE_ID),
    'type': 'vnic',
    'name': _INTERFACE_ID,
    'host': HOST_DOC['id'],
    'index': '4',
    'mac_address':  _INTERFACE['mac_address'],
    'parent_id': '{}-vnics'.format(HOST_DOC['id']),
    'parent_type': 'vnics_folder',
    'hardware_details': '\n'.join(VPPCTL_SHOW_HARDWARE_INTERFACES_OUTPUT[:5])
}


def run_fetch_lines_mock(cmd, ssh_to_host=None) -> list:
    if not ssh_to_host:
        pass
    return VPPCTL_SHOW_IP_ARP_OUTPUT \
        if cmd == 'vppctl show ip arp' \
        else VPPCTL_SHOW_HARDWARE_INTERFACES_OUTPUT
