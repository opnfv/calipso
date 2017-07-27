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

WRONG_HOST = {
    "show_in_tree" : True,
    "type" : "host",
    "zone" : "nova"
}

VCONNECTORS_FOLDER = {
    "create_object" : True,
    "environment" : "Mirantis-Liberty-Xiaocong",
    "id" : "node-6.cisco.com-vconnectors",
    "id_path" : "/Mirantis-Liberty-Xiaocong/Mirantis-Liberty-Xiaocong-regions/RegionOne/RegionOne-availability_zones/internal/node-6.cisco.com/node-6.cisco.com-vconnectors",
    "name" : "vConnectors",
    "name_path" : "/Mirantis-Liberty-Xiaocong/Regions/RegionOne/Availability Zones/internal/node-6.cisco.com/vConnectors",
    "object_name" : "vConnectors",
    "parent_id" : "node-6.cisco.com",
    "parent_type" : "host",
    "show_in_tree" : True,
    "text" : "vConnectors",
    "type" : "vconnectors_folder"
}

VCONNECTORS = [
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