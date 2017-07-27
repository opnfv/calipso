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
VEDGE_WITHOUT_CONFIGS ={

}
VEDGE_WITHOUT_TUNNEL_TYPES = {
    "configuration": {
        "tunnel_types": ""
    }
}
NON_ICEHOUSE_CONFIGS = {
    "distribution": "Mirantis-8.0"
}
ICEHOUSE_CONFIGS = {
    "distribution": "Canonical-icehouse"
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
IFCONFIG_LINES = [
    "br-mesh   Link encap:Ethernet  HWaddr 00:50:56:ac:28:9d  ",
    "          inet addr:192.168.2.1  Bcast:192.168.2.255  Mask:255.255.255.0",
    "          inet6 addr: fe80::d4e1:8fff:fe33:ed6a/64 Scope:Link",
    "          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1",
    "          RX packets:2273307 errors:0 dropped:0 overruns:0 frame:0",
    "          TX packets:2255930 errors:0 dropped:0 overruns:0 carrier:0",
    "          collisions:0 txqueuelen:0 ",
    "          RX bytes:578536155 (578.5 MB)  TX bytes:598541522 (598.5 MB)",
    ""
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
