###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
VEDGE_ID = "3858e121-d861-4348-9d64-a55fcd5bf60a"
VEDGE = {
    "configurations": {
        "tunnel_types": [
            "vxlan"
        ],
        "tunneling_ip": "192.168.2.1"
    },
    "host": "node-5.cisco.com",
    "id": "3858e121-d861-4348-9d64-a55fcd5bf60a",
    "tunnel_ports": {
        "vxlan-c0a80203": {
        }, 
        "br-tun": {
        }
    }, 
    "type": "vedge"
}
VEDGE_WITHOUT_CONFIGS = {

}
VEDGE_WITHOUT_TUNNEL_TYPES = {
    "configuration": {
        "tunnel_types": ""
    }
}
NON_ICEHOUSE_CONFIGS = {
    "distribution": "Mirantis",
    "distribution_version": "8.0"
}
ICEHOUSE_CONFIGS = {
    "distribution": "Canonical",
    "distribution_version": "icehouse"
}
HOST = {
    "host": "node-5.cisco.com",
    "id": "node-5.cisco.com",
    "ip_address": "192.168.0.4",
    "name": "node-5.cisco.com"
}
OTEPS_WITHOUT_CONFIGURATIONS_IN_VEDGE_RESULTS = []
OTEPS_WITHOUT_TUNNEL_TYPES_IN_VEDGE_RESULTS = []
OTEPS_FOR_NON_ICEHOUSE_DISTRIBUTION_RESULTS = [
    {
        "host": "node-5.cisco.com",
        "ip_address": "192.168.2.1",
        "udp_port": 4789,
        "id": "node-5.cisco.com-otep",
        "name": "node-5.cisco.com-otep",
        "overlay_type": "vxlan",
        "ports": {
            "vxlan-c0a80203": {
            },
            "br-tun": {
            }
        }
    }
]
OTEPS_FOR_ICEHOUSE_DISTRIBUTION_RESULTS = [
    {
        "host": "node-5.cisco.com",
        "ip_address": "192.168.0.4",
        "id": "node-5.cisco.com-otep",
        "name": "node-5.cisco.com-otep",
        "overlay_type": "vxlan",
        "ports": {
            "vxlan-c0a80203": {
            },
            "br-tun": {
            }
        },
        "udp_port": "67"
    }
]

OTEPS = [
    {
        "host": "node-5.cisco.com",
        "ip_address": "192.168.2.1",
        "udp_port": 4789
    }
]

OTEP_FOR_GETTING_VECONNECTOR = {
        "host": "node-5.cisco.com",
        "ip_address": "192.168.2.1",
        "udp_port": 4789,
        "id": "node-5.cisco.com-otep",
        "name": "node-5.cisco.com-otep",
        "overlay_type": "vxlan",
        "ports": {
            "vxlan-c0a80203": {
            },
            "br-tun": {
            }
        }
}
HOST_ID = "node-5.cisco.com"
IP_ADDRESS_SHOW_LINES = [
    "2: br-mesh: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc "
    "pfifo_fast state UP group default qlen 1000",
    "    link/ether 00:50:56:ac:28:9d brd ff:ff:ff:ff:ff:ff",
    "    inet 192.168.2.1/24 brd 192.168.2.255 scope global br-mesh",
    "       valid_lft forever preferred_lft forever",
    "    inet6 fe80::d4e1:8fff:fe33:ed6a/64 scope global mngtmpaddr dynamic",
    "       valid_lft 2591951sec preferred_lft 604751sec"
]

OTEP_WITH_CONNECTOR = {
    "host": "node-5.cisco.com",
    "ip_address": "192.168.2.1",
    "udp_port": 4789,
    "id": "node-5.cisco.com-otep",
    "name": "node-5.cisco.com-otep",
    "overlay_type": "vxlan",
    "ports": {
        "vxlan-c0a80203": {
        },
        "br-tun": {
        }
    },
    "vconnector": "br-mesh"
}
