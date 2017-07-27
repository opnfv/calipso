NETWORK_HOST = {
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
    "type" : "host",
    "zone" : "internal"
}

COMPUTE_HOST = {
    "environment": "Mirantis-Liberty-Xiaocong",
    "host": "node-5.cisco.com",
    "host_type": [
        "Compute"
    ],
    "id": "node-5.cisco.com",
    "id_path": "/Mirantis-Liberty-Xiaocong/Mirantis-Liberty-Xiaocong-regions/RegionOne/RegionOne-availability_zones/osdna-zone/node-5.cisco.com",
    "ip_address": "192.168.0.4",
    "name": "node-5.cisco.com",
    "name_path": "/Mirantis-Liberty-Xiaocong/Regions/RegionOne/Availability Zones/osdna-zone/node-5.cisco.com",
    "object_name": "node-5.cisco.com",
    "os_id": "1",
    "parent_id": "osdna-zone",
    "parent_type": "availability_zone",
    "services": {
        "nova-compute": {
            "active": True,
            "available": True,
            "updated_at": "2016-10-21T18:01:42.000000"
        }
    },
    "show_in_tree": True,
    "type": "host",
    "zone": "osdna-zone"
}

NAMESPACES = [
    'qdhcp-413de095-01ed-49dc-aa50-4479f43d390e',
    'qdhcp-2e3b85f4-756c-49d9-b34c-f3db13212dbc',
    'qdhcp-b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe',
    'qdhcp-eb276a62-15a9-4616-a192-11466fdd147f',
    'qdhcp-7e59b726-d6f4-451a-a574-c67a920ff627',
    'qdhcp-a55ff1e8-3821-4e5f-bcfd-07df93720a4f',
    'qdhcp-6504fcf7-41d7-40bb-aeb1-6a7658c105fc',
    'qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9',
    'qrouter-49ac7716-06da-49ed-b388-f8ba60e8a0e6',
    'haproxy',
    'vrouter'
]

LOCAL_SERVICES_IDS = [
    {
        "local_service_id": "qdhcp-413de095-01ed-49dc-aa50-4479f43d390e"
    },
    {
        "local_service_id": "qdhcp-2e3b85f4-756c-49d9-b34c-f3db13212dbc"
    },
    {
        "local_service_id": "qdhcp-b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe"
    },
    {
        "local_service_id": "qdhcp-eb276a62-15a9-4616-a192-11466fdd147f"
    },
    {
        "local_service_id": "qdhcp-7e59b726-d6f4-451a-a574-c67a920ff627"
    },
    {
        "local_service_id": "qdhcp-a55ff1e8-3821-4e5f-bcfd-07df93720a4f"
    },
    {
        "local_service_id": "qdhcp-6504fcf7-41d7-40bb-aeb1-6a7658c105fc"
    },
    {
        "local_service_id": "qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9"
    },
    {
        "local_service_id": "qrouter-49ac7716-06da-49ed-b388-f8ba60e8a0e6"
    }
]

VSERVICE = {
        "host": "node-6.cisco.com",
        "id": "qdhcp-b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
        "local_service_id": "qdhcp-b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
        "name": "dhcp-osdna-met4",
        "service_type": "dhcp"
    }

AGENT = {
    "description": "DHCP agent",
    "folder_text": "DHCP servers",
    "type": "dhcp"
}

ROUTER = [
    {"name": "123456"}
]

ID_CLEAN = "413de095-01ed-49dc-aa50-4479f43d390e"
# functional test
INPUT = "node-6.cisco.com"
OUTPUT = [
    {
        "host": "node-6.cisco.com",
        "id": "qdhcp-413de095-01ed-49dc-aa50-4479f43d390e",
        "local_service_id": "qdhcp-413de095-01ed-49dc-aa50-4479f43d390e",
        "master_parent_id": "node-6.cisco.com-vservices",
        "master_parent_type": "vservices_folder",
        "name": "dhcp-aiya",
        "parent_id": "node-6.cisco.com-vservices-dhcps",
        "parent_text": "DHCP servers",
        "parent_type": "vservice_dhcps_folder",
        "service_type": "dhcp"
    },
    {
        "host": "node-6.cisco.com",
        "id": "qdhcp-2e3b85f4-756c-49d9-b34c-f3db13212dbc",
        "local_service_id": "qdhcp-2e3b85f4-756c-49d9-b34c-f3db13212dbc",
        "master_parent_id": "node-6.cisco.com-vservices",
        "master_parent_type": "vservices_folder",
        "name": "dhcp-123456",
        "parent_id": "node-6.cisco.com-vservices-dhcps",
        "parent_text": "DHCP servers",
        "parent_type": "vservice_dhcps_folder",
        "service_type": "dhcp"
    },
    {
        "host": "node-6.cisco.com",
        "id": "qdhcp-b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
        "local_service_id": "qdhcp-b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
        "master_parent_id": "node-6.cisco.com-vservices",
        "master_parent_type": "vservices_folder",
        "name": "dhcp-osdna-met4",
        "parent_id": "node-6.cisco.com-vservices-dhcps",
        "parent_text": "DHCP servers",
        "parent_type": "vservice_dhcps_folder",
        "service_type": "dhcp"
    },
    {
        "host": "node-6.cisco.com",
        "id": "qdhcp-eb276a62-15a9-4616-a192-11466fdd147f",
        "local_service_id": "qdhcp-eb276a62-15a9-4616-a192-11466fdd147f",
        "master_parent_id": "node-6.cisco.com-vservices",
        "master_parent_type": "vservices_folder",
        "name": "dhcp-osdna-net3",
        "parent_id": "node-6.cisco.com-vservices-dhcps",
        "parent_text": "DHCP servers",
        "parent_type": "vservice_dhcps_folder",
        "service_type": "dhcp"
    },
    {
        "host": "node-6.cisco.com",
        "id": "qdhcp-7e59b726-d6f4-451a-a574-c67a920ff627",
        "local_service_id": "qdhcp-7e59b726-d6f4-451a-a574-c67a920ff627",
        "master_parent_id": "node-6.cisco.com-vservices",
        "master_parent_type": "vservices_folder",
        "name": "dhcp-osdna-net1",
        "parent_id": "node-6.cisco.com-vservices-dhcps",
        "parent_text": "DHCP servers",
        "parent_type": "vservice_dhcps_folder",
        "service_type": "dhcp"
    },
    {
        "host": "node-6.cisco.com",
        "id": "qdhcp-a55ff1e8-3821-4e5f-bcfd-07df93720a4f",
        "local_service_id": "qdhcp-a55ff1e8-3821-4e5f-bcfd-07df93720a4f",
        "master_parent_id": "node-6.cisco.com-vservices",
        "master_parent_type": "vservices_folder",
        "name": "dhcp-osdna-net2",
        "parent_id": "node-6.cisco.com-vservices-dhcps",
        "parent_text": "DHCP servers",
        "parent_type": "vservice_dhcps_folder",
        "service_type": "dhcp"
    },
    {
        "host": "node-6.cisco.com",
        "id": "qdhcp-6504fcf7-41d7-40bb-aeb1-6a7658c105fc",
        "local_service_id": "qdhcp-6504fcf7-41d7-40bb-aeb1-6a7658c105fc",
        "master_parent_id": "node-6.cisco.com-vservices",
        "master_parent_type": "vservices_folder",
        "name": "dhcp-admin_internal_net",
        "parent_id": "node-6.cisco.com-vservices-dhcps",
        "parent_text": "DHCP servers",
        "parent_type": "vservice_dhcps_folder",
        "service_type": "dhcp"
    },
    {
        "admin_state_up": 1,
        "enable_snat": 1,
        "gw_port_id": "63489f34-af99-44f4-81de-9a2eb1c1941f",
        "host": "node-6.cisco.com",
        "id": "qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9",
        "local_service_id": "qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9",
        "master_parent_id": "node-6.cisco.com-vservices",
        "master_parent_type": "vservices_folder",
        "name": "router-osdna-router",
        "parent_id": "node-6.cisco.com-vservices-routers",
        "parent_text": "Gateways",
        "parent_type": "vservice_routers_folder",
        "service_type": "router",
        "status": "ACTIVE",
        "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40"
    },
    {
        "admin_state_up": 1,
        "enable_snat": 1,
        "gw_port_id": "57e65d34-3d87-4751-8e95-fc78847a3070",
        "host": "node-6.cisco.com",
        "id": "qrouter-49ac7716-06da-49ed-b388-f8ba60e8a0e6",
        "local_service_id": "qrouter-49ac7716-06da-49ed-b388-f8ba60e8a0e6",
        "master_parent_id": "node-6.cisco.com-vservices",
        "master_parent_type": "vservices_folder",
        "name": "router-router04",
        "parent_id": "node-6.cisco.com-vservices-routers",
        "parent_text": "Gateways",
        "parent_type": "vservice_routers_folder",
        "service_type": "router",
        "status": "ACTIVE",
        "tenant_id": "8c1751e0ce714736a63fee3c776164da"
    }
]