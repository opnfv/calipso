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

EVENT_PAYLOAD_ROUTER_UPDATE = {
    '_context_request_id': 'req-da45908c-0765-4f8a-9fac-79246901de41', '_unique_id': '80723cc09a4748c6b13214dcb867719e',
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9', '_context_user': '13baa553aae44adca6615e711fd2f6d9',
    '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_context_auth_token': 'gAAAAABYE7T7789XjB_Nir9PykWTIpDNI0VhgtVQJNyGVImHnug2AVRX9e2JDcXe8F73eNmFepASsoCfqvZet9q' +
                           'N38vrX6GqzL89Quf6pQyLxgRorMv6RlScSCDBQzE8Hj5szSYi_a7F_O2Lr77omUiLi2R_Ludt25mcMiuaMgPkn' +
                           'J2bjoAyV_-eE_8CrSbdJ5Dk1MaCSq5K',
    '_context_user_name': 'admin',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_timestamp': '2016-10-28 20:29:35.548123', 'message_id': '42c0ca64-cea1-4c89-a059-72abf7990c40',
    'payload': {
        'router': {'id': 'bde87a5a-7968-4f3b-952c-e87681a96078', 'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
                   'ha': False, 'distributed': False, 'name': 'abc', 'status': 'ACTIVE', 'external_gateway_info': None,
                   'admin_state_up': True, 'routes': []}}, '_context_resource_uuid': None,
    'event_type': 'router.update.end', '_context_project_name': 'calipso-project', 'priority': 'INFO',
    '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_roles': ['_member_', 'admin'],
    '_context_project_domain': None, '_context_user_domain': None, '_context_read_only': False,
    '_context_is_admin': True, '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_domain': None,
    '_context_show_deleted': False, '_context_tenant_name': 'calipso-project', 'publisher_id': 'network.node-250.cisco.com',
    'timestamp': '2016-10-28 20:29:39.986161'}

ROUTER_VSERVICE = {'host': 'node-250.cisco.com', 'service_type': 'router', 'name': '1234',
                   'id': 'node-250.cisco.com-qrouter-bde87a5a-7968-4f3b-952c-e87681a96078',
                   'local_service_id': 'node-250.cisco.com-qrouter-bde87a5a-7968-4f3b-952c-e87681a96078',
                   'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'status': 'ACTIVE',
                   'master_parent_type': 'vservices_folder',
                   'admin_state_up': 1, 'parent_type': 'vservice_routers_folder', 'enable_snat': 1,
                   'parent_text': 'Gateways',
                   'gw_port_id': 'e2f31c24-d0f9-499e-a8b1-883941543aa4',
                   'master_parent_id': 'node-250.cisco.com-vservices',
                   'parent_id': 'node-250.cisco.com-vservices-routers'}

ROUTER_DOCUMENT = {
    "admin_state_up": True,
    "enable_snat": 1,
    "environment": ENV_CONFIG,
    "gw_port_id": "e2f31c24-d0f9-499e-a8b1-883941543aa4",
    "host": "node-250.cisco.com",
    "id": "node-250.cisco.com-qrouter-bde87a5a-7968-4f3b-952c-e87681a96078",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-regions/RegionOne/RegionOne-availability_zones/internal" +
               "/node-250.cisco.com/node-250.cisco.com-vservices/node-250.cisco.com-vservices-routers/qrouter-bde87a5a" +
               "-7968-4f3b-952c-e87681a96078",
    "last_scanned": 0,
    "local_service_id": "node-250.cisco.com-qrouter-bde87a5a-7968-4f3b-952c-e87681a96078",
    "master_parent_id": "node-250.cisco.com-vservices",
    "master_parent_type": "vservices_folder",
    "name": "1234",
    "name_path": "/" + ENV_CONFIG + "/Regions/RegionOne/Availability Zones/internal/node-250.cisco.com/" +
                 "Vservices/Gateways/router-1234",
    "network": [
        "a55ff1e8-3821-4e5f-bcfd-07df93720a4f"
    ],
    "object_name": "router-1234",
    "parent_id": "node-250.cisco.com-vservices-routers",
    "parent_text": "Gateways",
    "parent_type": "vservice_routers_folder",
    "service_type": "router",
    "show_in_tree": True,
    "status": "ACTIVE",
    "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
    "type": "vservice"
}

EVENT_PAYLOAD_ROUTER_SET_GATEWAY = {
    'publisher_id': 'network.node-250.cisco.com',
    '_context_request_id': 'req-79d53b65-47b8-46b2-9a72-3f4031e2d605',
    '_context_project_name': 'calipso-project', '_context_show_deleted': False,
    '_context_user_name': 'admin', '_context_timestamp': '2016-11-02 21:44:31.156447',
    '_context_user': '13baa553aae44adca6615e711fd2f6d9', 'payload': {
        'router': {'id': 'bde87a5a-7968-4f3b-952c-e87681a96078', 'admin_state_up': True, 'routes': [],
                   'status': 'ACTIVE', 'ha': False, 'name': 'test_namespace', 'distributed': False,
                   'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'external_gateway_info': {'external_fixed_ips': [
                {'ip_address': '172.16.0.144', 'subnet_id': 'a5336853-cbc0-49e8-8401-a093e8bab7bb'}],
                'network_id': 'a55ff1e8-3821-4e5f-bcfd-07df93720a4f',
                'enable_snat': True}}},
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9', '_context_read_only': False,
    '_context_auth_token': 'gAAAAABYGlU6mEqntx5E9Nss203DIKH352JKSZP0RsJrAJQ_PfjyZEAzYcFvMh4FYVRDRWLvu0cSDsvUk1ILu' +
                           'nHkpNF28pwcvkBgVModV2Xd2_BW2QbBa2csCOXYiN0LE2uOo3BkrLDEcblvJVT0XTJdDhrBldfyCH0_xSfJ7_' +
                           'wzdy8bB34HwHq2w0S3Okp8Tk_Zx_-xpIqB',
    'priority': 'INFO', 'timestamp': '2016-11-02 21:44:35.627776',
    '_context_roles': ['_member_', 'admin'], '_context_resource_uuid': None,
    '_context_user_domain': None, '_context_project_domain': None,
    '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    'message_id': '71889925-14ce-40c3-a3dc-f26731b10b26',
    'event_type': 'router.update.end',
    '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_unique_id': '9e6ab72c5901451f81748e0aa654ae25',
    '_context_tenant_name': 'calipso-project', '_context_is_admin': True,
    '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_domain': None}

EVENT_PAYLOAD_ROUTER_DEL_GATEWAY = {
    '_context_show_deleted': False, '_context_timestamp': '2016-11-03 18:48:40.420170', '_context_read_only': False,
    'publisher_id': 'network.node-250.cisco.com',
    '_context_auth_token': 'gAAAAABYG4UUGbe9bykUJUPY0lKye578aF0RrMCc7nA21eLbhpwcsh5pWWqz6hnOi7suUCUtr1DPTbqF1M8CVJ' +
                           '9FT2EevbqiahcyphrV2VbmP5_tebOcIHIPJ_f_K3KYJM1C6zgcWgdf9KFu_8t_G99wd1MwWBrZyUUElXgSNv48' +
                           'W4uaCKcbYclnZW78lgXVik5x6WLT_j5V',
    '_context_user_name': 'admin',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9', '_unique_id': '266f2bb0ab2c4a328ae0759d01b0035b',
    'timestamp': '2016-11-03 18:48:41.634214', '_context_roles': ['_member_', 'admin'],
    'event_type': 'router.update.end',
    '_context_user_domain': None, '_context_user': '13baa553aae44adca6615e711fd2f6d9', '_context_is_admin': True,
    '_context_tenant_name': 'calipso-project', '_context_project_domain': None, '_context_domain': None,
    'priority': 'INFO',
    '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'message_id': '5272cd90-7151-4d13-8c1f-e8ff2db773a1',
    '_context_project_name': 'calipso-project', '_context_resource_uuid': None, 'payload': {
        'router': {'id': 'bde87a5a-7968-4f3b-952c-e87681a96078', 'external_gateway_info': None, 'distributed': False,
                   'name': 'TEST_AAA', 'routes': [], 'ha': False, 'admin_state_up': True,
                   'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'status': 'ACTIVE'}},
    '_context_request_id': 'req-d7e73189-4709-4234-8b4c-fb6b4dc2017b'}

PORT = {
    "admin_state_up": True,
    "allowed_address_pairs": [

    ],
    "binding:host_id": "node-250.cisco.com",
    "binding:profile": {

    },
    "binding:vif_details": {
        "port_filter": True,
        "ovs_hybrid_plug": True
    },
    "binding:vif_type": "ovs",
    "binding:vnic_type": "normal",
    "device_id": "9ec3d703-0725-47e3-8f48-02b16236caf9",
    "device_owner": "network:router_interface",
    "dns_assignment": [
        {
            "hostname": "host-172-16-1-1",
            "fqdn": "host-172-16-1-1.openstacklocal.",
            "ip_address": "172.16.1.1"
        }
    ],
    "dns_name": "",
    "environment": ENV_CONFIG,
    "extra_dhcp_opts": [

    ],
    "fixed_ips": [
        {
            "subnet_id": "c1287696-224b-4a72-9f1d-d45176671bce",
            "ip_address": "172.16.1.1"
        }
    ],
    "id": "e2f31c24-d0f9-499e-a8b1-883941543aa4",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-projects/75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a42b" +
               "0ae4973c8375ddf40-networks/a55ff1e8-3821-4e5f-bcfd-07df93720a4f/a55ff1e8-3821-4e5f-bcfd-07df93720a4" +
               "f-ports/e2f31c24-d0f9-499e-a8b1-883941543aa4",
    "last_scanned": 0,
    "mac_address": "fa:16:3e:ee:9a:46",
    "name": "fa:16:3e:ee:9a:46",
    "name_path": "/" + ENV_CONFIG + "/Projects/calipso-project/Networks/calipso-net2/Ports/fa:16:3e:ee:9a:46",
    "network_id": "a55ff1e8-3821-4e5f-bcfd-07df93720a4f",
    "object_name": "fa:16:3e:ee:9a:46",
    "parent_id": "a55ff1e8-3821-4e5f-bcfd-07df93720a4f-ports",
    "parent_text": "Ports",
    "parent_type": "ports_folder",
    "port_security_enabled": False,
    "project": "calipso-project",
    "security_groups": [

    ],
    "show_in_tree": True,
    "status": "ACTIVE",
    "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
    "type": "port"
}

NETWORK_DOC = {
    "admin_state_up": True,
    "cidrs": [
        "172.16.4.0/24"
    ],
    "environment": ENV_CONFIG,
    "id": "a55ff1e8-3821-4e5f-bcfd-07df93720a4f",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-projects/75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a42b" +
               "0ae4973c8375ddf40-networks/a55ff1e8-3821-4e5f-bcfd-07df93720a4f",
    "last_scanned": 0,
    "mtu": 1400,
    "name": "calipso-net2",
    "name_path": "/" + ENV_CONFIG + "/Projects/calipso-project/Networks/calipso-net2",
    "network": "a55ff1e8-3821-4e5f-bcfd-07df93720a4f",
    "object_name": "calipso-net2",
    "parent_id": "75c0eb79ff4a42b0ae4973c8375ddf40-networks",
    "parent_text": "Networks",
    "parent_type": "networks_folder",
    "port_security_enabled": True,
    "project": "calipso-project",
    "provider:network_type": "vxlan",
    "provider:physical_network": None,
    "provider:segmentation_id": 0,
    "router:external": False,
    "shared": False,
    "show_in_tree": True,
    "status": "ACTIVE",
    "subnets": {},
    "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
    "type": "network"
}

HOST_DOC = {
    "config": {
        "gateway_external_network_id": "",
        "router_id": "",
        "handle_internal_only_routers": True,
        "agent_mode": "legacy",
        "ex_gw_ports": 4,
        "floating_ips": 1,
        "external_network_bridge": "",
        "interfaces": 1,
        "log_agent_heartbeats": False,
        "use_namespaces": True,
        "interface_driver": "neutron.agent.linux.interface.OVSInterfaceDriver",
        "routers": 4
    },
    "environment": ENV_CONFIG,
    "host": "node-250.cisco.com",
    "host_type": [
        "Controller",
        "Network"
    ],
    "id": "node-250.cisco.com",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-regions/RegionOne/RegionOne-availability_zones" +
               "/internal/node-250.cisco.com",
    "last_scanned": 0,
    "name": "node-250.cisco.com",
    "name_path": "/" + ENV_CONFIG + "/Regions/RegionOne/Availability Zones/internal/node-250.cisco.com",
    "object_name": "node-250.cisco.com",
    "parent_id": "internal",
    "parent_type": "availability_zone",
    "services": {
        "nova-scheduler": {
            "active": True,
            "available": True,
            "updated_at": "2016-11-02T21:19:47.000000"
        },
        "nova-consoleauth": {
            "active": True,
            "available": True,
            "updated_at": "2016-11-02T21:19:48.000000"
        },
        "nova-cert": {
            "active": True,
            "available": True,
            "updated_at": "2016-11-02T21:19:41.000000"
        },
        "nova-conductor": {
            "active": True,
            "available": True,
            "updated_at": "2016-11-02T21:19:52.000000"
        }
    },
    "show_in_tree": True,
    "type": "host",
    "zone": "internal"
}