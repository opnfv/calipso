NETWORK_NODE = {
    "config": {
        "interfaces": 4,
        "log_agent_heartbeats": False,
        "gateway_external_network_id": "",
        "router_id": "",
        "interface_driver": "neutron.agent.linux.interface.OVSInterfaceDriver",
        "ex_gw_ports": 2,
        "routers": 2,
        "handle_internal_only_routers": True,
        "floating_ips": 1,
        "external_network_bridge": "",
        "use_namespaces": True,
        "agent_mode": "legacy"
    },
    "environment": "Mirantis-Liberty-Xiaocong",
    "host": "node-6.cisco.com",
    "host_type": [
        "Controller",
        "Network"
    ],
    "id": "node-6.cisco.com",
    "id_path": "/Mirantis-Liberty-Xiaocong/Mirantis-Liberty-Xiaocong-regions/RegionOne/RegionOne-availability_zones/internal/node-6.cisco.com",
    "name": "node-6.cisco.com",
    "name_path": "/Mirantis-Liberty-Xiaocong/Regions/RegionOne/Availability Zones/internal/node-6.cisco.com",
    "object_name": "node-6.cisco.com",
    "parent_id": "internal",
    "parent_type": "availability_zone",
    "services": {
        "nova-scheduler": {
            "active": True,
            "available": True,
            "updated_at": "2016-10-21T18:01:10.000000"
        },
        "nova-consoleauth": {
            "active": True,
            "available": True,
            "updated_at": "2016-10-21T18:01:54.000000"
        },
        "nova-conductor": {
            "active": True,
            "available": True,
            "updated_at": "2016-10-21T18:01:45.000000"
        },
        "nova-cert": {
            "active": True,
            "available": True,
            "updated_at": "2016-10-21T18:01:56.000000"
        }
    },
    "show_in_tree": True,
    "type": "host",
    "zone": "internal"
}

BRIDGE_RESULT = [
    "bridge name\tbridge id\t\tSTP enabled\tinterfaces",
    "br-ex\t\t8000.005056acc9a2\tno\t\teno33554952",
    "\t\t\t\t\t\t\tp_ff798dba-0",
    "\t\t\t\t\t\t\tv_public",
    "\t\t\t\t\t\t\tv_vrouter_pub",
    "br-fw-admin\t\t8000.005056ace897\tno\t\teno16777728",
    "br-mesh\t\t8000.005056acc9a2\tno\t\teno33554952.103",
    "br-mgmt\t\t8000.005056ace897\tno\t\teno16777728.101",
    "\t\t\t\t\t\t\tmgmt-conntrd",
    "\t\t\t\t\t\t\tv_management",
    "\t\t\t\t\t\t\tv_vrouter",
    "br-storage\t\t8000.005056ace897\tno\t\teno16777728.102"
]

FIXED_LINES = [
    "br-ex\t\t8000.005056acc9a2\tno\t\teno33554952,p_ff798dba-0,v_public,v_vrouter_pub",
    "br-fw-admin\t\t8000.005056ace897\tno\t\teno16777728",
    "br-mesh\t\t8000.005056acc9a2\tno\t\teno33554952.103",
    "br-mgmt\t\t8000.005056ace897\tno\t\teno16777728.101,mgmt-conntrd,v_management,v_vrouter",
    "br-storage\t\t8000.005056ace897\tno\t\teno16777728.102"
]

PARSE_CM_RESULTS = [
    {
        "bridge_id": "8000.005056acc9a2",
        "bridge_name": "br-ex",
        "interfaces": "eno33554952,p_ff798dba-0,v_public,v_vrouter_pub",
        "stp_enabled": "no"
    },
    {
        "bridge_id": "8000.005056ace897",
        "bridge_name": "br-fw-admin",
        "interfaces": "eno16777728",
        "stp_enabled": "no"
    },
    {
        "bridge_id": "8000.005056acc9a2",
        "bridge_name": "br-mesh",
        "interfaces": "eno33554952.103",
        "stp_enabled": "no"
    },
    {
        "bridge_id": "8000.005056ace897",
        "bridge_name": "br-mgmt",
        "interfaces": "eno16777728.101,mgmt-conntrd,v_management,v_vrouter",
        "stp_enabled": "no"
    },
    {
        "bridge_id": "8000.005056ace897",
        "bridge_name": "br-storage",
        "interfaces": "eno16777728.102",
        "stp_enabled": "no"
    }
]

# functional test
INPUT = "node-6.cisco.com"
OUPUT = [
    {
        "connector_type": "bridge",
        "host": "node-6.cisco.com",
        "id": "8000.005056acc9a2",
        "interfaces": {
            "eno33554952": {
                "mac_address": "",
                "name": "eno33554952"
            },
            "p_ff798dba-0": {
                "mac_address": "",
                "name": "p_ff798dba-0"
            },
            "v_public": {
                "mac_address": "",
                "name": "v_public"
            },
            "v_vrouter_pub": {
                "mac_address": "",
                "name": "v_vrouter_pub"
            }
        },
        "interfaces_names": [
            "p_ff798dba-0",
            "v_public",
            "v_vrouter_pub",
            "eno33554952"
        ],
        "name": "br-ex",
        "stp_enabled": "no"
    },
    {
        "connector_type": "bridge",
        "host": "node-6.cisco.com",
        "id": "8000.005056ace897",
        "interfaces": {
            "eno16777728": {
                "mac_address": "",
                "name": "eno16777728"
            }
        },
        "interfaces_names": [
            "eno16777728"
        ],
        "name": "br-fw-admin",
        "stp_enabled": "no"
    },
    {
        "connector_type": "bridge",
        "host": "node-6.cisco.com",
        "id": "8000.005056acc9a2",
        "interfaces": {
            "eno33554952.103": {
                "mac_address": "",
                "name": "eno33554952.103"
            }
        },
        "interfaces_names": [
            "eno33554952.103"
        ],
        "name": "br-mesh",
        "stp_enabled": "no"
    },
    {
        "connector_type": "bridge",
        "host": "node-6.cisco.com",
        "id": "8000.005056ace897",
        "interfaces": {
            "eno16777728.101": {
                "mac_address": "",
                "name": "eno16777728.101"
            },
            "mgmt-conntrd": {
                "mac_address": "",
                "name": "mgmt-conntrd"
            },
            "v_management": {
                "mac_address": "",
                "name": "v_management"
            },
            "v_vrouter": {
                "mac_address": "",
                "name": "v_vrouter"
            }
        },
        "interfaces_names": [
            "v_management",
            "mgmt-conntrd",
            "v_vrouter",
            "eno16777728.101"
        ],
        "name": "br-mgmt",
        "stp_enabled": "no"
    },
    {
        "connector_type": "bridge",
        "host": "node-6.cisco.com",
        "id": "8000.005056ace897",
        "interfaces": {
            "eno16777728.102": {
                "mac_address": "",
                "name": "eno16777728.102"
            }
        },
        "interfaces_names": [
            "eno16777728.102"
        ],
        "name": "br-storage",
        "stp_enabled": "no"
    }
]