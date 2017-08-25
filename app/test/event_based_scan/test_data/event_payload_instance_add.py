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

EVENT_PAYLOAD_INSTANCE_ADD = {
    'publisher_id': 'compute.node-251.cisco.com', '_context_resource_uuid': None,
    '_context_instance_lock_checked': False,
    '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40',
    '_context_request_id': 'req-432fccc8-4d13-4e62-8639-c99acee82cb3',
    '_context_show_deleted': False,
    '_context_timestamp': '2016-09-08T22:01:41.724236',
    '_unique_id': '537fc5b27c244479a69819a4a435723b',
    '_context_roles': ['_member_', 'admin'], '_context_read_only': False,
    '_context_user_id': '13baa553aae44adca6615e711fd2f6d9',
    '_context_project_name': 'calipso-project',
    '_context_project_domain': None, 'event_type': 'compute.instance.update',
    '_context_service_catalog': [{'endpoints': [
      {'internalURL': 'http://192.168.0.2:8776/v2/75c0eb79ff4a42b0ae4973c8375ddf40',
       'publicURL': 'http://172.16.0.3:8776/v2/75c0eb79ff4a42b0ae4973c8375ddf40',
       'adminURL': 'http://192.168.0.2:8776/v2/75c0eb79ff4a42b0ae4973c8375ddf40',
       'region': 'RegionOne'}],
      'type': 'volumev2',
      'name': 'cinderv2'},
      {'endpoints': [{
          'internalURL': 'http://192.168.0.2:8776/v1/75c0eb79ff4a42b0ae4973c8375ddf40',
          'publicURL': 'http://172.16.0.3:8776/v1/75c0eb79ff4a42b0ae4973c8375ddf40',
          'adminURL': 'http://192.168.0.2:8776/v1/75c0eb79ff4a42b0ae4973c8375ddf40',
          'region': 'RegionOne'}],
          'type': 'volume',
          'name': 'cinder'}],
    'payload': {'instance_type': 'm1.micro', 'progress': '', 'display_name': 'test8',
              'kernel_id': '',
              'new_task_state': None, 'old_display_name': 'name-change',
              'state_description': '',
              'old_state': 'building', 'ramdisk_id': '',
              'created_at': '2016-09-08 16:32:46+00:00',
              'os_type': None,
              'ephemeral_gb': 0, 'launched_at': '2016-09-08T16:25:08.000000',
              'instance_flavor_id': 'f068e24b-5d7e-4819-b5ca-89a33834a918',
              'image_meta': {'min_ram': '64', 'container_format': 'bare', 'min_disk': '0',
                             'disk_format': 'qcow2',
                             'base_image_ref': 'c6f490c4-3656-43c6-8d03-b4e66bd249f9'},
              'audit_period_beginning': '2016-09-01T00:00:00.000000', 'memory_mb': 64,
              'cell_name': '',
              'access_ip_v6': None, 'instance_type_id': 6, 'reservation_id': 'r-bycutzve',
              'access_ip_v4': None,
              'hostname': 'chengli-test-vm1', 'metadata': {},
              'user_id': '13baa553aae44adca6615e711fd2f6d9',
              'availability_zone': 'calipso-zone',
              'instance_id': '27a87908-bc1b-45cc-9238-09ad1ae686a7', 'deleted_at': '',
              'image_ref_url': 'http://172.16.0.4:9292/images/c6f490c4-3656-43c6-8d03-b4e66bd249f9',
              'host': 'node-252.cisco.com', 'vcpus': 1, 'state': 'active',
              'old_task_state': None,
              'architecture': None,
              'terminated_at': '', 'root_gb': 0,
              'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
              'node': 'node-252.cisco.com', 'bandwidth': {}, 'disk_gb': 0,
              'audit_period_ending': '2016-09-08T22:01:43.165282'},
    '_context_quota_class': None,
    '_context_is_admin': True, '_context_read_deleted': 'no',
    'timestamp': '2016-09-08 22:01:43.189907',
    'message_id': '4a9068c6-dcd1-4d6c-81d7-db866e07c1ff', 'priority': 'INFO',
    '_context_domain': None,
    '_context_user': '13baa553aae44adca6615e711fd2f6d9',
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_remote_address': '192.168.0.2', '_context_user_domain': None,
    '_context_auth_token': '''gAAAAABX0d-R0Q4zIrznmZ_L8BT0m4r_lp-7eOr4IenbKz511g2maNo8qhIb86HtA7S
    VGsEJvy4KRcNIGlVRdmGyXBYm3kEuakQXTsXLxvyQeTtgZ9UgnLLXhQvMLbA2gwaimVpyRljq92R7Y7CwnNFLjibhOiYs
    NlvBqitJkaRaQa4sg4xCN2tBj32Re-jRu6dR_sIA-haT''',
    '_context_user_name': 'admin'}

INSTANCES_ROOT = {
    "create_object": True,
    "environment": ENV_CONFIG,
    "id": "node-252.cisco.com-instances",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-regions/RegionOne/RegionOne-availability_zones" +
               "/calipso-zone/node-252.cisco.com/node-252.cisco.com-instances",
    "name": "Instances",
    "name_path": "/" + ENV_CONFIG + "/Regions/RegionOne/Availability Zones/calipso-zone/node-252.cisco.com/Instances",
    "object_name": "Instances",
    "parent_id": "node-252.cisco.com",
    "parent_type": "host",
    "show_in_tree": True,
    "text": "Instances",
    "type": "instances_folder"
}

INSTANCE_DOCUMENT = {
    'projects': ['calipso-project'],
    'network': [],
    'host': 'node-252.cisco.com', 'parent_type': 'instances_folder',
    '_id': '57e421194a0a8a3fbe3bd2d0', 'mac_address': 'fa:16:3e:5e:9e:db', 'type': 'instance',
    'name': 'name-change',
    'uuid': '27a87908-bc1b-45cc-9238-09ad1ae686a7', 'environment': ENV_CONFIG,
    'ip_address': '192.168.0.4', 'local_name': 'instance-00000020', 'object_name': 'test8',
    'parent_id': 'node-223.cisco.com-instances', 'project_id': '75c0eb79ff4a42b0ae4973c8375ddf40',
    'name_path': '/'+ENV_CONFIG+'/Regions/RegionOne/Availability Zones' +
                 '/calipso-zone/node-252.cisco.com/Instances/name-change',
    'id': '27a87908-bc1b-45cc-9238-09ad1ae686a7',
    'id_path': '/'+ENV_CONFIG+'/'+ENV_CONFIG+'-regions/RegionOne/RegionOne-availability_zones/calipso-zone' +
               '/node-223.cisco.com/node-223.cisco.com-instances/27a87908-bc1b-45cc-9238-09ad1ae686a7',
    'show_in_tree': True}

HOST = {
    'name_path': '/'+ ENV_CONFIG +'/Regions/RegionOne/Availability Zones/calipso-zone/node-252.cisco.com',
    'id_path': '/'+ENV_CONFIG+ '/'+ENV_CONFIG+'-regions/RegionOne/' +
               'RegionOne-availability_zones/calipso-zone/node-252.cisco.com',
    'object_name': 'node-252.cisco.com', 'last_scanned': 0,
    'type': 'host', 'environment': ENV_CONFIG, 'host': 'node-252.cisco.com', 'id': 'node-252.cisco.com',
    'ip_address': '192.168.0.4', 'name': 'node-252.cisco.com', 'host_type': ['Compute'],
    'services': {'nova-compute': {'updated_at': '2016-09-26T22:47:09.000000', 'active': True, 'available': True}},
    'show_in_tree': True, 'zone': 'calipso-zone', 'os_id': '1',
    'parent_type': 'availability_zone', 'parent_id': 'calipso-zone'
}
