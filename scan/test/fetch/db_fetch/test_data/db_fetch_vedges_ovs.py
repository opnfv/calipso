###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
VEDGES_FOLDER_ID = "node-6.cisco.com-vedges"

OBJECTS_FROM_DB = [
    {
        "host": "node-6.cisco.com",
        "agent_type": "Open vSwitch agent",
        "configurations": '{"tunneling_ip": "192.168.2.3"}',
    }
]

HOST = {
    "host": "node-6.cisco.com",
    "host_type": [
        "Controller", 
        "Network"
    ],
    "id": "node-6.cisco.com",
    "name": "node-6.cisco.com"
}

HOST_WITHOUT_REQUIRED_HOST_TYPES = {
    "id": "node-6.cisco.com",
    "host_type": []
}

PORTS = {
    "ovs-system": {
        "name": "ovs-system",
        "id": "0",
        "internal": True
    },
    "qr-bb9b8340-72": {
        "name": "qr-bb9b8340-72",
        "id": "1",
        "internal": True,
        "tag": "3"
    },
    "qr-8733cc5d-b3": {
        "name": "qr-8733cc5d-b3",
        "id": "2",
        "internal": True,
        "tag": "4"
    }
}

TUNNEL_PORTS = {
    "patch-int": {
        "interface": "patch-int",
        "name": "patch-int",
        "options": {
            "peer": "patch-tun"
        },
        "type": "patch"
    }
}

GET_RESULTS = [
    {
        'name': 'node-6.cisco.com-OVS',
        'host': 'node-6.cisco.com',
        'agent_type': 'Open vSwitch agent',
        'configurations': {"tunneling_ip": "192.168.2.3"},
        'ports': PORTS,
        'tunnel_ports': TUNNEL_PORTS
    }
]


VSCTL_LINES = [
    "3b12f08e-4e13-4976-8da5-23314b268805",
    "    Bridge br-int",
    "        fail_mode: secure",
    "        Port \"qr-bb9b8340-72\"",
    "            tag: 3",
    "            Interface \"qr-bb9b8340-72\"",
    "                type: internal",
    "        Port \"qr-8733cc5d-b3\"",
    "            tag: 4",
    "            Interface \"qr-8733cc5d-b3\"",
    "                type: internal",
    "    Bridge br-tun",
    "        fail_mode: secure",
    "        Port patch-int",
    "            Interface patch-int",
    "                type: patch",
    "                options: {peer=patch-tun}",
]

DPCTL_LINES = [
    "system@ovs-system:",
    "\tlookups: hit:14039304 missed:35687906 lost:0",
    "\tflows: 4",
    "\tmasks: hit:95173613 total:2 hit/pkt:1.91",
    "\tport 0: ovs-system (internal)",
    "\tport 1: qr-bb9b8340-72 (internal)",
    "\tport 2: qr-8733cc5d-b3 (internal)"
]

DPCTL_RESULTS = {
    "ovs-system": {
        "name": "ovs-system",
        "id": "0",
        "internal": True
    },
    "qr-bb9b8340-72": {
        "name": "qr-bb9b8340-72",
        "id": "1",
        "internal": True
    },
    "qr-8733cc5d-b3": {
        "name": "qr-8733cc5d-b3",
        "id": "2",
        "internal": True
    }
}

FETCH__PORT_TAGS_INPUT = {
    "ovs-system": {
        "name": "ovs-system",
        "id": "0",
        "internal": True
    },
    "qr-bb9b8340-72": {
        "name": "qr-bb9b8340-72",
        "id": "1",
        "internal": True
    },
    "qr-8733cc5d-b3": {
        "name": "qr-8733cc5d-b3",
        "id": "2",
        "internal": True
    }
}

FETCH_PORT_TAGS_RESULT = {
    "ovs-system": {
        "name": "ovs-system",
        "id": "0",
        "internal": True
    },
    "qr-bb9b8340-72": {
        "name": "qr-bb9b8340-72",
        "id": "1",
        "internal": True,
        "tag": "3"
    },
    "qr-8733cc5d-b3": {
        "name": "qr-8733cc5d-b3",
        "id": "2",
        "internal": True,
        "tag": "4"
    }
}

DOC_TO_GET_OVERLAY = {
    "host": "node-6.cisco.com",
    "agent_type": "Open vSwitch agent",
    "configurations": {"tunneling_ip": "192.168.2.3"},
}

LIST_IFACES_LINES = [
    "eth0",
    "p",
    "t"
]
LIST_IFACES_NAMES = LIST_IFACES_LINES
LIST_IFACES_LINES_MIRANTIS = {
    "eth0--br-eth0",
    "phy-eth0"
}
LIST_IFACES_NAMES_MIRANTIS = ["eth0"]

VEDGE_CONFIGURATIONS_MIRANTIS = {
    "bridge_mappings": {
        "br-prv": "eth0"
    }
}
VEDGE_CONFIGURATIONS = {
    "bridge_mappings": {
        "physnet1": "eth0",
        "physnet2": "p",
        "physnet3": "t",
        "physnet4": "p",
        "physnet5": "p"
    }
}

VEDGE_MIRANTIS = {
    'host': HOST['host'],
    'ports': {
        "eth0": {"name": "eth0", "id": "eth0-port_id"}
    },
    'configurations': VEDGE_CONFIGURATIONS_MIRANTIS
}
VEDGE = {
    'host': HOST['host'],
    'ports': {
        "eth0": {"name": "eth0", "id": "eth0-port_id"},
        "p": {"name": "p", "id": "p-port_id"},
        "t": {"name": "t", "id": "t-port_id"}
    },
    'configurations': VEDGE_CONFIGURATIONS
}

ANOTHER_DIST = "another distribution"

PNICS_MIRANTS = {
    "eth0": {"name": "eth0", "mac_address": "eth0 mac_address"}
}
PNICS = {
    "eth0": {"name": "eth0", "mac_address": "eth0 mac_address"},
    "p": {"name": "p", "mac_address": "p mac_address"},
    "t": {"name": "t", "mac_address": "t mac_address"}
}
