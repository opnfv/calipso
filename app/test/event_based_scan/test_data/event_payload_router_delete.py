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

EVENT_PAYLOAD_ROUTER_DELETE = {
    '_context_request_id': 'req-8b2dd9ba-5faa-4471-94c3-fb41781eef8d', '_unique_id': 'c7417f771ee74bb19036b06e685c93dc',
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9', '_context_user': '13baa553aae44adca6615e711fd2f6d9',
    '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_context_auth_token': 'gAAAAABYE7T7789XjB_Nir9PykWTIpDNI0VhgtVQJNyGVImHnug2AVRX9e2JDcXe8F73eNmFepASsoCfqvZet9qN' +
                           '38vrX6GqzL89Quf6pQyLxgRorMv6RlScSCDBQzE8Hj5szSYi_a7F_O2Lr77omUiLi2R_Ludt25mcMiuaMgPknJ2b' +
                           'joAyV_-eE_8CrSbdJ5Dk1MaCSq5K',
    '_context_user_name': 'admin',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_timestamp': '2016-10-28 20:31:27.902723', 'message_id': '569118ad-1f5b-4a50-96ec-f160ebbb1b34',
    'payload': {'router_id': 'bde87a5a-7968-4f3b-952c-e87681a96078'}, '_context_resource_uuid': None,
    'event_type': 'router.delete.end', '_context_project_name': 'calipso-project', 'priority': 'INFO',
    '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_roles': ['_member_', 'admin'],
    '_context_project_domain': None, '_context_user_domain': None, '_context_read_only': False,
    '_context_is_admin': True, '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_domain': None,
    '_context_show_deleted': False, '_context_tenant_name': 'calipso-project', 'publisher_id': 'network.node-6.cisco.com',
    'timestamp': '2016-10-28 20:31:37.012032'}

ROUTER_DOCUMENT = {
    "admin_state_up": True,
    "enable_snat": 1,
    "environment": ENV_CONFIG,
    "gw_port_id": None,
    "host": "node-6.cisco.com",
    "_id": "593fc4c6797ffad322bc5329",
    "id": "node-6.cisco.com-qrouter-bde87a5a-7968-4f3b-952c-e87681a96078",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-regions/RegionOne/RegionOne-availability_zones/internal" +
               "/node-6.cisco.com/node-6.cisco.com-vservices/node-6.cisco.com-vservices-routers/qrouter-bde87a5a" +
               "-7968-4f3b-952c-e87681a96078",
    "last_scanned": 0,
    "local_service_id": "node-6.cisco.com-qrouter-bde87a5a-7968-4f3b-952c-e87681a96078",
    "master_parent_id": "node-6.cisco.com-vservices",
    "master_parent_type": "vservices_folder",
    "name": "1234",
    "name_path": "/" + ENV_CONFIG + "/Regions/RegionOne/Availability Zones/internal/node-6.cisco.com/" +
                 "Vservices/Gateways/router-1234",
    "network": [
        "c64adb76-ad9d-4605-9f5e-bd6dbe325cfb"
    ],
    "object_name": "router-1234",
    "parent_id": "node-6.cisco.com-vservices-routers",
    "parent_text": "Gateways",
    "parent_type": "vservice_routers_folder",
    "service_type": "router",
    "show_in_tree": True,
    "status": "ACTIVE",
    "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
    "type": "vservice"
}
