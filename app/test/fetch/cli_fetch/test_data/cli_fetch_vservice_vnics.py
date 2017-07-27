###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
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

COMPUTE_NODE = {
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

ERROR_NODE = {
    "environment": "Mirantis-Liberty-Xiaocong",
    "host": "node-5.cisco.com",
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

NAME_SPACES = [
    'qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17',
    'qdhcp-0abe6331-0d74-4bbd-ad89-a5719c3793e4',
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

SERVICE_ID = 'qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17'

SERVICES = [
    {
        "IP Address": "172.16.13.2",
        "IPv6 Address": "fe80::f816:3eff:fea1:eb73/64",
        "cidr": "172.16.13.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:a1:eb:73\ninet addr:172.16.13.2  Bcast:172.16.13.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:fea1:eb73/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:28 errors:0 dropped:35 overruns:0 frame:0\nTX packets:8 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:4485 (4.4 KB)  TX bytes:648 (648.0 B)\n",
        "host": "node-6.cisco.com",
        "id": "tapa68b2627-a1",
        "mac_address": "fa:16:3e:a1:eb:73",
        "master_parent_id": "qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17",
        "master_parent_type": "vservice",
        "name": "tapa68b2627-a1",
        "netmask": "255.255.255.0",
        "network": "8673c48a-f137-4497-b25d-08b7b218fd17",
        "parent_id": "qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    }
]

NET_MASK_ARRAY = ["255", "255", "255", "0"]
SIZE = '24'

VNIC = {
    "IP Address": "172.16.13.2",
    "IPv6 Address": "fe80::f816:3eff:fea1:eb73/64",
    "host": "node-6.cisco.com",
    "id": "tapa68b2627-a1",
    "lines": [
        "Link encap:Ethernet  HWaddr fa:16:3e:a1:eb:73",
        "inet addr:172.16.13.2  Bcast:172.16.13.255  Mask:255.255.255.0",
        "inet6 addr: fe80::f816:3eff:fea1:eb73/64 Scope:Link",
        "UP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1",
        "RX packets:28 errors:0 dropped:35 overruns:0 frame:0",
        "TX packets:8 errors:0 dropped:0 overruns:0 carrier:0",
        "collisions:0 txqueuelen:0",
        "RX bytes:4485 (4.4 KB)  TX bytes:648 (648.0 B)",
        ""
    ],
    "mac_address": "fa:16:3e:a1:eb:73",
    "master_parent_id": "qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17",
    "master_parent_type": "vservice",
    "name": "tapa68b2627-a1",
    "netmask": "255.255.255.0",
    "parent_id": "qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17-vnics",
    "parent_text": "vNICs",
    "parent_type": "vnics_folder",
    "type": "vnic",
    "vnic_type": "vservice_vnic"
}

RAW_VNIC = {
    "host": "node-6.cisco.com",
    "id": "tapa68b2627-a1",
    "lines": [],
    "master_parent_id": "qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17",
    "master_parent_type": "vservice",
    "name": "tapa68b2627-a1",
    "parent_id": "qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17-vnics",
    "parent_text": "vNICs",
    "parent_type": "vnics_folder",
    "type": "vnic",
    "vnic_type": "vservice_vnic"
}

NETWORK = [{
    "admin_state_up": True,
    "cidrs": [
        "172.16.13.0/24"
    ],
    "environment": "Mirantis-Liberty-Xiaocong",
    "id": "8673c48a-f137-4497-b25d-08b7b218fd17",
    "id_path": "/Mirantis-Liberty-Xiaocong/Mirantis-Liberty-Xiaocong-projects/75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a42b0ae4973c8375ddf40-networks/8673c48a-f137-4497-b25d-08b7b218fd17",
    "mtu": 1400,
    "name": "25",
    "name_path": "/Mirantis-Liberty-Xiaocong/Projects/OSDNA-project/Networks/25",
    "network": "8673c48a-f137-4497-b25d-08b7b218fd17",
    "object_name": "25",
    "parent_id": "75c0eb79ff4a42b0ae4973c8375ddf40-networks",
    "parent_text": "Networks",
    "parent_type": "networks_folder",
    "port_security_enabled": True,
    "project": "OSDNA-project",
    "provider:network_type": "vxlan",
    "provider:physical_network": None,
    "provider:segmentation_id": 52,
    "router:external": False,
    "shared": False,
    "show_in_tree": True,
    "status": "ACTIVE",
    "subnets": {
        "123e": {
            "ip_version": 4,
            "enable_dhcp": True,
            "gateway_ip": "172.16.13.1",
            "id": "fcfa62ec-5ae7-46ce-9259-5f30de7af858",
            "ipv6_ra_mode": None,
            "name": "123e",
            "dns_nameservers": [

            ],
            "cidr" : "172.16.13.0/24",
            "subnetpool_id": None,
            "ipv6_address_mode": None,
            "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
            "network_id": "8673c48a-f137-4497-b25d-08b7b218fd17",
            "host_routes": [

            ],
            "allocation_pools": [
                {
                    "start": "172.16.13.2",
                    "end": "172.16.13.254"
                }
            ]
        }
    },
    "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
    "type": "network"
}]

VSERVICE = {
    "children_url": "/osdna_dev/discover.py?type=tree&id=qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17",
    "environment": "Mirantis-Liberty-Xiaocong",
    "host": "node-6.cisco.com",
    "id": "qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17",
    "id_path": "/Mirantis-Liberty-Xiaocong/Mirantis-Liberty-Xiaocong-regions/RegionOne/RegionOne-availability_zones/internal/node-6.cisco.com/node-6.cisco.com-vservices/node-6.cisco.com-vservices-dhcps/qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17",
    "local_service_id": "qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17",
    "name": "dhcp-25",
    "name_path": "/Mirantis-Liberty-Xiaocong/Regions/RegionOne/Availability Zones/internal/node-6.cisco.com/Vservices/DHCP servers/dhcp-25",
    "network": [
        "8673c48a-f137-4497-b25d-08b7b218fd17"
    ],
    "object_name": "dhcp-25",
    "parent_id": "node-6.cisco.com-vservices-dhcps",
    "parent_text": "DHCP servers",
    "parent_type": "vservice_dhcps_folder",
    "service_type": "dhcp",
    "show_in_tree": True,
    "type": "vservice"
}


CIDR = "172.16.13.0/24"

IFCONFIG_RESULT = [
    "lo        Link encap:Local Loopback  ",
    "          inet addr:127.0.0.1  Mask:255.0.0.0",
    "          inet6 addr: ::1/128 Scope:Host",
    "          UP LOOPBACK RUNNING  MTU:65536  Metric:1",
    "          RX packets:0 errors:0 dropped:0 overruns:0 frame:0",
    "          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0",
    "          collisions:0 txqueuelen:0 ",
    "          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)",
    "",
    "tapa68b2627-a1 Link encap:Ethernet  HWaddr fa:16:3e:a1:eb:73  ",
    "          inet addr:172.16.13.2  Bcast:172.16.13.255  Mask:255.255.255.0",
    "          inet6 addr: fe80::f816:3eff:fea1:eb73/64 Scope:Link",
    "          UP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1",
    "          RX packets:28 errors:0 dropped:35 overruns:0 frame:0",
    "          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0",
    "          collisions:0 txqueuelen:0 ",
    "          RX bytes:4485 (4.4 KB)  TX bytes:648 (648.0 B)",
    ""
]

MAC_ADDRESS_LINE = "tapa68b2627-a1 Link encap:Ethernet  HWaddr 00:50:56:ac:e8:97  "
MAC_ADDRESS = "00:50:56:ac:e8:97"
IPV6_ADDRESS_LINE = "          inet6 addr: fe80::f816:3eff:fea1:eb73/64 Scope:Link"
IPV6_ADDRESS = "fe80::f816:3eff:fea1:eb73/64"
IPV4_ADDRESS_LINE = "          inet addr:172.16.13.2  Bcast:172.16.13.255  Mask:255.255.255.0"
IPV4_ADDRESS = "172.16.13.2"

# functional test
INPUT = "node-6.cisco.com"
OUTPUT = [
    {
        "IP Address": "172.16.13.2",
        "IPv6 Address": "fe80::f816:3eff:fea1:eb73/64",
        "cidr": "172.16.13.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:a1:eb:73\ninet addr:172.16.13.2  Bcast:172.16.13.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:fea1:eb73/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:28 errors:0 dropped:35 overruns:0 frame:0\nTX packets:8 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:4485 (4.4 KB)  TX bytes:648 (648.0 B)\n",
        "host": "node-6.cisco.com",
        "id": "tapa68b2627-a1",
        "mac_address": "fa:16:3e:a1:eb:73",
        "master_parent_id": "qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17",
        "master_parent_type": "vservice",
        "name": "tapa68b2627-a1",
        "netmask": "255.255.255.0",
        "network": "8673c48a-f137-4497-b25d-08b7b218fd17",
        "parent_id": "qdhcp-8673c48a-f137-4497-b25d-08b7b218fd17-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "172.16.12.2",
        "IPv6 Address": "fe80::f816:3eff:fec1:7f19/64",
        "cidr": "172.16.12.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:c1:7f:19\ninet addr:172.16.12.2  Bcast:172.16.12.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:fec1:7f19/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:6 errors:0 dropped:8 overruns:0 frame:0\nTX packets:8 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:360 (360.0 B)  TX bytes:648 (648.0 B)\n",
        "host": "node-6.cisco.com",
        "id": "tape67d81de-48",
        "mac_address": "fa:16:3e:c1:7f:19",
        "master_parent_id": "qdhcp-0abe6331-0d74-4bbd-ad89-a5719c3793e4",
        "master_parent_type": "vservice",
        "name": "tape67d81de-48",
        "netmask": "255.255.255.0",
        "network": "0abe6331-0d74-4bbd-ad89-a5719c3793e4",
        "parent_id": "qdhcp-0abe6331-0d74-4bbd-ad89-a5719c3793e4-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "172.16.10.2",
        "IPv6 Address": "fe80::f816:3eff:fe23:1b94/64",
        "cidr": "172.16.10.0/25",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:23:1b:94\ninet addr:172.16.10.2  Bcast:172.16.10.127  Mask:255.255.255.128\ninet6 addr: fe80::f816:3eff:fe23:1b94/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:51 errors:0 dropped:12 overruns:0 frame:0\nTX packets:8 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:9161 (9.1 KB)  TX bytes:648 (648.0 B)\n",
        "host": "node-6.cisco.com",
        "id": "tapa1bf631f-de",
        "mac_address": "fa:16:3e:23:1b:94",
        "master_parent_id": "qdhcp-413de095-01ed-49dc-aa50-4479f43d390e",
        "master_parent_type": "vservice",
        "name": "tapa1bf631f-de",
        "netmask": "255.255.255.128",
        "network": "413de095-01ed-49dc-aa50-4479f43d390e",
        "parent_id": "qdhcp-413de095-01ed-49dc-aa50-4479f43d390e-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "172.16.13.2",
        "IPv6 Address": "fe80::f816:3eff:fec3:c871/64",
        "cidr": "172.16.13.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:c3:c8:71\ninet addr:172.16.13.2  Bcast:172.16.13.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:fec3:c871/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:4614 errors:0 dropped:4 overruns:0 frame:0\nTX packets:4459 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:823296 (823.2 KB)  TX bytes:929712 (929.7 KB)\n",
        "host": "node-6.cisco.com",
        "id": "tapaf69959f-ef",
        "mac_address": "fa:16:3e:c3:c8:71",
        "master_parent_id": "qdhcp-2e3b85f4-756c-49d9-b34c-f3db13212dbc",
        "master_parent_type": "vservice",
        "name": "tapaf69959f-ef",
        "netmask": "255.255.255.0",
        "network": "8673c48a-f137-4497-b25d-08b7b218fd17",
        "parent_id": "qdhcp-2e3b85f4-756c-49d9-b34c-f3db13212dbc-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "172.16.4.2",
        "IPv6 Address": "fe80::f816:3eff:fed7:c516/64",
        "cidr": "172.16.4.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:d7:c5:16\ninet addr:172.16.4.2  Bcast:172.16.4.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:fed7:c516/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:56928 errors:0 dropped:15 overruns:0 frame:0\nTX packets:56675 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:10526014 (10.5 MB)  TX bytes:12041070 (12.0 MB)\n",
        "host": "node-6.cisco.com",
        "id": "tap16620a58-c4",
        "mac_address": "fa:16:3e:d7:c5:16",
        "master_parent_id": "qdhcp-b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
        "master_parent_type": "vservice",
        "name": "tap16620a58-c4",
        "netmask": "255.255.255.0",
        "network": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
        "parent_id": "qdhcp-b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "172.16.2.2",
        "IPv6 Address": "fe80::f816:3eff:feeb:39c2/64",
        "cidr": "172.16.2.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:eb:39:c2\ninet addr:172.16.2.2  Bcast:172.16.2.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:feeb:39c2/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:93317 errors:0 dropped:57 overruns:0 frame:0\nTX packets:93264 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:17406098 (17.4 MB)  TX bytes:19958079 (19.9 MB)\n",
        "host": "node-6.cisco.com",
        "id": "tap82d4992f-4d",
        "mac_address": "fa:16:3e:eb:39:c2",
        "master_parent_id": "qdhcp-eb276a62-15a9-4616-a192-11466fdd147f",
        "master_parent_type": "vservice",
        "name": "tap82d4992f-4d",
        "netmask": "255.255.255.0",
        "network": "eb276a62-15a9-4616-a192-11466fdd147f",
        "parent_id": "qdhcp-eb276a62-15a9-4616-a192-11466fdd147f-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "172.16.3.2",
        "IPv6 Address": "fe80::f816:3eff:fe1c:9936/64",
        "cidr": "172.16.3.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:1c:99:36\ninet addr:172.16.3.2  Bcast:172.16.3.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:fe1c:9936/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:170894 errors:0 dropped:41 overruns:0 frame:0\nTX packets:170588 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:31784458 (31.7 MB)  TX bytes:36444046 (36.4 MB)\n",
        "host": "node-6.cisco.com",
        "id": "tap5f22f397-d8",
        "mac_address": "fa:16:3e:1c:99:36",
        "master_parent_id": "qdhcp-7e59b726-d6f4-451a-a574-c67a920ff627",
        "master_parent_type": "vservice",
        "name": "tap5f22f397-d8",
        "netmask": "255.255.255.0",
        "network": "7e59b726-d6f4-451a-a574-c67a920ff627",
        "parent_id": "qdhcp-7e59b726-d6f4-451a-a574-c67a920ff627-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "172.16.1.2",
        "IPv6 Address": "fe80::f816:3eff:fe59:5fff/64",
        "cidr": "172.16.1.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:59:5f:ff\ninet addr:172.16.1.2  Bcast:172.16.1.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:fe59:5fff/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:93468 errors:0 dropped:38 overruns:0 frame:0\nTX packets:93452 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:17416578 (17.4 MB)  TX bytes:19972565 (19.9 MB)\n",
        "host": "node-6.cisco.com",
        "id": "tapbf16c3ab-56",
        "mac_address": "fa:16:3e:59:5f:ff",
        "master_parent_id": "qdhcp-a55ff1e8-3821-4e5f-bcfd-07df93720a4f",
        "master_parent_type": "vservice",
        "name": "tapbf16c3ab-56",
        "netmask": "255.255.255.0",
        "network": "a55ff1e8-3821-4e5f-bcfd-07df93720a4f",
        "parent_id": "qdhcp-a55ff1e8-3821-4e5f-bcfd-07df93720a4f-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "192.168.111.2",
        "IPv6 Address": "fe80::f816:3eff:fe74:5/64",
        "cidr": "192.168.111.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:74:00:05\ninet addr:192.168.111.2  Bcast:192.168.111.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:fe74:5/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:45 errors:0 dropped:28 overruns:0 frame:0\nTX packets:8 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:3734 (3.7 KB)  TX bytes:648 (648.0 B)\n",
        "host": "node-6.cisco.com",
        "id": "tapee8e5dbb-03",
        "mac_address": "fa:16:3e:74:00:05",
        "master_parent_id": "qdhcp-6504fcf7-41d7-40bb-aeb1-6a7658c105fc",
        "master_parent_type": "vservice",
        "name": "tapee8e5dbb-03",
        "netmask": "255.255.255.0",
        "network": "6504fcf7-41d7-40bb-aeb1-6a7658c105fc",
        "parent_id": "qdhcp-6504fcf7-41d7-40bb-aeb1-6a7658c105fc-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "172.16.0.131",
        "IPv6 Address": "2001:420:4482:24c1:f816:3eff:fe23:3ad7/64",
        "cidr": "172.16.0.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:23:3a:d7\ninet addr:172.16.0.131  Bcast:172.16.0.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:fe23:3ad7/64 Scope:Link\ninet6 addr: 2001:420:4482:24c1:f816:3eff:fe23:3ad7/64 Scope:Global\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:48172796 errors:0 dropped:1144801 overruns:0 frame:0\nTX packets:63 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:4220491940 (4.2 GB)  TX bytes:3162 (3.1 KB)\n",
        "host": "node-6.cisco.com",
        "id": "qg-63489f34-af",
        "mac_address": "fa:16:3e:23:3a:d7",
        "master_parent_id": "qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9",
        "master_parent_type": "vservice",
        "name": "qg-63489f34-af",
        "netmask": "255.255.255.0",
        "network": "c64adb76-ad9d-4605-9f5e-bd6dbe325cfb",
        "parent_id": "qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "172.16.13.5",
        "IPv6 Address": "fe80::f816:3eff:fe1f:e174/64",
        "cidr": "172.16.13.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:1f:e1:74\ninet addr:172.16.13.5  Bcast:172.16.13.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:fe1f:e174/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:25 errors:0 dropped:1 overruns:0 frame:0\nTX packets:10 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:2460 (2.4 KB)  TX bytes:864 (864.0 B)\n",
        "host": "node-6.cisco.com",
        "id": "qr-18f029db-77",
        "mac_address": "fa:16:3e:1f:e1:74",
        "master_parent_id": "qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9",
        "master_parent_type": "vservice",
        "name": "qr-18f029db-77",
        "netmask": "255.255.255.0",
        "network": "8673c48a-f137-4497-b25d-08b7b218fd17",
        "parent_id": "qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "172.16.2.1",
        "IPv6 Address": "fe80::f816:3eff:fe2c:fb9b/64",
        "cidr": "172.16.2.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:2c:fb:9b\ninet addr:172.16.2.1  Bcast:172.16.2.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:fe2c:fb9b/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:49 errors:0 dropped:3 overruns:0 frame:0\nTX packets:10 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:5825 (5.8 KB)  TX bytes:864 (864.0 B)\n",
        "host": "node-6.cisco.com",
        "id": "qr-3ff411a2-54",
        "mac_address": "fa:16:3e:2c:fb:9b",
        "master_parent_id": "qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9",
        "master_parent_type": "vservice",
        "name": "qr-3ff411a2-54",
        "netmask": "255.255.255.0",
        "network": "eb276a62-15a9-4616-a192-11466fdd147f",
        "parent_id": "qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "172.16.1.1",
        "IPv6 Address": "fe80::f816:3eff:feee:9a46/64",
        "cidr": "172.16.1.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:ee:9a:46\ninet addr:172.16.1.1  Bcast:172.16.1.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:feee:9a46/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:85 errors:0 dropped:14 overruns:0 frame:0\nTX packets:10 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:7402 (7.4 KB)  TX bytes:864 (864.0 B)\n",
        "host": "node-6.cisco.com",
        "id": "qr-8733cc5d-b3",
        "mac_address": "fa:16:3e:ee:9a:46",
        "master_parent_id": "qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9",
        "master_parent_type": "vservice",
        "name": "qr-8733cc5d-b3",
        "netmask": "255.255.255.0",
        "network": "a55ff1e8-3821-4e5f-bcfd-07df93720a4f",
        "parent_id": "qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "172.16.3.1",
        "IPv6 Address": "fe80::f816:3eff:feba:5a3c/64",
        "cidr": "172.16.3.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:ba:5a:3c\ninet addr:172.16.3.1  Bcast:172.16.3.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:feba:5a3c/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:3018 errors:0 dropped:15 overruns:0 frame:0\nTX packets:1766 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:295458 (295.4 KB)  TX bytes:182470 (182.4 KB)\n",
        "host": "node-6.cisco.com",
        "id": "qr-bb9b8340-72",
        "mac_address": "fa:16:3e:ba:5a:3c",
        "master_parent_id": "qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9",
        "master_parent_type": "vservice",
        "name": "qr-bb9b8340-72",
        "netmask": "255.255.255.0",
        "network": "7e59b726-d6f4-451a-a574-c67a920ff627",
        "parent_id": "qrouter-9ec3d703-0725-47e3-8f48-02b16236caf9-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "172.16.0.130",
        "IPv6 Address": "fe80::f816:3eff:fecb:8d7b/64",
        "cidr": "172.16.0.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:cb:8d:7b\ninet addr:172.16.0.130  Bcast:172.16.0.255  Mask:255.255.255.0\ninet6 addr: 2001:420:4482:24c1:f816:3eff:fecb:8d7b/64 Scope:Global\ninet6 addr: fe80::f816:3eff:fecb:8d7b/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:48172955 errors:0 dropped:1144729 overruns:0 frame:0\nTX packets:59 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:4220505032 (4.2 GB)  TX bytes:2958 (2.9 KB)\n",
        "host": "node-6.cisco.com",
        "id": "qg-57e65d34-3d",
        "mac_address": "fa:16:3e:cb:8d:7b",
        "master_parent_id": "qrouter-49ac7716-06da-49ed-b388-f8ba60e8a0e6",
        "master_parent_type": "vservice",
        "name": "qg-57e65d34-3d",
        "netmask": "255.255.255.0",
        "network": "c64adb76-ad9d-4605-9f5e-bd6dbe325cfb",
        "parent_id": "qrouter-49ac7716-06da-49ed-b388-f8ba60e8a0e6-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    },
    {
        "IP Address": "192.168.111.1",
        "IPv6 Address": "fe80::f816:3eff:fe0a:3cc/64",
        "cidr": "192.168.111.0/24",
        "data": "Link encap:Ethernet  HWaddr fa:16:3e:0a:03:cc\ninet addr:192.168.111.1  Bcast:192.168.111.255  Mask:255.255.255.0\ninet6 addr: fe80::f816:3eff:fe0a:3cc/64 Scope:Link\nUP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1\nRX packets:79 errors:0 dropped:0 overruns:0 frame:0\nTX packets:10 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:6475 (6.4 KB)  TX bytes:864 (864.0 B)\n",
        "host": "node-6.cisco.com",
        "id": "qr-f7b44150-99",
        "mac_address": "fa:16:3e:0a:03:cc",
        "master_parent_id": "qrouter-49ac7716-06da-49ed-b388-f8ba60e8a0e6",
        "master_parent_type": "vservice",
        "name": "qr-f7b44150-99",
        "netmask": "255.255.255.0",
        "network": "6504fcf7-41d7-40bb-aeb1-6a7658c105fc",
        "parent_id": "qrouter-49ac7716-06da-49ed-b388-f8ba60e8a0e6-vnics",
        "parent_text": "vNICs",
        "parent_type": "vnics_folder",
        "type": "vnic",
        "vnic_type": "vservice_vnic"
    }
]