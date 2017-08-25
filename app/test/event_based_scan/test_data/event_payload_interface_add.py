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

EVENT_PAYLOAD_INTERFACE_ADD = {
    '_context_timestamp': '2016-10-26 21:52:18.893134', '_context_project_name': 'calipso-project',
    'publisher_id': 'network.node-251.cisco.com', 'timestamp': '2016-10-26 21:52:22.377165',
    '_context_user_name': 'admin',
    '_context_roles': ['_member_', 'admin'], '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_unique_id': '44d8a3be1078455b9f73e76cdda9f67a', 'priority': 'INFO',
    '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9', '_context_user_domain': None,
    '_context_show_deleted': False,
    '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_user': '13baa553aae44adca6615e711fd2f6d9',
    '_context_is_admin': True, 'message_id': 'b81eb79f-f5d2-4bc8-b68e-81650cca1c92', 'payload': {
        'router_interface': {'port_id': '1233445-75b6-4c05-9480-4bc648845c6f',
                             'id': 'c57216ca-c1c4-430d-a045-32851ca879e3',
                             'subnet_ids': ['6f6ef3b5-76c9-4f70-81e5-f3cc196db025'],
                             'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
                             'subnet_id': '6f6ef3b5-76c9-4f70-81e5-f3cc196db025'}}, '_context_domain': None,
    '_context_read_only': False, '_context_resource_uuid': None, 'event_type': 'router.interface.create',
    '_context_request_id': 'req-260fe6fd-0e14-42de-8dbc-acd480015166', '_context_project_domain': None,
    '_context_tenant_name': 'calipso-project',
    '_context_auth_token': 'gAAAAABYERgkK8sR80wFsQywjt8vwG0caJW5oxfsWNURcDaYAxy0O6P0u2QQczoMuHBAZa-Ga8T1b3O-5p7p' +
                           'jw-vAyI1z5whuY7i-hJSl2II6WUX2-9dy7BALQgxhCGpe60atLcyTl-rW6o_TKc3f-ppvqtiul4UTlzH9OtY' +
                           'N7b-CezaywYDCIMuzGbThPARd9ilQR2B6DuE'}

NETWORK_DOC = {
    "admin_state_up": True,
    "cidrs": [
        "172.16.12.0/24"
    ],
    "environment": ENV_CONFIG,
    "id": "55550a69-24eb-47f5-a458-3aa086cc71c2",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-projects/75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a42b0a" +
               "e4973c8375ddf40-networks/55550a69-24eb-47f5-a458-3aa086cc71c2",
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

EVENT_PAYLOAD_REGION = {
    'RegionOne': {
        'object_name': 'RegionOne', 'id': 'RegionOne', 'name': 'RegionOne',
        'environment': ENV_CONFIG,
        'last_scanned': 0,
        'name_path': '/' + ENV_CONFIG + '/Regions/RegionOne',
        'parent_id': ENV_CONFIG + '-regions', 'parent_type': 'regions_folder',
        'endpoints': {'nova': {'id': '274cbbd9fd6d4311b78e78dd3a1df51f',
                               'adminURL': 'http://192.168.0.2:8774/v2/8c1751e0ce714736a63fee3c776164da',
                               'service_type': 'compute',
                               'publicURL': 'http://172.16.0.3:8774/v2/8c1751e0ce714736a63fee3c776164da',
                               'internalURL': 'http://192.168.0.2:8774/v2/8c1751e0ce714736a63fee3c776164da'},
                      'heat-cfn': {'id': '0f04ec6ed49f4940822161bf677bdfb2',
                                   'adminURL': 'http://192.168.0.2:8000/v1',
                                   'service_type': 'cloudformation',
                                   'publicURL': 'http://172.16.0.3:8000/v1',
                                   'internalURL': 'http://192.168.0.2:8000/v1'},
                      'nova_ec2': {'id': '390dddc753cc4d378b489129d06c4b7d',
                                   'adminURL': 'http://192.168.0.2:8773/services/Admin',
                                   'service_type': 'ec2',
                                   'publicURL': 'http://172.16.0.3:8773/services/Cloud',
                                   'internalURL': 'http://192.168.0.2:8773/services/Cloud'},
                      'glance': {'id': '475c6c77a94e4e63a5a0f0e767f697a8',
                                 'adminURL': 'http://192.168.0.2:9292',
                                 'service_type': 'image',
                                 'publicURL': 'http://172.16.0.3:9292',
                                 'internalURL': 'http://192.168.0.2:9292'},
                      'swift': {'id': '12e78e06595f48339baebdb5d4309c70',
                                'adminURL': 'http://192.168.0.2:8080/v1/AUTH_8c1751e0ce714736a63fee3c776164da',
                                'service_type': 'object-store',
                                'publicURL': 'http://172.16.0.3:8080/v1/AUTH_8c1751e0ce714736a63fee3c776164da',
                                'internalURL': 'http://192.168.0.2:8080/v1/AUTH_8c1751e0ce714736a63fee3c776164da'},
                      'swift_s3': {'id': '4f655c8f2bef46a0a7ba4a20bba53666',
                                   'adminURL': 'http://192.168.0.2:8080',
                                   'service_type': 's3',
                                   'publicURL': 'http://172.16.0.3:8080',
                                   'internalURL': 'http://192.168.0.2:8080'},
                      'keystone': {'id': '404cceb349614eb39857742970408301',
                                   'adminURL': 'http://192.168.0.2:35357/v2.0',
                                   'service_type': 'identity',
                                   'publicURL': 'http://172.16.0.3:5000/v2.0',
                                   'internalURL': 'http://192.168.0.2:5000/v2.0'},
                      'cinderv2': {'id': '2c30937688e944889db4a64fab6816e6',
                                   'adminURL': 'http://192.168.0.2:8776/v2/8c1751e0ce714736a63fee3c776164da',
                                   'service_type': 'volumev2',
                                   'publicURL': 'http://172.16.0.3:8776/v2/8c1751e0ce714736a63fee3c776164da',
                                   'internalURL': 'http://192.168.0.2:8776/v2/8c1751e0ce714736a63fee3c776164da'},
                      'novav3': {'id': '1df917160dfb4ce5b469764fde22b3ab',
                                 'adminURL': 'http://192.168.0.2:8774/v3',
                                 'service_type': 'computev3',
                                 'publicURL': 'http://172.16.0.3:8774/v3',
                                 'internalURL': 'http://192.168.0.2:8774/v3'},
                      'ceilometer': {'id': '617177a3dcb64560a5a79ab0a91a7225',
                                     'adminURL': 'http://192.168.0.2:8777',
                                     'service_type': 'metering',
                                     'publicURL': 'http://172.16.0.3:8777',
                                     'internalURL': 'http://192.168.0.2:8777'},
                      'neutron': {'id': '8dc28584da224c4b9671171ead3c982a',
                                  'adminURL': 'http://192.168.0.2:9696',
                                  'service_type': 'network',
                                  'publicURL': 'http://172.16.0.3:9696',
                                  'internalURL': 'http://192.168.0.2:9696'},
                      'cinder': {'id': '05643f2cf9094265b432376571851841',
                                 'adminURL': 'http://192.168.0.2:8776/v1/8c1751e0ce714736a63fee3c776164da',
                                 'service_type': 'volume',
                                 'publicURL': 'http://172.16.0.3:8776/v1/8c1751e0ce714736a63fee3c776164da',
                                 'internalURL': 'http://192.168.0.2:8776/v1/8c1751e0ce714736a63fee3c776164da'},
                      'heat': {'id': '9e60268a5aaf422d9e42f0caab0a19b4',
                               'adminURL': 'http://192.168.0.2:8004/v1/8c1751e0ce714736a63fee3c776164da',
                               'service_type': 'orchestration',
                               'publicURL': 'http://172.16.0.3:8004/v1/8c1751e0ce714736a63fee3c776164da',
                               'internalURL': 'http://192.168.0.2:8004/v1/8c1751e0ce714736a63fee3c776164da'}},
        'show_in_tree': True,
        'id_path': '/' + ENV_CONFIG + '/' + ENV_CONFIG + '-regions/RegionOne',
        'type': 'region'}}

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
    "device_owner": "network:router_interface",
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
    "id": "1233445-75b6-4c05-9480-4bc648845c6f",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-projects/75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a42b0a" +
               "e4973c8375ddf40-networks/55550a69-24eb-47f5-a458-3aa086cc71c2/55550a69-24eb-47f5-a458-3aa086cc71c2" +
               "-ports/1233445-75b6-4c05-9480-4bc648845c6f",
    "last_scanned": 0,
    "mac_address": "fa:16:3e:13:b2:aa",
    "master_parent_id": "55550a69-24eb-47f5-a458-3aa086cc71c2",
    "master_parent_type": "network",
    "name": "fa:16:3e:13:b2:aa",
    "name_path": "/" + ENV_CONFIG + "/Projects/calipso-project/Networks/test_interface/Ports" +
                 "/1233445-75b6-4c05-9480-4bc648845c6f",
    "network_id": "55550a69-24eb-47f5-a458-3aa086cc71c2",
    "object_name": "1233445-75b6-4c05-9480-4bc648845c6f",
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

ROUTER_DOCUMENT = {
    "admin_state_up": True,
    "enable_snat": 1,
    "environment": ENV_CONFIG,
    "gw_port_id": "e2f31c24-d0f9-499e-a8b1-883941543aa4",
    "host": "node-251.cisco.com",
    "id": "node-251.cisco.com-qrouter-c57216ca-c1c4-430d-a045-32851ca879e3",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-regions/RegionOne/RegionOne-availability_zones/internal" +
               "/node-251.cisco.com/node-251.cisco.com-vservices/node-251.cisco.com-vservices-routers/node-251.cisco.com-qrouter-bde87" +
               "a5a-7968-4f3b-952c-e87681a96078",
    "last_scanned": 0,
    "local_service_id": "node-251.cisco.com-qrouter-c57216ca-c1c4-430d-a045-32851ca879e3",
    "master_parent_id": "node-251.cisco.com-vservices",
    "master_parent_type": "vservices_folder",
    "name": "1234",
    "name_path": "/" + ENV_CONFIG + "/Regions/RegionOne/Availability Zones/internal/node-251.cisco.com/" +
                 "Vservices/Gateways/router-1234",
    "network": [
        "55550a69-24eb-47f5-a458-3aa086cc71c2"
    ],
    "object_name": "router-1234",
    "parent_id": "node-251.cisco.com-vservices-routers",
    "parent_text": "Gateways",
    "parent_type": "vservice_routers_folder",
    "service_type": "router",
    "show_in_tree": True,
    "status": "ACTIVE",
    "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
    "type": "vservice"
}

HOST = {
    "config": {
        "use_namespaces": True,
        "handle_internal_only_routers": True,
        "ex_gw_ports": 2,
        "agent_mode": "legacy",
        "log_agent_heartbeats": False,
        "floating_ips": 1,
        "external_network_bridge": "",
        "router_id": "",
        "gateway_external_network_id": "",
        "interface_driver": "neutron.agent.linux.interface.OVSInterfaceDriver",
        "routers": 2,
        "interfaces": 4
    },
    "environment": ENV_CONFIG,
    "host": "node-251.cisco.com",
    "host_type": [
        "Controller",
        "Network"
    ],
    "id": "node-251.cisco.com",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-regions/RegionOne/RegionOne-availability_zones" +
               "/internal/node-251.cisco.com",
    "last_scanned": 0,
    "name": "node-251.cisco.com",
    "name_path": "/" + ENV_CONFIG + "/Regions/RegionOne/Availability Zones/internal/node-251.cisco.com",
    "object_name": "node-251.cisco.com",
    "parent_id": "internal",
    "parent_type": "availability_zone",
    "services": {
        "nova-conductor": {
            "available": True,
            "active": True,
            "updated_at": "2016-11-08T19:12:08.000000"
        },
        "nova-scheduler": {
            "available": True,
            "active": True,
            "updated_at": "2016-11-08T19:12:38.000000"
        },
        "nova-cert": {
            "available": True,
            "active": True,
            "updated_at": "2016-11-08T19:12:29.000000"
        },
        "nova-consoleauth": {
            "available": True,
            "active": True,
            "updated_at": "2016-11-08T19:12:37.000000"
        }
    },
    "show_in_tree": True,
    "type": "host",
    "zone": "internal"
}

VNIC_DOCS = [{
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
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-regions/RegionOne/RegionOne-availability_zones/internal" +
               "/node-251.cisco.com/node-251.cisco.com-vservices/node-251.cisco.com-vservices-dhcps/qdhcp-911fe57e" +
               "-1ddd-4151-9dc7-6b578ab357b1/qdhcp-911fe57e-1ddd-4151-9dc7-6b578ab357b1-vnics/tapca33c645-5b",
    "last_scanned": 0,
    "mac_address": "fa:16:3e:13:b2:aa",
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
    "type": "vnic",
    "vnic_type": "vservice_vnic"
}]
