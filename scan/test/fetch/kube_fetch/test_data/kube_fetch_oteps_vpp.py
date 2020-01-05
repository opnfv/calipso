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

ENVIRONMENT = {
    'name': 'test-env',
    'environment_type': 'Kubernetes',
    'distribution': 'Kubernetes',
    'distribution_version': '1.9',
    'mechanism_drivers': ['Flannel'],
    'type_drivers': 'vxlan'
}

HOST_DOC = deepcopy(HOST_DOC)
HOST_DOC['interfaces'] = {
    'vpp1-92:3f:17:da:ad:fe': {
        'PHYAD': '0',
        'name': 'vpp1',
        'Supports auto-negotiation': 'No',
        'MDI-X': 'Unknown',
        'Advertised pause frame use': 'No',
        'index': '10',
        'Advertised auto-negotiation': 'No',
        'data': '<BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 '
                'qdisc noqueue master cni0 state UP\n'
                '10: vpp1@if3: <BROADCAST,MULTICAST,UP,LOWER_UP> '
                'mtu 1450 qdisc noqueue master cni0 state UP\n'
                'link/ether 92:3f:17:da:ad:fe brd ff:ff:ff:ff:ff:ff '
                'link-netnsid 2\n'
                'inet6 fe80::903f:17ff:feda:adfe/64 scope link\n'
                'valid_lft forever preferred_lft forever',
        'Supported pause frame use': 'No',
        'state': 'UP',
        'IP Address': '1.2.3.4',
        'mac_address': '92:3f:17:da:ad:fe',
        'Advertised link modes': 'Not reported',
        'local_name': 'vpp1',
        'Auto-negotiation': 'off',
        'Port': 'Twisted Pair',
        'Link detected': 'yes',
        'id': 'vpp1-92:3f:17:da:ad:fe',
        'Supported ports': '[ ]',
        'Duplex': 'Full',
        'Transceiver': 'internal',
        'host': 'korlev-kub1',
        'Supported link modes': 'Not reported',
        'Speed': '10000Mb/s'
    },
    'veth939a1f9c-b6:08:92:75:f6:fc': {
        'PHYAD': '0',
        'name': 'veth939a1f9c',
        'Supports auto-negotiation': 'No',
        'MDI-X': 'Unknown',
        'Advertised pause frame use': 'No',
        'index': '9',
        'Advertised auto-negotiation': 'No',
        'data': '<BROADCAST,MULTICAST,UP,LOWER_UP> '
                'mtu 1450 qdisc noqueue master cni0 state UP\n'
                '9: veth939a1f9c@if3: <BROADCAST,MULTICAST,UP,LOWER_UP> '
                'mtu 1450 qdisc noqueue master cni0 state UP\n'
                'link/ether b6:08:92:75:f6:fc brd ff:ff:ff:ff:ff:ff '
                'link-netnsid 1\n'
                'inet6 fe80::b408:92ff:fe75:f6fc/64 scope link\n'
                'valid_lft forever preferred_lft forever',
        'Supported pause frame use': 'No',
        'state': 'UP',
        'mac_address': 'b6:08:92:75:f6:fc',
        'Advertised link modes': 'Not reported',
        'local_name': 'veth939a1f9c',
        'Auto-negotiation': 'off',
        'Port': 'Twisted Pair',
        'Link detected': 'yes',
        'id': 'veth939a1f9c-b6:08:92:75:f6:fc',
        'Supported ports': '[ ]',
        'Duplex': 'Full',
        'Transceiver': 'internal',
        'host': 'korlev-kub1',
        'Supported link modes': 'Not reported',
        'Speed': '10000Mb/s'
    }
}

OTEPS_PARENT = HOST_DOC['id']

OTEPS_LIST = [
    {
        '_id': '5aafe3a189f6e7759a516b63',
        'environment': 'kube-aci',
        'id': 'kub1-aci-otep',
        'type': 'otep',
        'name': 'kub1-aci-otep',
        'overlay_type': 'vxlan',
        'parent_type': 'vedge',
        'ip_address': '172.16.100.1',
        'name_path': '/kube-aci/Hosts/kub1-aci/vEdges/'
                     'kube-flannel-ds-642n5/kub1-aci-otep',
        'host': 'kub1-aci',
        'ports': {
            'vxlan-remote-kub2-aci': {
                'remote_host': 'kub2-aci',
                'options': {
                    'remote_ip': '172.16.100.2',
                    'local_ip': '172.16.100.1'
                },
                'interface': 'vxlan-remote-kub2-aci',
                'name': 'vxlan-remote-kub2-aci',
                'type': 'vxlan'
            },
            'vxlan-remote-kub3-aci': {
                'remote_host': 'kub3-aci',
                'options': {
                    'remote_ip': '172.16.100.3',
                    'local_ip': '172.16.100.1'
                },
                'interface': 'vxlan-remote-kub3-aci',
                'name': 'vxlan-remote-kub3-aci',
                'type': 'vxlan'
            }
        },
        'id_path': '/kube-aci/kube-aci-hosts/kub1-aci/'
                   'kub1-aci-vedges/kub1-aci-vedge/kub1-aci-otep',
        'object_name': 'kub1-aci-otep',
        'parent_id': 'kub1-aci-vedge'
    },
    {
        '_id': '5aafe3a389f6e7759a516bef',
        'environment': 'kube-aci',
        'id': 'kub3-aci-otep',
        'type': 'otep',
        'name': 'kub3-aci-otep',
        'overlay_type': 'vxlan',
        'parent_type': 'vedge',
        'ip_address': '172.16.100.3',
        'name_path': '/kube-aci/Hosts/kub3-aci/'
                     'vEdges/kube-flannel-ds-vhkbl/kub3-aci-otep',
        'host': 'kub3-aci',
        'ports': {
            'vxlan-remote-kub2-aci': {
                'remote_host': 'kub2-aci',
                'options': {
                    'remote_ip': '172.16.100.2',
                    'local_ip': '172.16.100.3'
                },
                'interface': 'vxlan-remote-kub2-aci',
                'name': 'vxlan-remote-kub2-aci',
                'type': 'vxlan'
            },
            'vxlan-remote-kub1-aci': {
                'remote_host': 'kub1-aci',
                'options': {
                    'remote_ip': '172.16.100.1',
                    'local_ip': '172.16.100.3'
                },
                'interface': 'vxlan-remote-kub1-aci',
                'name': 'vxlan-remote-kub1-aci',
                'type': 'vxlan'
            }
        },
        'id_path': '/kube-aci/kube-aci-hosts/kub3-aci/kub3-aci-vedges/'
                   'kub3-aci-vedge/kub3-aci-otep',
        'object_name': 'kub3-aci-otep',
        'parent_id': 'kub3-aci-vedge'
    }
]

EXPECTED_OTEP = {
    'id': '{}-otep'.format(HOST_DOC['id']),
    'name': '{}-otep'.format(HOST_DOC['name']),
    'host': HOST_DOC['id'],
    'parent_id': OTEPS_PARENT,
    'parent_type': 'vedge',
    'ip_address': '1.2.3.4',
    'overlay_type': 'vxlan',
    'overlay_mac_address': '92:3f:17:da:ad:fe',
    'ports': {
        'vxlan-remote-kub1-aci': {
            'name': 'vxlan-remote-kub1-aci',
            'type': 'vxlan',
            'remote_host': 'kub1-aci',
            'interface': 'vxlan-remote-kub1-aci',
            'options': {
                'local_ip': '1.2.3.4',
                'remote_ip': '172.16.100.1'
            }
        },
        'vxlan-remote-kub3-aci': {
            'name': 'vxlan-remote-kub3-aci',
            'type': 'vxlan',
            'remote_host': 'kub3-aci',
            'interface': 'vxlan-remote-kub3-aci',
            'options': {
                'local_ip': '1.2.3.4',
                'remote_ip': '172.16.100.3'
            }
        }
    },
    'udp_port': 8285
}
