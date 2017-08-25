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

EVENT_PAYLOAD_NETWORK_UPDATE = {
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9', '_context_user': '13baa553aae44adca6615e711fd2f6d9',
    'priority': 'INFO',
    '_context_auth_token': 'gAAAAABYBrNJA6Io1infkUKquvCpC1bAWOCRxKE-8YQ71qLJhli200beztKmlY5ToBHSqFyPvoadkVKjA740jF' +
                           'bqeY-YtezMHhJAe-t_VyRJQ46IWAv8nPYvWRd_lmgtHrvBeId8NIPCZkhoAEmj5GwcZUZgnFYEhVlUliNO6IfV' +
                           'Oxcb17Z_1MKfdrfu1AtgD5hWb61w1F6x',
    '_context_user_name': 'admin', '_context_project_name': 'calipso-project', '_context_domain': None,
    '_unique_id': 'd1a96723db9341dca6f0d5fb9620f548', '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
    'message_id': '6b99d060-9cd6-4c14-8a0a-cbfc5c50d122', 'timestamp': '2016-10-18 23:47:31.636433',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_resource_uuid': None, '_context_request_id': 'req-b33cbd49-7af9-4c64-bcfb-782fcd400a5e',
    'publisher_id': 'network.node-6.cisco.com', 'payload': {
        'network': {'provider:network_type': 'vxlan', 'port_security_enabled': True, 'status': 'ACTIVE',
                    'id': '8673c48a-f137-4497-b25d-08b7b218fd17', 'shared': False, 'router:external': False,
                    'subnets': ['fcfa62ec-5ae7-46ce-9259-5f30de7af858'], 'admin_state_up': True,
                    'provider:segmentation_id': 52, 'provider:physical_network': None, 'name': '24',
                    'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'mtu': 1400}}, 'event_type': 'network.update.end',
    '_context_roles': ['_member_', 'admin'], '_context_project_domain': None, '_context_is_admin': True,
    '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_show_deleted': False, '_context_user_domain': None,
    '_context_read_only': False, '_context_timestamp': '2016-10-18 23:47:20.629297',
    '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_tenant_name': 'calipso-project'}


NETWORK_DOCUMENT = {
    "admin_state_up" : True,
    "cidrs" : [
        "172.16.4.0/24"
    ],
    "environment" : ENV_CONFIG,
    "id" : "8673c48a-f137-4497-b25d-08b7b218fd17",
    "id_path" : '/%s/%s-projects/' % (ENV_CONFIG, ENV_CONFIG) +'75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a42b' +
                '0ae4973c8375ddf40-networks/8673c48a-f137-4497-b25d-08b7b218fd17',
    "last_scanned" : 0,
    "mtu" : 1400,
    "name" : "calipso-met4",
    "name_path" : "/"+ENV_CONFIG+"/Projects/calipso-project/Networks/calipso-met4",
    "network" : "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
    "object_name" : "calipso-met4",
    "parent_id" : "75c0eb79ff4a42b0ae4973c8375ddf40-networks",
    "parent_text" : "Networks",
    "parent_type" : "networks_folder",
    "port_security_enabled" : True,
    "project" : "calipso-project",
    "provider:network_type" : "vxlan",
    "provider:physical_network" : None,
    "provider:segmentation_id" : 0,
    "router:external" : False,
    "shared" : False,
    "show_in_tree" : True,
    "status" : "ACTIVE",
    "subnets" : {},
    "tenant_id" : "75c0eb79ff4a42b0ae4973c8375ddf40",
    "type" : "network"
}

UPDATED_NETWORK_FIELDS = {'name': '24',
                          'name_path': '/{}/Projects/calipso-project/Networks/24'.format(ENV_CONFIG),
                          'object_name': '24'}
