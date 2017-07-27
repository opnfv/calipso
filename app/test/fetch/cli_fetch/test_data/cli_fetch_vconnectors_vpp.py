###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
HOST = {
    "config" : {
        "metadata_proxy_socket" : "/opt/stack/data/neutron/metadata_proxy",
        "nova_metadata_ip" : "192.168.20.14",
        "log_agent_heartbeats" : False
    },
    "environment" : "Devstack-VPP-2",
    "host" : "ubuntu0",
    "host_type" : [
        "Controller",
        "Compute",
        "Network"
    ],
    "id" : "ubuntu0",
    "id_path" : "/Devstack-VPP-2/Devstack-VPP-2-regions/RegionOne/RegionOne-availability_zones/nova/ubuntu0",
    "ip_address" : "192.168.20.14",
    "name" : "ubuntu0",
    "name_path" : "/Devstack-VPP-2/Regions/RegionOne/Availability Zones/nova/ubuntu0",
    "object_name" : "ubuntu0",
    "os_id" : "1",
    "parent_id" : "nova",
    "parent_type" : "availability_zone",
    "services" : {
        "nova-conductor" : {
            "available" : True,
            "active" : True,
            "updated_at" : "2016-08-30T09:18:58.000000"
        },
        "nova-scheduler" : {
            "available" : True,
            "active" : True,
            "updated_at" : "2016-08-30T09:18:54.000000"
        },
        "nova-consoleauth" : {
            "available" : True,
            "active" : True,
            "updated_at" : "2016-08-30T09:18:54.000000"
        }
    },
    "show_in_tree" : True,
    "type" : "host",
    "zone" : "nova"
}

MODE_RESULT = [
    "l3 local0  ",
    "l3 pg/stream-0  ",
    "l3 pg/stream-1  ",
    "l3 pg/stream-2  ",
    "l3 pg/stream-3  ",
    "l2 bridge TenGigabitEthernetc/0/0 bd_id 5678 shg 0",
    "l3 TenGigabitEthernetd/0/0  ",
    "l2 bridge VirtualEthernet0/0/0 bd_id 5678 shg 0",
    "l2 bridge VirtualEthernet0/0/1 bd_id 5678 shg 0",
    "l2 bridge VirtualEthernet0/0/2 bd_id 5678 shg 0",
    "l2 bridge VirtualEthernet0/0/3 bd_id 5678 shg 0",
    "l2 bridge VirtualEthernet0/0/4 bd_id 5678 shg 0",
    "l2 bridge VirtualEthernet0/0/5 bd_id 5678 shg 0",
    "l2 bridge VirtualEthernet0/0/6 bd_id 5678 shg 0",
    "l2 bridge VirtualEthernet0/0/7 bd_id 5678 shg 0",
    "l2 bridge VirtualEthernet0/0/8 bd_id 5678 shg 0"
]

INTERFACE_LINES = [
    "              Name                Idx   Link  Hardware",
    "TenGigabitEthernetc/0/0            5     up   TenGigabitEthernetc/0/0",
    "  Ethernet address 00:25:b5:99:00:5c",
    "  Cisco VIC",
    "    carrier up full duplex speed 40000 mtu 1500  promisc",
    "    rx queues 1, rx desc 5120, tx queues 1, tx desc 2048",
    "    cpu socket 0",
    "",
    "    tx frames ok                                       81404",
    "    tx bytes ok                                      6711404",
    "    rx frames ok                                      502521",
    "    rx bytes ok                                    668002732",
    "    rx missed                                          64495",
    "    extended stats:",
    "      rx good packets                                 502521",
    "      tx good packets                                  81404",
    "      rx good bytes                                668002732",
    "      tx good bytes                                  6711404"
]

INTERFACE_NAME = "TenGigabitEthernetc/0/0"

GET_INTERFACE_DETAIL = {
    "hardware": "TenGigabitEthernetc/0/0",
    "id": "5",
    "mac_address": "00:25:b5:99:00:5c",
    "name": "TenGigabitEthernetc/0/0",
    "state": "up"
}

# functional test
# environment: Devstack-VPP-2
# inventory name: vpp

INPUT = "ubuntu0"
OUPUT = [
    {
        "bd_id": "5678",
        "host": "ubuntu0",
        "id": "ubuntu0-vconnector-5678",
        "interfaces": {
            "name": {
                "hardware": "VirtualEthernet0/0/8",
                "id": "15",
                "mac_address": "fa:16:3e:d1:98:73",
                "name": "VirtualEthernet0/0/8",
                "state": "up"
            }
        },
        "interfaces_names": [
            "TenGigabitEthernetc/0/0",
            "VirtualEthernet0/0/0",
            "VirtualEthernet0/0/1",
            "VirtualEthernet0/0/2",
            "VirtualEthernet0/0/3",
            "VirtualEthernet0/0/4",
            "VirtualEthernet0/0/5",
            "VirtualEthernet0/0/6",
            "VirtualEthernet0/0/7",
            "VirtualEthernet0/0/8"
        ],
        "name": "bridge-domain-5678"
    }
]