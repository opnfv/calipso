###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import datetime

from listen.test.event_based_scan.test_data.test_config import ENV_CONFIG

NETWORK_DOC = {'port_security_enabled': True, 'status': 'ACTIVE', 'subnet_ids': [], 'parent_type': 'networks_folder',
               'parent_id': '75c0eb79ff4a42b0ae4973c8375ddf40-networks', 'parent_text': 'Networks', 'subnets': {},
               'admin_state_up': True, 'show_in_tree': True, 'project': 'calipso-project',
               'name_path': '/' + ENV_CONFIG + '/Projects/calipso-project/Networks/testsubnetadd',
               'router:external': False,
               'provider:physical_network': None,
               'id_path': '/' + ENV_CONFIG + '/' + ENV_CONFIG + '-projects/75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a42b0' +
                          'ae4973c8375ddf40-networks/1bb0ba6c-6863-4121-ac89-93f81a9da2b0',
               'object_name': 'testsubnetadd', 'provider:segmentation_id': 46, 'provider:network_type': 'vxlan',
               'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'environment': ENV_CONFIG, 'name': 'testsubnetadd',
               'last_scanned': '2016-10-13 00:20:59.280329', 'id': '1bb0ba6c-6863-4121-ac89-93f81a9da2b0', 'cidrs': [],
               'type': 'network', 'network': '1bb0ba6c-6863-4121-ac89-93f81a9da2b0', 'shared': False, 'mtu': 1400}

EVENT_PAYLOAD_SUBNET_ADD = {
    'payload': {
        'subnet': {'dns_nameservers': [], 'ipv6_address_mode': None, 'ipv6_ra_mode': None, 'gateway_ip': '172.16.10.1',
                   'allocation_pools': [{'start': '172.16.10.2', 'end': '172.16.10.126'}], 'enable_dhcp': True,
                   'id': 'e950055d-231c-4380-983c-a258ea958d58', 'network_id': '1bb0ba6c-6863-4121-ac89-93f81a9da2b0',
                   'tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'ip_version': 4, 'cidr': '172.16.10.0/25',
                   'subnetpool_id': None, 'name': 'testsubnetadd', 'host_routes': []}}, '_context_domain': None,
    'timestamp': '2016-10-13 00:20:59.776358', '_context_project_domain': None, '_context_user_domain': None,
    '_context_project_id': '75c0eb79ff4a42b0ae4973c8375ddf40', 'publisher_id': 'network.node-6.cisco.com',
    '_context_user': '13baa553aae44adca6615e711fd2f6d9', '_context_user_id': '13baa553aae44adca6615e711fd2f6d9',
    'event_type': 'subnet.create.end', 'message_id': '90581321-e9c9-4112-8fe6-38ebf57d5b6b',
    '_context_tenant': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_tenant_name': 'calipso-project',
    '_context_project_name': 'calipso-project', '_context_user_name': 'admin', '_context_resource_uuid': None,
    '_unique_id': 'e8b328229a724938a6bc63f9db737f49', '_context_request_id': 'req-20cfc138-4e1a-472d-b996-7f27ac58446d',
    'priority': 'INFO', '_context_roles': ['_member_', 'admin'],
    '_context_auth_token': 'gAAAAABX_tLMEzC9KhdcD20novcuvgwmpQkwV9hOk86d4AZlsQwXSRbCwBZgUPQZco4VsuCg59_gFeM_scBVmI' +
                           'dDysNUrAhZctDzXneM0cb5nBtjJTfJPpI2_kKgAuGDBARrHZpNs-vPg-SjMtu87w2rgTKfda6idTMKWG3ipe' +
                           '-jXrgNN7p-2kkJzGhZXbMaaeBs3XU-X_ew',
    '_context_read_only': False,
    '_context_user_identity': '13baa553aae44adca6615e711fd2f6d9 75c0eb79ff4a42b0ae4973c8375ddf40 - - -',
    '_context_tenant_id': '75c0eb79ff4a42b0ae4973c8375ddf40', '_context_is_admin': True, '_context_show_deleted': False,
    '_context_timestamp': '2016-10-13 00:20:59.307917'}

EVENT_PAYLOAD_REGION = {
    'RegionOne': {
        'object_name': 'RegionOne', 'id': 'RegionOne', 'name': 'RegionOne',
        'environment': ENV_CONFIG,
                                 'last_scanned': datetime.datetime.utcnow(),
        'name_path': '/' + ENV_CONFIG + '/Regions/RegionOne',
        'parent_id': ENV_CONFIG + '-regions', 'parent_type': 'regions_folder',
        'endpoints': {'nova': {'id': '274cbbd9fd6d4311b78e78dd3a1df51f',
                               'adminURL': 'http://192.168.0.2:8774/v2/8c1751e0ce714736a63fee3c776164da',
                               'service_type': 'compute',
                               'publicURL': 'http://172.16.0.3:8774/v2/8c1751e0ce714736a63fee3c776164da',
                               'internalURL': 'http://192.168.0.2:8774/v2/8c1751e0ce714736a63fee3c776164da'},
                      'heat-cfn': {'id': '0f04ec6ed49f4940822161bf677bdfb2',
                                   'adminURL': 'http://192.168.0.2:8000/v1',
                                   'service_type': 'cloudformation',
                                   'publicURL': 'http://172.16.0.3:8000/v1',
                                   'internalURL': 'http://192.168.0.2:8000/v1'},
                      'nova_ec2': {'id': '390dddc753cc4d378b489129d06c4b7d',
                                   'adminURL': 'http://192.168.0.2:8773/services/Admin',
                                   'service_type': 'ec2',
                                   'publicURL': 'http://172.16.0.3:8773/services/Cloud',
                                   'internalURL': 'http://192.168.0.2:8773/services/Cloud'},
                      'glance': {'id': '475c6c77a94e4e63a5a0f0e767f697a8',
                                 'adminURL': 'http://192.168.0.2:9292',
                                 'service_type': 'image',
                                 'publicURL': 'http://172.16.0.3:9292',
                                 'internalURL': 'http://192.168.0.2:9292'},
                      'swift': {'id': '12e78e06595f48339baebdb5d4309c70',
                                'adminURL': 'http://192.168.0.2:8080/v1/AUTH_8c1751e0ce714736a63fee3c776164da',
                                'service_type': 'object-store',
                                'publicURL': 'http://172.16.0.3:8080/v1/AUTH_8c1751e0ce714736a63fee3c776164da',
                                'internalURL': 'http://192.168.0.2:8080/v1/AUTH_8c1751e0ce714736a63fee3c776164da'},
                      'swift_s3': {'id': '4f655c8f2bef46a0a7ba4a20bba53666',
                                   'adminURL': 'http://192.168.0.2:8080',
                                   'service_type': 's3',
                                   'publicURL': 'http://172.16.0.3:8080',
                                   'internalURL': 'http://192.168.0.2:8080'},
                      'keystone': {'id': '404cceb349614eb39857742970408301',
                                   'adminURL': 'http://192.168.0.2:35357/v2.0',
                                   'service_type': 'identity',
                                   'publicURL': 'http://172.16.0.3:5000/v2.0',
                                   'internalURL': 'http://192.168.0.2:5000/v2.0'},
                      'cinderv2': {'id': '2c30937688e944889db4a64fab6816e6',
                                   'adminURL': 'http://192.168.0.2:8776/v2/8c1751e0ce714736a63fee3c776164da',
                                   'service_type': 'volumev2',
                                   'publicURL': 'http://172.16.0.3:8776/v2/8c1751e0ce714736a63fee3c776164da',
                                   'internalURL': 'http://192.168.0.2:8776/v2/8c1751e0ce714736a63fee3c776164da'},
                      'novav3': {'id': '1df917160dfb4ce5b469764fde22b3ab',
                                 'adminURL': 'http://192.168.0.2:8774/v3',
                                 'service_type': 'computev3',
                                 'publicURL': 'http://172.16.0.3:8774/v3',
                                 'internalURL': 'http://192.168.0.2:8774/v3'},
                      'ceilometer': {'id': '617177a3dcb64560a5a79ab0a91a7225',
                                     'adminURL': 'http://192.168.0.2:8777',
                                     'service_type': 'metering',
                                     'publicURL': 'http://172.16.0.3:8777',
                                     'internalURL': 'http://192.168.0.2:8777'},
                      'neutron': {'id': '8dc28584da224c4b9671171ead3c982a',
                                  'adminURL': 'http://192.168.0.2:9696',
                                  'service_type': 'network',
                                  'publicURL': 'http://172.16.0.3:9696',
                                  'internalURL': 'http://192.168.0.2:9696'},
                      'cinder': {'id': '05643f2cf9094265b432376571851841',
                                 'adminURL': 'http://192.168.0.2:8776/v1/8c1751e0ce714736a63fee3c776164da',
                                 'service_type': 'volume',
                                 'publicURL': 'http://172.16.0.3:8776/v1/8c1751e0ce714736a63fee3c776164da',
                                 'internalURL': 'http://192.168.0.2:8776/v1/8c1751e0ce714736a63fee3c776164da'},
                      'heat': {'id': '9e60268a5aaf422d9e42f0caab0a19b4',
                               'adminURL': 'http://192.168.0.2:8004/v1/8c1751e0ce714736a63fee3c776164da',
                               'service_type': 'orchestration',
                               'publicURL': 'http://172.16.0.3:8004/v1/8c1751e0ce714736a63fee3c776164da',
                               'internalURL': 'http://192.168.0.2:8004/v1/8c1751e0ce714736a63fee3c776164da'}},
        'show_in_tree': True,
        'id_path': '/' + ENV_CONFIG + '/' + ENV_CONFIG + '-regions/RegionOne',
        'type': 'region'}}


HOST_DOC = {
    "environment": ENV_CONFIG,
    "host": "node-6.cisco.com",
    "host_type": [
        "Controller",
        "Network"
    ],
    "id": "node-6.cisco.com",
    "id_path": "/" + ENV_CONFIG + "/" + ENV_CONFIG + "-regions/RegionOne/RegionOne-availability_zones" +
               "/internal/node-6.cisco.com",
    "name": "node-6.cisco.com",
    "name_path": "/" + ENV_CONFIG + "/Regions/RegionOne/Availability Zones/internal/node-6.cisco.com",
    "object_name": "node-6.cisco.com",
    "parent_id": "internal",
    "parent_type": "availability_zone",
    "show_in_tree": True,
    "type": "host",
    "zone": "internal"
}

PORT_DOC = {
    "admin_state_up": True,
    "device_id": "c57216ca-c1c4-430d-a045-32851ca879e3",
    "device_owner": "compute:nova",
    "dns_assignment": [
        {
            "hostname": "host-172-16-10-1",
            "ip_address": "172.16.10.1",
            "fqdn": "host-172-16-10-1.openstacklocal."
        }
    ],
    "dns_name": "",
    "environment": ENV_CONFIG,
    "extra_dhcp_opts": [

    ],
    "fixed_ips": [
        {
            "ip_address": "172.16.10.1",
            "subnet_id": "6f6ef3b5-76c9-4f70-81e5-f3cc196db025"
        }
    ],
    "id": "2233445-55b6-4c05-9480-4bc648845c6f",
    "id_path": ENV_CONFIG + "/" + ENV_CONFIG + "-projects/75c0eb79ff4a42b0ae4973c8375ddf40/75c0eb79ff4a42b0ae4973c837" +
               "5ddf40-networks/1bb0ba6c-6863-4121-ac89-93f81a9da2b0/1bb0ba6c-6863-4121-ac89-93f81a9da2b0-ports" +
               "/2233445-55b6-4c05-9480-4bc648845c6f",
    "last_scanned": 0,
    "mac_address": "fa:16:3e:13:b2:aa",
    "master_parent_id": "1bb0ba6c-6863-4121-ac89-93f81a9da2b0",
    "master_parent_type": "network",
    "name": "fa:16:3e:13:b2:aa",
    "name_path": "/" + ENV_CONFIG + "/Projects/calipso-project/Networks/test_interface/Ports/" +
                 "2233445-55b6-4c05-9480-4bc648845c6f",
    "network_id": "1bb0ba6c-6863-4121-ac89-93f81a9da2b0",
    "object_name": "2233445-55b6-4c05-9480-4bc648845c6f",
    "parent_id": "1bb0ba6c-6863-4121-ac89-93f81a9da2b0-ports",
    "parent_text": "Ports",
    "parent_type": "ports_folder",
    "port_security_enabled": False,
    "project": "calipso-project",
    "security_groups": [

    ],
    "status": "DOWN",
    "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
    "type": "port"
}