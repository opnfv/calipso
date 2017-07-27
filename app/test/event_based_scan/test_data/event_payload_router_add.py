###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import datetime

from test.event_based_scan.config.test_config import ENV_CONFIG

EVENT_PAYLOAD_ROUTER_ADD = {
    '_context_show_deleted': False, '_context_domain': None,
    '_context_user': '13baa553aae44adca6615e711fd2f6d9',
    'message_id': '05682485-9283-4cef-aae5-0bc1e86ed14d',
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9', '_context_read_only': False,
    '_context_user_domain': None, '_unique_id': '40f10fd246814669b61d906fd71be301',
    '_context_auth_token': 'gAAAAABYE58-bIhpHKOyCNnav0czsBonPJbJJPxtkTFHT_gJ-sVPPO1xCldKOoJoJ58M5egmK0' +
                           'tsCOiH9N6u-2h08rH84nrnE6YUoLJM_SWyJlbYDzH7rJyHYPBVE1aYkzMceiy7Jr33G4k6cGZQ' +
                           '7UzAaZRrGLxMMFddvNZa47dVPZsg1oJpdIVVcoaRHf4hPM8lj1qSn6WG',
    'event_type': 'router.create.end', '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
    'priority': 'INFO', '_context_roles': ['_member_', 'admin'],
    '_context_project_name': 'calipso-project',
    '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_context_request_id': 'req-a543a2e4-3160-4e98-b1b8-21a876fff205',
    '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40',
    'timestamp': '2016-10-28 19:00:36.600958',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_tenant_name': 'calipso-project', 'payload': {
        'router': {'name': 'test-router-add',
                   'external_gateway_info': {
                       'enable_snat': True,
                       'external_fixed_ips': [{
                           'ip_address': '172.16.0.137',
                           'subnet_id': 'a5336853-cbc0-49e8-8401-a093e8bab7bb'}],
                       'network_id': 'c64adb76-ad9d-4605-9f5e-123456781234'},
                   'admin_state_up': True,
                   'distributed': False,
                   'routes': [], 'ha': False,
                   'id': 'c485d5f4-dfec-430f-8ad8-409c7034b46d',
                   'status': 'ACTIVE',
                   'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40'}},
    '_context_timestamp': '2016-10-28 19:00:34.395521', '_context_project_domain': None,
    'publisher_id': 'network.node-250.cisco.com', '_context_is_admin': True,
    '_context_user_name': 'admin', '_context_resource_uuid': None}

ROUTER_DOCUMENT = {'host': 'node-250.cisco.com', 'service_type': 'router', 'name': 'router-test-router-add',
                   'id': 'node-250.cisco.com-qrouter-c485d5f4-dfec-430f-8ad8-409c7034b46d',
                   'local_service_id': 'node-250.cisco.com-qrouter-c485d5f4-dfec-430f-8ad8-409c7034b46d',
                   'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'status': 'ACTIVE',
                   'master_parent_type': 'vservices_folder',
                   'admin_state_up': 1, 'parent_type': 'vservice_routers_folder', 'enable_snat': 1,
                   'parent_text': 'Gateways',
                   'gw_port_id': 'e2f31c24-d0f9-499e-a8b1-883941543aa4',
                   'master_parent_id': 'node-250.cisco.com-vservices',
                   'parent_id': 'node-250.cisco.com-vservices-routers'}

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
    "last_scanned": datetime.datetime.utcnow(),
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

NETWORK_DOC = {
    "admin_state_up": True,
    "cidrs": [
        "172.16.0.0/24"
    ],
    "environment": ENV_CONFIG,
    "id": "c64adb76-ad9d-4605-9f5e-123456781234",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-projects/8c1751e0ce714736a63fee3c776164da/8c1751e0ce71" +
               "4736a63fee3c776164da-networks/c64adb76-ad9d-4605-9f5e-123456781234",
    "last_scanned": datetime.datetime.utcnow(),
    "mtu": 1500,
    "name": "admin_floating_net",
    "name_path": "/" + ENV_CONFIG + "/Projects/admin/Networks/admin_floating_net",
    "network": "c64adb76-ad9d-4605-9f5e-123456781234",
    "object_name": "admin_floating_net",
    "parent_id": "8c1751e0ce714736a63fee3c776164da-networks",
    "parent_text": "Networks",
    "parent_type": "networks_folder",
    "port_security_enabled": True,
    "project": "admin",
    "provider:network_type": "flat",
    "provider:physical_network": "physnet1",
    "provider:segmentation_id": None,
    "router:external": True,
    "shared": False,
    "show_in_tree": True,
    "status": "ACTIVE",
    "subnets": {
        "admin_floating_net__subnet": {
            "allocation_pools": [
                {
                    "end": "172.16.0.254",
                    "start": "172.16.0.130"
                }
            ],
            "id": "a5336853-cbc0-49e8-8401-a093e8bab7bb",
            "network_id": "c64adb76-ad9d-4605-9f5e-123456781234",
            "ipv6_ra_mode": None,
            "ipv6_address_mode": None,
            "ip_version": 4,
            "tenant_id": "8c1751e0ce714736a63fee3c776164da",
            "cidr": "172.16.0.0/24",
            "dns_nameservers": [

            ],
            "name": "admin_floating_net__subnet",
            "subnetpool_id": None,
            "gateway_ip": "172.16.0.1",
            "host_routes": [

            ],
            "enable_dhcp": False,
        }
    },
    "subnets_id": [
        "a5336853-cbc0-49e8-8401-a093e8bab7bb"
    ],
    "tenant_id": "8c1751e0ce714736a63fee3c776164da",
    "type": "network"
}
