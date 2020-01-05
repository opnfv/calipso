###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from listen.test.event_based_scan.test_data.test_config import ENV_CONFIG

EVENT_PAYLOAD_PORT_DELETE = {
    '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_tenant_name': 'calipso-project',
    '_context_project_name': 'calipso-project', '_context_user_id': '13baa553aae44adca6615e711fd2f6d9',
    '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_context_auth_token': 'gAAAAABYIR4eeMzyZ6IWHjWSK9kmr-p4hxRhm5LtDp--kiu5v5MzpnShwkZAbFTkIBR0fC2iaBurXlAvI0pE' +
                           'myBRpAuxWFsM5rbsiFlo_qpuo_dqIGe6_R7J-MDIGnLCl4T3z3Rb4asZKksXRhP5brkJF1-LdqAXJJ55sgQ' +
                           'aH-22H9g9Wxhziz5YaoshWskJYhb_geTeqPsa',
    '_context_show_deleted': False, '_context_read_only': False, '_context_is_admin': True,
    '_context_timestamp': '2016-11-08 00:58:07.248644',
    'payload': {'port_id': '2233445-55b6-4c05-9480-4bc648845c6f'},
    'timestamp': '2016-11-08 00:58:07.294731', '_context_user': '13baa553aae44adca6615e711fd2f6d9',
    'event_type': 'port.delete.start', '_unique_id': '83a98a31743c4c11aa1d1787037f6683',
    '_context_request_id': 'req-51f0aeba-2648-436f-9505-0c5efb259146', 'publisher_id': 'network.node-6.cisco.com',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_domain': None, '_context_user_domain': None, 'priority': 'INFO', '_context_user_name': 'admin',
    '_context_roles': ['_member_', 'admin'], 'message_id': 'ce1e3e9c-e2ef-47e2-99e1-0b6c69e5eeca',
    '_context_resource_uuid': None, '_context_project_domain': None,
    '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40'}

PORT_DOC = {
    "admin_state_up": True,
    "allowed_address_pairs": [

    ],
    "binding:host_id": "",
    "binding:profile": {

    },
    "binding:vif_details": {

    },
    "binding:vif_type": "unbound",
    "binding:vnic_type": "normal",
    "device_id": "c57216ca-c1c4-430d-a045-32851ca879e3",
    "device_owner": "compute:nova",
    "dns_assignment": [
        {
            "hostname": "host-172-16-10-1",
            "ip_address": "172.16.10.1",
            "fqdn": "host-172-16-10-1.openstacklocal."
        }
    ],
    "dns_name": "",
    "environment": ENV_CONFIG,
    "extra_dhcp_opts": [

    ],
    "fixed_ips": [
        {
            "ip_address": "172.16.10.1",
            "subnet_id": "6f6ef3b5-76c9-4f70-81e5-f3cc196db025"
        }
    ],
    "id": "2233445-55b6-4c05-9480-4bc648845c6f",
    "id_path": ENV_CONFIG + "/" + ENV_CONFIG + "-projects/75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a42b0ae4973c837" +
               "5ddf40-networks/55550a69-24eb-47f5-a458-3aa086cc71c2/55550a69-24eb-47f5-a458-3aa086cc71c2-ports" +
               "/2233445-55b6-4c05-9480-4bc648845c6f",
    "last_scanned": 0,
    "mac_address": "fa:16:3e:13:b2:aa",
    "master_parent_id": "55550a69-24eb-47f5-a458-3aa086cc71c2",
    "master_parent_type": "network",
    "name": "fa:16:3e:13:b2:aa",
    "name_path": "/" + ENV_CONFIG + "/Projects/calipso-project/Networks/test_interface/Ports/" +
                 "2233445-55b6-4c05-9480-4bc648845c6f",
    "network_id": "55550a69-24eb-47f5-a458-3aa086cc71c2",
    "object_name": "2233445-55b6-4c05-9480-4bc648845c6f",
    "parent_id": "55550a69-24eb-47f5-a458-3aa086cc71c2-ports",
    "parent_text": "Ports",
    "parent_type": "ports_folder",
    "port_security_enabled": False,
    "project": "calipso-project",
    "security_groups": [

    ],
    "status": "DOWN",
    "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
    "type": "port"
}

VNIC_DOC = {
    "IP Address": "172.16.10.2",
    "IPv6 Address": "fe80::f816:3eff:fe96:5066/64",
    "cidr": "172.16.10.0/25",
    "data": "Link encap:Ethernet  HWaddr fa:16:3e:96:50:66\ninet addr:172.16.10.2  Bcast:172.16.10.127  " +
            "Mask:255.255.255.128\ninet6 addr: fe80::f816:3eff:fe96:5066/64 Scope:Link\nUP BROADCAST RUNNING " +
            "MULTICAST  MTU:1450  Metric:1\nRX packets:17 errors:0 dropped:2 overruns:0 frame:0\nTX packets:8 " +
            "errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:0\nRX bytes:1593 " +
            "(1.5 KB)  TX bytes:648 (648.0 B)\n",
    "environment": ENV_CONFIG,
    "host": "node-251.cisco.com",
    "id": "tapca33c645-5b",
    '_id': '5970b9aa797ffad322bc9b84',
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-regions/RegionOne/RegionOne-availability_zones/internal" +
               "/node-251.cisco.com/node-251.cisco.com-vservices/node-251.cisco.com-vservices-dhcps/qdhcp-911fe57e-" +
               "1ddd-4151-9dc7-6b578ab357b1/qdhcp-911fe57e-1ddd-4151-9dc7-6b578ab357b1-vnics/tapca33c645-5b",
    "last_scanned": 0,
    "mac_address": "fa:16:3e:13:b2:aa",
    "name": "tapca33c645-5b",
    "name_path": "/"+ENV_CONFIG+"/Regions/RegionOne/Availability Zones/internal/node-251.cisco.com/" +
                 "Vservices/DHCP servers/dhcp-test_interface/vNICs/tapca33c645-5b",
    "netmask": "255.255.255.128",
    "network": "911fe57e-1ddd-4151-9dc7-6b578ab357b1",
    "object_name": "tapca33c645-5b",
    "parent_id": "qdhcp-911fe57e-1ddd-4151-9dc7-6b578ab357b1-vnics",
    "parent_text": "vNICs",
    "parent_type": "vnics_folder",
    "show_in_tree": True,
    "type": "vnic",
    "vnic_type": "vservice_vnic"
}

INSTANCE_DOC = {
    "environment": ENV_CONFIG,
    "type": "instance",
    "uuid": "b2bda4bf-1259-4d60-99ab-85ab4d5014a8",
    "network": [
        "55550a69-24eb-47f5-a458-3aa086cc71c2"
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
            "id": "2233445-55b6-4c05-9480-4bc648845c6f",
            "network": {
                "bridge": "br-int",
                "meta": {
                    "injected": False,
                    "tenant_id": "a3efb05cd0484bf0b600e45dab09276d"
                },
                "id": "55550a69-24eb-47f5-a458-3aa086cc71c2",
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
            "address": "fa:16:3e:04:ab:cd",
            "vnic_type": "normal",
            "meta": {
            },
            "ovs_interfaceid": "2233445-55b6-4c05-9480-4bc648845c6f",
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
    "mac_address": "fa:16:3e:13:b2:aa"
}

INSTANCE_DOCS = [
    {
        "environment": ENV_CONFIG,
        "type": "instance",
        "uuid": "b2bda4bf-1259-4d60-99ab-85ab4d5014a8",
        "network": [
            "55550a69-24eb-47f5-a458-3aa086cc71c2"
        ],
        "local_name": "instance-00000002",
        'name_path': '/' + ENV_CONFIG + '/Regions/RegionOne/Availability Zones' +
                     '/calipso-zone/node-223.cisco.com/Instances/name-change',
        'id': 'c57216ca-c1c4-430d-a045-32851ca879e3',
        'id_path': '/' + ENV_CONFIG + '/' + ENV_CONFIG + '-regions/RegionOne/RegionOne-availability_zones/calipso-zone' +
                   '/node-223.cisco.com/node-223.cisco.com-instances/c57216ca-c1c4-430d-a045-32851ca879e3',
        "name": "name-change",
        "network_info": [
            {
                "qbg_params": None,
                "id": "2233445-55b6-4c05-9480-4bc648845c6f",
                "network": {
                    "bridge": "br-int",
                    "meta": {
                        "injected": False,
                        "tenant_id": "a3efb05cd0484bf0b600e45dab09276d"
                    },
                    "id": "55550a69-24eb-47f5-a458-3aa086cc71c2",
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
                "address": "fa:16:3e:04:ab:cd",
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
    }
]