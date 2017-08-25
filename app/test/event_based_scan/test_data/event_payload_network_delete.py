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


EVENT_PAYLOAD_NETWORK_DELETE = {
    'event_type': 'network.delete.end', 'priority': 'INFO', '_context_tenant_name': 'calipso-project',
    '_context_domain': None, '_context_show_deleted': False, '_unique_id': 'e6f3a44575dd45ea891ec527335a55d7',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_read_only': False, '_context_timestamp': '2016-10-13 23:48:29.632205', '_context_project_domain': None,
    '_context_roles': ['_member_', 'admin'], '_context_user_domain': None,
    '_context_request_id': 'req-21307ef4-f4f7-4e8e-afaf-75dd04d71463',
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9', '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40',
    'payload': {'network_id': '0bb0ba6c-6863-4121-ac89-93f81a9da2b0'}, '_context_user_name': 'admin',
    '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_is_admin': True,
    '_context_resource_uuid': None,
    'timestamp': '2016-10-13 23:48:31.609788', '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
    'message_id': '7b78b897-7a82-4aab-82a5-b1c431535dce', '_context_project_name': 'calipso-project',
    '_context_auth_token': 'gAAAAABYAB0cVTm6fzL1S2q2lskw3z7FiEslh_amLhDmDEwQsm3M7L4omSjZ5qKacvgFTXS0HtpbCQfkZn8' +
                           'BQK80qfbzaQdh05tW1gnboB_FR7vfsUZ1yKUzpDdAgfStDzj_SMWK6FGyZperukjp7Xhmxh91O6cxFvG1' +
                           '0qZmxwtJoKyuW0pCM1593rTsj1Lh6zOIo2iaoC1a',
    '_context_user': '13baa553aae44adca6615e711fd2f6d9', 'publisher_id': 'network.node-6.cisco.com'}


NETWORK_DOCUMENT = {
    "admin_state_up" : True,
    "cidrs" : [
        "172.16.9.0/24"
    ],
    "environment" : ENV_CONFIG,
    "_id": '583c0c69c5f6980fec665422',
    "id" : '0bb0ba6c-6863-4121-ac89-93f81a9da2b0',
    "id_path" : '/%s/%s-projects/' % (ENV_CONFIG, ENV_CONFIG) +'75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a42b' +
                '0ae4973c8375ddf40-networks/0bb0ba6c-6863-4121-ac89-93f81a9da2b0' ,
    "last_scanned" : 0,
    "mtu" : 1400,
    "name" : "testnetwork",
    "name_path" : "/"+ENV_CONFIG+"/Projects/calipso-project/Networks/testnetwork",
    "network" : "0bb0ba6c-6863-4121-ac89-93f81a9da2b0",
    "object_name" : "testnetwork",
    "parent_id" : "75c0eb79ff4a42b0ae4973c8375ddf40-networks",
    "parent_text" : "Networks",
    "parent_type" : "networks_folder",
    "port_security_enabled" : True,
    "project" : "calipso-project",
    "provider:network_type" : "vxlan",
    "provider:physical_network" : None,
    "provider:segmentation_id" : 107,
    "router:external" : False,
    "shared" : False,
    "show_in_tree" : True,
    "status" : "ACTIVE",
    "subnets" : {
        "testabc" : {
            "dns_nameservers" : [

            ],
            "enable_dhcp" : False,
            "host_routes" : [

            ],
            "cidr" : "172.16.9.0/24",
            "ip_version" : 4,
            "id" : "7a1be27e-4aae-43ef-b3c0-7231a41625b8",
            "subnetpool_id" : None,
            "ipv6_ra_mode" : None,
            "ipv6_address_mode" : None,
            "network_id" : "0bb0ba6c-6863-4121-ac89-93f81a9da2b0",
            "tenant_id" : "75c0eb79ff4a42b0ae4973c8375ddf40",
            "name" : "testabc",
            "allocation_pools" : [
                {
                    "end" : "172.16.9.254",
                    "start" : "172.16.9.2"
                }
            ],
            "gateway_ip" : "172.16.9.1"
        }
    },
    "tenant_id" : "75c0eb79ff4a42b0ae4973c8375ddf40",
    "type" : "network"
}