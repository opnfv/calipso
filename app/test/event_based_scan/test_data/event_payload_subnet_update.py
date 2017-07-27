###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from test.event_based_scan.config.test_config import ENV_CONFIG

NETWORK_DOC = {
    'port_security_enabled': True, 'status': 'ACTIVE',
    'subnets_id': ['393a1f80-4277-4c9a-b44c-0bc05a5121c6'], 'parent_type': 'networks_folder',
    'parent_id': '75c0eb79ff4a42b0ae4973c8375ddf40-networks', 'parent_text': 'Networks',
    'subnets': {'test': {'name': 'test', 'subnetpool_id': None, 'id': '393a1f80-4277-4c9a-b44c-0bc05a5121c6',
                   'network_id': '0abe6331-0d74-4bbd-ad89-a5719c3793e4', 'gateway_ip': '172.16.12.1',
                   'ipv6_address_mode': None, 'dns_nameservers': [], 'ipv6_ra_mode': None, 'cidr': '172.16.12.0/24',
                   'allocation_pools': [{'start': '172.16.12.2', 'end': '172.16.12.254'}], 'enable_dhcp': True,
                   'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'host_routes': [], 'ip_version': 4},
                },
    'admin_state_up': True, 'show_in_tree': True, 'project': 'calipso-project',
    'name_path': '/'+ENV_CONFIG+'/Projects/calipso-project/Networks/testsubnetadd', 'router:external': False,
    'provider:physical_network': None,
    'id_path': '/'+ENV_CONFIG+'/'+ENV_CONFIG+'-projects/75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a42b0'+
            'ae4973c8375ddf40-networks/0abe6331-0d74-4bbd-ad89-a5719c3793e4',
    'object_name': 'testsubnetadd', 'provider:segmentation_id': 46, 'provider:network_type': 'vxlan',
    'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'environment': ENV_CONFIG, 'name': 'testsubnetadd',
    'last_scanned': '2016-10-13 00:20:59.280329', 'id': '0abe6331-0d74-4bbd-ad89-a5719c3793e4',
    'cidrs': ['172.16.12.0/24'],
    'type': 'network', 'network': '0abe6331-0d74-4bbd-ad89-a5719c3793e4', 'shared': False, 'mtu': 1400}


EVENT_PAYLOAD_SUBNET_UPDATE = {
    'publisher_id': 'network.node-6.cisco.com', '_context_show_deleted': False, '_context_project_domain': None,
    '_context_resource_uuid': None, '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40',
    'message_id': '548650b4-2cba-45b6-9b3b-b87cb5c3246e',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_unique_id': '9ffd93fe355141d9976c6808a9ce9b7d',
    '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_read_only': False,
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9', '_context_timestamp': '2016-10-25 00:00:18.505443',
    'priority': 'INFO', '_context_roles': ['_member_', 'admin'], '_context_project_name': 'calipso-project',
    '_context_user': '13baa553aae44adca6615e711fd2f6d9', '_context_user_name': 'admin',
    'timestamp': '2016-10-25 00:00:19.354342', '_context_request_id': 'req-62945d8f-a233-44c8-aa53-f608ad92fd56',
    '_context_tenant_name': 'calipso-project', '_context_domain': None, 'payload': {
        'subnet': {'name': 'port', 'subnetpool_id': None, 'id': '393a1f80-4277-4c9a-b44c-0bc05a5121c6',
                   'network_id': '0abe6331-0d74-4bbd-ad89-a5719c3793e4', 'gateway_ip': '172.16.12.1',
                   'ipv6_address_mode': None, 'dns_nameservers': [], 'ipv6_ra_mode': None, 'cidr': '172.16.12.0/24',
                   'allocation_pools': [{'start': '172.16.12.2', 'end': '172.16.12.254'}], 'enable_dhcp': True,
                   'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'host_routes': [], 'ip_version': 4}},
    '_context_is_admin': True, '_context_user_domain': None, 'event_type': 'subnet.update.end',
    '_context_auth_token': 'gAAAAABYDp0ZacwkUNIRvtiS-3qjLQFZKbkOtTmvuoKX9yM8yCIvl-eZmMC_SPjwPAMJcd8qckE77lLpQ' +
                           'Sx0lWB67mT5jQA-tmp8bcz26kXXr8KlGCicxxjkYTYkJQhC9w8BbGc36CpbRBzIKlOrPtPXUYZrUmPgInQ' +
                           'qCNA-eDeMyJ-AiA1zmNSZK3R43YIJtnDYieLQvX2P'}

EVENT_PAYLOAD_SUBNET_UPDATE_1 = {
    'publisher_id': 'network.node-6.cisco.com', '_context_show_deleted': False, '_context_project_domain': None,
    '_context_resource_uuid': None, '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40',
    'message_id': 'd0f7545f-a2d6-4b0e-a658-01e4de4ecd19',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_unique_id': '1ca167b1317d4523a31b2ae99b25d67c',
    '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_read_only': False,
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9', '_context_timestamp': '2016-10-25 00:03:21.079403',
    'priority': 'INFO', '_context_roles': ['_member_', 'admin'], '_context_project_name': 'calipso-project',
    '_context_user': '13baa553aae44adca6615e711fd2f6d9', '_context_user_name': 'admin',
    'timestamp': '2016-10-25 00:03:22.689115', '_context_request_id': 'req-7a19e8d7-51f6-470e-9035-5e007c9b1f89',
    '_context_tenant_name': 'calipso-project', '_context_domain': None, 'payload': {
    'subnet': {'name': 'port', 'subnetpool_id': None, 'id': '393a1f80-4277-4c9a-b44c-0bc05a5121c6',
               'network_id': '0abe6331-0d74-4bbd-ad89-a5719c3793e4', 'gateway_ip': None, 'ipv6_address_mode': None,
               'dns_nameservers': [], 'ipv6_ra_mode': None, 'cidr': '172.16.12.0/24',
               'allocation_pools': [{'start': '172.16.12.2', 'end': '172.16.12.254'}], 'enable_dhcp': True,
               'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'host_routes': [], 'ip_version': 4}},
    '_context_is_admin': True, '_context_user_domain': None, 'event_type': 'subnet.update.end',
    '_context_auth_token': 'gAAAAABYDp0ZacwkUNIRvtiS-3qjLQFZKbkOtTmvuoKX9yM8yCIvl-eZmMC_SPjwPAMJcd8qckE77lLpQSx0l'+
                           'WB67mT5jQA-tmp8bcz26kXXr8KlGCicxxjkYTYkJQhC9w8BbGc36CpbRBzIKlOrPtPXUYZrUmPgInQqCNA-eD'+
                           'eMyJ-AiA1zmNSZK3R43YIJtnDYieLQvX2P'}
