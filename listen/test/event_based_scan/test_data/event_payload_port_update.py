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

EVENT_PAYLOAD_PORT_UPDATE = {
    '_context_timestamp': '2016-10-25 21:27:05.591848', '_context_user_name': 'admin',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_tenant_name': 'calipso-project', '_context_resource_uuid': None,
    'priority': 'INFO', '_context_user': '13baa553aae44adca6615e711fd2f6d9',
    '_context_domain': None, '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40', 'event_type': 'port.update.end',
    '_context_project_domain': None, '_context_show_deleted': False,
    '_context_request_id': 'req-5c502a18-cf79-4903-85c0-84eeab525378',
    '_context_roles': ['_member_', 'admin'],
    'message_id': 'ee8e493e-1134-4077-bb0a-db9d28b625dd', 'payload': {'port': {
        'dns_assignment': [
            {'ip_address': '172.16.4.2', 'fqdn': 'host-172-16-4-2.openstacklocal.', 'hostname': 'host-172-16-4-2'}],
        'mac_address': 'fa:16:3e:d7:c5:16', 'security_groups': [], 'admin_state_up': True, 'dns_name': '',
        'allowed_address_pairs': [], 'binding:profile': {},
        'binding:vif_details': {'port_filter': True, 'ovs_hybrid_plug': True}, 'port_security_enabled': False,
        'device_id': 'dhcp7a15cee0-2af1-5441-b1dc-94897ef4dee9-b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe',
        'id': '16620a58-c48c-4195-b9c1-779a8ba2e6f8',
        'fixed_ips': [{'subnet_id': 'f68b9dd3-4cb5-46aa-96b1-f9c8a7abc3aa', 'ip_address': '172.16.4.2'}],
        'name': 'test',
        'binding:vnic_type': 'normal', 'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'extra_dhcp_opts': [],
        'network_id': 'b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe', 'binding:vif_type': 'ovs',
        'binding:host_id': 'node-6.cisco.com', 'status': 'ACTIVE', 'device_owner': 'network:dhcp'}},
    'timestamp': '2016-10-25 21:27:06.281892',
    '_unique_id': '964361cb7a434daf9fa6452507133fe5',
    '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_user_domain': None,
    '_context_auth_token': 'gAAAAABYD8zsy7c8LhL2SoZTzmK-YpUMFBJHare_RA7_4E94zqj328sC0cETsFAoWoBY' +
                           '6X8ZvjBQg--5UCqgj7iUE-zfIQwZLzXbl46MP1Fg5ZKCUtdCCPN5yqXxGA-ebYlBB_G' +
                           'If0LUo1YXCKe3GacmfFNC-k0T_B1p340stgLdpW7r0g1jvTDleqK7NWNrnCniZHrgGiLw',
    '_context_is_admin': True, '_context_read_only': False,
    '_context_project_name': 'calipso-project',
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9',
    'publisher_id': 'network.node-6.cisco.com'}

PORT_DOCUMENT = {
    "admin_state_up": True,
    "allowed_address_pairs": [

    ],
    "binding:host_id": "node-6.cisco.com",
    "binding:profile": {

    },
    "binding:vif_details": {
        "port_filter": True,
        "ovs_hybrid_plug": True
    },
    "binding:vif_type": "ovs",
    "binding:vnic_type": "normal",
    "device_id": "dhcp7a15cee0-2af1-5441-b1dc-94897ef4dee9-b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
    "device_owner": "network:dhcp",
    "dns_assignment": [
        {
            "hostname": "host-172-16-4-2",
            "fqdn": "host-172-16-4-2.openstacklocal.",
            "ip_address": "172.16.4.2"
        }
    ],
    "dns_name": "",
    "environment": ENV_CONFIG,
    "extra_dhcp_opts": [

    ],
    "fixed_ips": [
        {
            "subnet_id": "f68b9dd3-4cb5-46aa-96b1-f9c8a7abc3aa",
            "ip_address": "172.16.4.2"
        }
    ],
    "id": "16620a58-c48c-4195-b9c1-779a8ba2e6f8",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-projects/75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb" +
               "79ff4a42b0ae4973c8375ddf40-networks/b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe/b6fd5175-4b22" +
               "-4256-9b1a-9fc4b9dce1fe-ports/16620a58-c48c-4195-b9c1-779a8ba2e6f8",
    "last_scanned": 0,
    "mac_address": "fa:16:3e:d7:c5:16",
    "name": "123",
    "name_path": "/"+ENV_CONFIG+"/Projects/calipso-project/Networks/calipso-met4/Ports/fa:16:3e:d7:c5:16",
    "network_id": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
    "object_name": "fa:16:3e:d7:c5:16",
    "parent_id": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe-ports",
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
