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

EVENT_PAYLOAD_SUBNET_DELETE = {
    'payload': {'subnet_id': '88442b4a-e62d-4d72-9d18-b8d6973eb3da'},
    '_context_auth_token': 'gAAAAABYGRxBKUKuNjrN4Z9H5HNhfpfS9h671aqjRNwPT_2snUk5OI52zTpAh-9yjIlcJOZRXHUlWZW7R'+
                           '-vNAjUwdSJ4ILwMW9smDT8hLTsBIki-QtJl1nSSlfhVAqhMsnrQxREJeagESGuvsR3BxHgMVrCt1Vh5wR9'+
                           'E1_pHgn0WFpwVJEN0U8IxNfBvU8uLuIHq1j6XRiiY',
    '_context_user_domain': None, '_context_user_name': 'admin', '_context_read_only': False,
    'publisher_id': 'network.node-6.cisco.com', 'event_type': 'subnet.delete.end',
    'timestamp': '2016-11-01 22:58:04.504790', 'priority': 'INFO',
    '_context_roles': ['_member_', 'admin'],
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_unique_id': 'f79384f4c7764bdc93ee2469d79123d1',
    '_context_tenant_name': 'calipso-project',
    '_context_request_id': 'req-cbb08126-3027-49f0-a896-aedf05cc3389',
    '_context_domain': None, '_context_is_admin': True,
    '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_project_domain': None,
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9',
    '_context_project_name': 'calipso-project',
    '_context_user': '13baa553aae44adca6615e711fd2f6d9', '_context_resource_uuid': None,
    '_context_timestamp': '2016-11-01 22:58:02.675098', '_context_show_deleted': False,
    'message_id': '7bd8402e-8f1f-4f8c-afc2-5042b3388ae7',
    '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40'}


EVENT_PAYLOAD_NETWORK = {
    "admin_state_up": True,
    "cidrs": [
        "172.16.10.0/25"
    ],
    "environment": ENV_CONFIG,
    "id": "121c727b-6376-4a86-a5a8-793dfe7a8ef4",
    "id_path": "/"+ENV_CONFIG+"/"+ENV_CONFIG+"-projects/75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a" +
               "42b0ae4973c8375ddf40-networks/121c727b-6376-4a86-a5a8-793dfe7a8ef4",
    "last_scanned": 0,
    "mtu": 1400,
    "name": "asad",
    "name_path": "/"+ENV_CONFIG+"/Projects/calipso-project/Networks/asad",
    "network": "121c727b-6376-4a86-a5a8-793dfe7a8ef4",
    "object_name": "asad",
    "parent_id": "75c0eb79ff4a42b0ae4973c8375ddf40-networks",
    "parent_text": "Networks",
    "parent_type": "networks_folder",
    "port_security_enabled": True,
    "project": "calipso-project",
    "provider:network_type": "vxlan",
    "provider:physical_network": None,
    "provider:segmentation_id": 18,
    "router:external": False,
    "shared": False,
    "show_in_tree": True,
    "status": "ACTIVE",
    "subnets": {
        "testsubnet": {
            "subnetpool_id": None,
            "enable_dhcp": True,
            "ipv6_ra_mode": None,
            "dns_nameservers": [

            ],
            "name": "testsubnet",
            "ipv6_address_mode": None,
            "ip_version": 4,
            "gateway_ip": "172.16.10.1",
            "network_id": "121c727b-6376-4a86-a5a8-793dfe7a8ef4",
            "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
            "allocation_pools": [
                {
                    "start": "172.16.10.2",
                    "end": "172.16.10.126"
                }
            ],
            "id": "88442b4a-e62d-4d72-9d18-b8d6973eb3da",
            "host_routes": [

            ],
            "cidr": "172.16.10.0/25"
        }
    },
    "subnet_ids": [
        "88442b4a-e62d-4d72-9d18-b8d6973eb3da"
    ],
    "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
    "type": "network"
}
