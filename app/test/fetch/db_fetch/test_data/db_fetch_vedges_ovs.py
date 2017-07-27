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
