###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from test.event_based_scan.test_data.test_config import ENV_CONFIG

EVENT_PAYLOAD_PORT_INSTANCE_ADD = {
    '_context_user_id': '73638a2687534f9794cd8057ba860637', 'payload': {
        'port': {'port_security_enabled': True, 'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
                 'binding:vif_type': 'ovs',
                 'mac_address': 'fa:16:3e:04:cd:ab',
                 'fixed_ips': [{'subnet_id': '9a9c1848-ea23-4c5d-8c40-ae1def4c2de3', 'ip_address': '172.16.13.6'}],
                 'security_groups': ['2dd5c169-1ff7-40e5-ad96-18924b6d23f1'], 'allowed_address_pairs': [],
                 'binding:host_id': 'node-223.cisco.com', 'dns_name': '', 'status': 'DOWN',
                 'id': '1233445-75b6-4c05-9480-4bc648845c6f', 'binding:profile': {}, 'admin_state_up': True,
                 'device_owner': 'compute:calipso-zone', 'device_id': '27a87908-bc1b-45cc-9238-09ad1ae686a7',
                 'network_id': '55550a69-24eb-47f5-a458-3aa086cc71c2', 'name': '',
                 'binding:vif_details': {'ovs_hybrid_plug': True, 'port_filter': True}, 'extra_dhcp_opts': [],
                 'binding:vnic_type': 'normal'}}, '_context_project_domain': None, 'event_type': 'port.create.end',
    'message_id': '2e0da8dc-6d2d-4bde-9e52-c43ec4687864', 'publisher_id': 'network.node-6.cisco.com',
    '_context_domain': None, '_context_tenant_name': 'services', '_context_tenant': 'a83c8b0d2df24170a7c54f09f824230e',
    '_context_project_name': 'services', '_context_user': '73638a2687534f9794cd8057ba860637',
    '_context_user_name': 'neutron', 'priority': 'INFO', '_context_timestamp': '2016-10-24 21:29:52.127098',
    '_context_read_only': False, '_context_roles': ['admin'], '_context_is_admin': True, '_context_show_deleted': False,
    '_context_user_domain': None,
    '_context_auth_token': 'gAAAAABYDnRG3mhPMwyF17iUiIT4nYjtcSktNmmCKlMrUtmpHYsJWl44xU-boIaf4ChWcBsTjl6jOk6Msu7l17As' +
                           '1Y9vFc1rlmKMl86Eknqp0P22RV_Xr6SIobsl6Axl2Z_w-AB1cZ4pSsY4uscxeJdVkoxRb0aC9B7gllrvAgrfO9O' +
                           'GDqw2ILA',
    '_context_tenant_id': 'a83c8b0d2df24170a7c54f09f824230e', '_context_resource_uuid': None,
    '_context_request_id': 'req-3d6810d9-bee9-41b5-a224-7e9641689cc8', '_unique_id': 'b4f1ffae88b342c09658d9ed2829670c',
    'timestamp': '2016-10-24 21:29:56.383789', '_context_project_id': 'a83c8b0d2df24170a7c54f09f824230e',
    '_context_user_identity': '73638a2687534f9794cd8057ba860637 a83c8b0d2df24170a7c54f09f824230e - - -'}

NETWORK_DOC = {
    "admin_state_up": True,
    "cidrs": [
        "172.16.12.0/24"
    ],
    "environment": ENV_CONFIG,
    "id": "55550a69-24eb-47f5-a458-3aa086cc71c2",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-projects/75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a42b0ae" +
               "4973c8375ddf40-networks/55550a69-24eb-47f5-a458-3aa086cc71c2",
    "last_scanned": 0,
    "mtu": 0,
    "name": "please_connect",
    "name_path": "/" + ENV_CONFIG + "/Projects/calipso-project/Networks/please_connect",
    "network": "55550a69-24eb-47f5-a458-3aa086cc71c2",
    "object_name": "please_connect",
    "parent_id": "75c0eb79ff4a42b0ae4973c8375ddf40-networks",
    "parent_text": "Networks",
    "parent_type": "networks_folder",
    "port_security_enabled": True,
    "project": "calipso-project",
    "provider:network_type": "vxlan",
    "provider:physical_network": None,
    "provider:segmentation_id": 23,
    "router:external": False,
    "shared": False,
    "show_in_tree": True,
    "status": "ACTIVE",
    "subnet_ids": [
        "6f6ef3b5-76c9-4f70-81e5-f3cc196db025"
    ],
    "subnets": {
        "1234": {
            "cidr": "172.16.12.0/24",
            "network_id": "55550a69-24eb-47f5-a458-3aa086cc71c2",
            "allocation_pools": [
                {
                    "start": "172.16.12.2",
                    "end": "172.16.12.254"
                }
            ],
            "id": "6f6ef3b5-76c9-4f70-81e5-f3cc196db025",
            "enable_dhcp": True,
            "ipv6_address_mode": None,
            "name": "1234",
            "host_routes": [

            ],
            "ipv6_ra_mode": None,
            "gateway_ip": "172.16.12.1",
            "ip_version": 4,
            "subnetpool_id": None,
            "dns_nameservers": [

            ],
            "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40"
        }
    },
    "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
    "type": "network"
}

INSTANCE_DOC = {
    "environment": ENV_CONFIG,
    "id": "b2bda4bf-1259-4d60-99ab-85ab4d5014a8",
    "type": "instance",
    "uuid": "b2bda4bf-1259-4d60-99ab-85ab4d5014a8",
    "network": [
        "a09455d9-399a-4193-9cb4-95e9d8e9a560"
    ],
    "local_name": "instance-00000002",
    'name_path': '/' + ENV_CONFIG + '/Regions/RegionOne/Availability Zones' +
                 '/calipso-zone/node-223.cisco.com/Instances/name-change',
    'id': '27a87908-bc1b-45cc-9238-09ad1ae686a7',
    'id_path': '/' + ENV_CONFIG + '/' + ENV_CONFIG + '-regions/RegionOne/RegionOne-availability_zones/calipso-zone' +
               '/node-223.cisco.com/node-223.cisco.com-instances/27a87908-bc1b-45cc-9238-09ad1ae686a7',
    "name": "name-change",
    "network_info": [
        {
            "qbg_params": None,
            "id": "1233445-75b6-4c05-9480-4bc648845c6f",
            "network": {
                "bridge": "br-int",
                "meta": {
                    "injected": False,
                    "tenant_id": "a3efb05cd0484bf0b600e45dab09276d"
                },
                "id": "a09455d9-399a-4193-9cb4-95e9d8e9a560",
                "subnets": [
                    {
                        "gateway": {
                            "meta": {

                            },
                            "type": "gateway",
                            "version": 4,
                            "address": "172.16.50.254"
                        },
                        "version": 4,
                        "dns": [

                        ],
                        "cidr": "172.16.50.0/24",
                        "routes": [

                        ],
                        "meta": {
                            "dhcp_server": "172.16.50.1"
                        },
                        "ips": [
                            {
                                "floating_ips": [

                                ],
                                "meta": {

                                },
                                "type": "fixed",
                                "version": 4,
                                "address": "172.16.50.3"
                            }
                        ]
                    }
                ],
                "label": "calipso-network"
            },
            "active": True,
            "address": "fa:16:3e:04:cd:ab",
            "vnic_type": "normal",
            "meta": {
            },
            "ovs_interfaceid": "1233445-75b6-4c05-9480-4bc648845c6f",
            "type": "ovs",
            "devname": "tapa9a8fa24-11",
        }
    ],
    "host": "node-223.cisco.com",
    "project_id": "a3efb05cd0484bf0b600e45dab09276d",
    "object_name": "libertyDD",
    "parent_id": "node-223.cisco.com-instances",
    "parent_type": "instances_folder",
    "projects": [
        "project-calipso"
    ],
    "mac_address": "fa:16:3e:04:cd:ab"
}

INSTANCES_ROOT = {
    "create_object": True,
    "environment": ENV_CONFIG,
    "id": "node-223.cisco.com-instances",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-regions/RegionOne/RegionOne-availability_zones" +
               "/calipso-zone/node-223.cisco.com/node-223.cisco.com-instances",
    "name": "Instances",
    "name_path": "/" + ENV_CONFIG + "/Regions/RegionOne/Availability Zones/calipso-zone/node-223.cisco.com/Instances",
    "object_name": "Instances",
    "parent_id": "node-223.cisco.com",
    "parent_type": "host",
    "show_in_tree": True,
    "text": "Instances",
    "type": "instances_folder"
}

INSTANCE_DOCS = [
    {
        "environment": ENV_CONFIG,
        "type": "instance",
        "uuid": "b2bda4bf-1259-4d60-99ab-85ab4d5014a8",
        "network": [
            "a09455d9-399a-4193-9cb4-95e9d8e9a560"
        ],
        "local_name": "instance-00000002",
        'name_path': '/' + ENV_CONFIG + '/Regions/RegionOne/Availability Zones' +
                     '/calipso-zone/node-223.cisco.com/Instances/name-change',
        'id': '27a87908-bc1b-45cc-9238-09ad1ae686a7',
        'id_path': '/' + ENV_CONFIG + '/' + ENV_CONFIG + '-regions/RegionOne/RegionOne-availability_zones/calipso-zone' +
                   '/node-223.cisco.com/node-223.cisco.com-instances/27a87908-bc1b-45cc-9238-09ad1ae686a7',
        "name": "name-change",
        "network_info": [
            {
                "qbg_params": None,
                "id": "2233445-75b6-4c05-9480-4bc648845c6f",
                "network": {
                    "bridge": "br-int",
                    "meta": {
                        "injected": False,
                        "tenant_id": "a3efb05cd0484bf0b600e45dab09276d"
                    },
                    "id": "a09455d9-399a-4193-9cb4-95e9d8e9a560",
                    "subnets": [
                        {
                            "gateway": {
                                "meta": {

                                },
                                "type": "gateway",
                                "version": 4,
                                "address": "172.16.50.254"
                            },
                            "version": 4,
                            "dns": [

                            ],
                            "cidr": "172.16.50.0/24",
                            "routes": [

                            ],
                            "meta": {
                                "dhcp_server": "172.16.50.1"
                            },
                            "ips": [
                                {
                                    "floating_ips": [

                                    ],
                                    "meta": {

                                    },
                                    "type": "fixed",
                                    "version": 4,
                                    "address": "172.16.50.3"
                                }
                            ]
                        }
                    ],
                    "label": "calipso-network"
                },
                "active": True,
                "address": "fa:16:3e:04:cd:ab",
                "vnic_type": "normal",
                "meta": {
                },
                "ovs_interfaceid": "2233445-75b6-4c05-9480-4bc648845c6f",
                "type": "ovs",
                "devname": "tapa9a8fa24-12",
            }
        ],
        "host": "node-223.cisco.com",
        "project_id": "a3efb05cd0484bf0b600e45dab09276d",
        "object_name": "libertyDD",
        "parent_id": "node-223.cisco.com-instances",
        "parent_type": "instances_folder",
        "projects": [
            "project-calipso"
        ],
        "mac_address": "fa:16:3e:04:cd:ab"
    }
]

VNIC_DOCS = [{
    "IP Address": "172.16.10.2",
    "IPv6 Address": "fe80::f816:3eff:fe96:5066/64",
    "cidr": "172.16.10.0/25",
    "data": "Link encap:Ethernet  HWaddr fa:16:3e:96:50:66\ninet addr:172.16.10.2  Bcast:172.16.10.127  " +
            "Mask:255.255.255.128\ninet6 addr: fe80::f816:3eff:fe96:5066/64 Scope:Link\nUP BROADCAST RUNNING " +
            "MULTICAST  MTU:1450  Metric:1\nRX packets:17 errors:0 dropped:2 overruns:0 frame:0\nTX packets:8 " +
            "errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:1593 " +
            "(1.5 KB)  TX bytes:648 (648.0 B)\n",
    "host": "node-251.cisco.com",
    "id": "tapca33c645-5b",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-regions/RegionOne/RegionOne-availability_zones/internal" +
               "/node-251.cisco.com/node-251.cisco.com-vservices/node-251.cisco.com-vservices-dhcps/qdhcp-911fe57e" +
               "-1ddd-4151-9dc7-6b578ab357b1/qdhcp-911fe57e-1ddd-4151-9dc7-6b578ab357b1-vnics/tapca33c645-5b",
    "last_scanned": 0,
    "mac_address": "fa:16:3e:04:cd:ab",
    "name": "tapca33c645-5b",
    "name_path": "/" + ENV_CONFIG + "/Regions/RegionOne/Availability Zones/internal/node-251.cisco.com/" +
                 "Vservices/DHCP servers/dhcp-test_interface/vNICs/tapca33c645-5b",
    "netmask": "255.255.255.128",
    "network": "911fe57e-1ddd-4151-9dc7-6b578ab357b1",
    "object_name": "tapca33c645-5b",
    "parent_id": "qdhcp-911fe57e-1ddd-4151-9dc7-6b578ab357b1-vnics",
    "parent_text": "vNICs",
    "parent_type": "vnics_folder",
    "show_in_tree": True,
    "vnic_type": "instance_vnic"
}]

PORTS_FOLDER = {'parent_id': '55550a69-24eb-47f5-a458-3aa086cc71c2',
                'create_object': True,
                'text': 'Ports',
                'show_in_tree': True,
                'id_path': 'test-env/test-env-projects/a83c8b0d2df24170a7c54f09f824230e/a83c8b0d2df24170a7c54f09f824230e-networks/55550a69-24eb-47f5-a458-3aa086cc71c2/55550a69-24eb-47f5-a458-3aa086cc71c2-ports/',
                'name_path': '/test-env/Projects/a83c8b0d2df24170a7c54f09f824230e/Networks/please_connect/Ports',
                'environment': ENV_CONFIG,
                'id': '55550a69-24eb-47f5-a458-3aa086cc71c2-ports',
                'name': 'Ports', 'parent_type': 'network',
                'type': 'ports_folder', 'object_name': 'Ports'}

PORT_DOC = {'id': '1233445-75b6-4c05-9480-4bc648845c6f'}