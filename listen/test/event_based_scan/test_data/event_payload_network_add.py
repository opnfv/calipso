###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
EVENT_PAYLOAD_NETWORK_ADD = {
    '_context_request_id': 'req-d8593c49-8424-459b-9ac1-1fd8667310eb', '_context_project_domain': None,
    '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_project_name': 'calipso-project',
    '_context_show_deleted': False, '_context_timestamp': '2016-09-30 17:45:01.738932', '_context_domain': None,
    '_context_roles': ['_member_', 'admin'], '_context_is_admin': True, 'priority': 'INFO',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    'message_id': '093e1ee0-87a7-4d40-9303-68d5eaf11f71', '_context_read_only': False,
    '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_unique_id': '3dc7690856e14066902d861631236297', '_context_resource_uuid': None,
    '_context_user': '13baa553aae44adca6615e711fd2f6d9', '_context_user_domain': None,
    'event_type': 'network.create.end', '_context_user_name': 'admin',
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9',
    '_context_auth_token': 'gAAAAABX7qQJkXEm4q2dRrVg4gjxYZ4iKWOFdkA4IVWXpDOiDtu_nwtAeSpTP3W0sEJiTjQXgxqCXrhCzi5cZ1edo6'
                           + 'DqEhND8TTtCqknIMwXcGGonUV0TkhKDOEnOgJhQLiV6JG-CtI4x0VnAp6muwankIGNChndH-gP0lw3bdIK29' +
                           'aqDS4obeXGsYA3oLoORLubgPQjUpdO',
    'publisher_id': 'network.node-6.cisco.com', 'timestamp': '2016-09-30 17:45:02.125633',
    '_context_tenant_name': 'calipso-project',
    'payload': {
        'network': {'provider:physical_network': None, 'router:external': False, 'shared': False,
                    'id': 'a8226605-40d0-4111-93bd-11ffa5b2d1d7', 'provider:network_type': 'vxlan',
                    'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'mtu': 1400, 'subnets': [], 'status': 'ACTIVE',
                    'provider:segmentation_id': 8, 'port_security_enabled': True, 'name': 'calipso-network-add',
                    'admin_state_up': True}}}

NETWORK_DOCUMENT = {'provider:physical_network': None,
                    'router:external': False,
                    'shared': False,
                    'id': 'a8226605-40d0-4111-93bd-11ffa5b2d1d7',
                    'provider:network_type': 'vxlan',
                    'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
                    'mtu': 1400, 'subnets': {}, 'status': 'ACTIVE',
                    'provider:segmentation_id': 8,
                    'port_security_enabled': True,
                    'name': 'calipso-network-add',
                    'admin_state_up': True, 'environment': 'test-env',
                    'type': 'network',
                    'id_path': '/test-env/test-env-projects/75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a42b0ae4973c8375ddf40-networks/a8226605-40d0-4111-93bd-11ffa5b2d1d7',
                    'cidrs': [], 'subnet_ids': [],
                    'last_scanned': '2016-09-30 17:45:02.125633',
                    'name_path': '/test-env/Projects/calipso-project/Networks/calipso-network-add',
                    'network': 'a8226605-40d0-4111-93bd-11ffa5b2d1d7',
                    'object_name': 'calipso-network-add',
                    'parent_id': '75c0eb79ff4a42b0ae4973c8375ddf40-networks',
                    'parent_text': 'Networks', 'parent_type': 'networks_folder',
                    'project': 'calipso-project', 'show_in_tree': True}
