###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import queue

from scan.fetchers.folder_fetcher import FolderFetcher

SCANNER_TYPE_FOR_ENV = "ScanEnvironment"

METADATA = {
    "scanners_package": "discover",
    "scanners": {}
}
LINK_FINDERS_METADATA = {
    "finders_package": "discover.link_finders",
    "base_finder": "FindLinks",
    "link_finders": [
        "FindLinksForInstanceVnics",
        "FindLinksForOteps",
        "FindLinksForVconnectors",
        "FindLinksForVedges",
        "FindLinksForVserviceVnics",
        "FindLinksForPnics",
        "FindImplicitLinks"
    ]
}

TYPE_TO_FETCH = {
    "type": "host_pnic",
    "fetcher": "CliFetchHostPnicsVpp",
    "environment_condition": {"mechanism_drivers": "OVS"},
    "children_scanner": "ScanOteps"
}

TYPE_TO_FETCH_WITH_WRONG_ENVIRONMENT_CONDITION = {
    "type": "host_pnic",
    "fetcher": "CliFetchHostPnicsVpp",
    "environment_condition": {"mechanism_drivers": "VPP"},
    "children_scanner": "ScanOteps"
}

TYPE_TO_FETCH_WITH_ERROR_VALUE = {
    "environment_condition": {
        "distribution": "Mirantis-7.0"
    }
}

TYPE_TO_FETCH_WITHOUT_ENV_CON = {
    "type": "host_pnic",
    "fetcher": "CliFetchHostPnicsVpp",
    "children_scanner": "ScanOteps"
}

TYPES_TO_FETCH = [
    {
        "type": "ports_folder",
        "fetcher": FolderFetcher("ports", "network")
    },
    {
        "type": "network_services_folder",
        "fetcher": FolderFetcher("network_services", "network",
                                 "Network vServices")
    }
]

ID_FIELD = "id"

PROJECT1 = {
    "object": {
        "description": "",
        "enabled": True,
        "id": "75c0eb79ff4a42b0ae4973c8375ddf40",
        "name": "OSDNA-project"
    },
    "child_id_field": ID_FIELD,
    "scanner": "ScanProject"
}

PROJECT2 = {
    "object": {
        "description": "admin tenant",
        "enabled": True,
        "id": "8c1751e0ce714736a63fee3c776164da",
        "name": "admin"
    },
    "child_id_field": ID_FIELD,
    "scanner": "ScanProject"
}

SCAN_QUEUE = queue.Queue()
SCAN_QUEUE.put(PROJECT1)
SCAN_QUEUE.put(PROJECT2)
QUEUE_SIZE = 2

LIMIT_TO_CHILD_TYPE = "ports_folder"

CONFIGURATIONS = {
    "configuration": [
        {
            "mock": "True",
            "host": "10.56.20.239",
            "name": "mysql",
            "pwd": "102QreDdiD5sKcvNf9qbHrmr",
            "port": 3307.0,
            "user": "root",
            "schema": "nova"
        },
        {
            "name": "OpenStack",
            "host": "10.56.20.239",
            "admin_token": "38MUh19YWcgQQUlk2VEFQ7Ec",
            "port": "5000",
            "user": "admin",
            "pwd": "admin"
        },
        {
            "host": "10.56.20.239",
            "key": "/Users/ngrandhi/.ssh/id_rsa",
            "name": "CLI",
            "pwd": "",
            "user": "root"
        },
        {
            "name": "AMQP",
            "host": "10.56.20.239",
            "port": "5673",
            "user": "nova",
            "pwd": "NF2nSv3SisooxPkCTr8fbfOa"
        }
    ],
    "distribution": "Mirantis",
    "distribution_version": "8.0",
    "last_scanned:": "5/8/16",
    "name": "Mirantis-Liberty-Nvn",
    "mechanism_drivers": [
        "OVS"
    ],
    "operational": "yes",
    "type": "environment"
}

TYPES_TO_FETCHES_FOR_PNIC = {
    "type": "host_pnic",
    "fetcher": "CliFetchHostPnicsVpp",
    "environment_condition": {"mechanism_drivers": "VPP"},
    "children_scanner": "ScanOteps"
}

TYPES_TO_FETCHES_FOR_PNIC_WITHOUT_ENV_CON = {
    "type": "host_pnic",
    "fetcher": "CliFetchHostPnicsVpp",
    "children_scanner": "ScanOteps"
}

TYPES_TO_FETCHES_FOR_SCAN_AGGREGATE = [{
    "type": "host_ref",
    "fetcher": "DbFetchAggregateHosts"
}]

# id = 'RegionOne-aggregates'
# obj = self.inv.get_by_id(self.env, id)
obj = {'id': 'Mirantis-Liberty-Nvn'}
id_field = 'id'
child_id = '',
child_type = ''

child_data = [
    {
        'id_path': '/Mirantis-Liberty-Nvn/Mirantis-Liberty-Nvn-regions',
        'object_name': 'Regions',
        'parent_id': 'Mirantis-Liberty-Nvn',
        'environment': 'Mirantis-Liberty-Nvn',
        'id': 'Mirantis-Liberty-Nvn-regions',
        'show_in_tree': True,
        'text': 'Regions',
        'type': 'regions_folder',
        'name': 'Regions',
        'create_object': True,
        'name_path': '/Mirantis-Liberty-Nvn/Regions',
        'parent_type': 'environment'
    }
]

PARENT = {
    "environment": "Mirantis-Liberty-Xiaocong",
    "id": "node-6.cisco.com-vservices-dhcps",
    "id_path": "/Mirantis-Liberty-Xiaocong/Mirantis-Liberty-Xiaocong-regions"
               "/RegionOne/RegionOne-availability_zones"
               "/internal/node-6.cisco.com"
               "/node-6.cisco.com-vservices/node-6.cisco.com-vservices-dhcps",
    "name": "node-6.cisco.com-vservices-dhcps",
    "name_path": "/Mirantis-Liberty-Xiaocong/Regions"
               "/RegionOne/Availability Zones"
               "/internal/node-6.cisco.com"
               "/vServices/DHCP servers",
    "object_name": "DHCP servers",
    "parent_id": "node-6.cisco.com-vservices",
    "parent_type": "vservices_folder",
    "show_in_tree": True,
    "text": "DHCP servers",
    "type": "vservice_dhcps_folder"
}

PARENT_WITHOUT_ID = {
    'id': ''
}

TYPE_TO_FETCH_FOR_ENVIRONMENT = {
    "type": "regions_folder",
    "fetcher": FolderFetcher("regions", "environment"),
    "children_scanner": "ScanRegionsRoot"
}

TYPE_TO_FETCH_FOR_ENV_WITHOUT_CHILDREN_FETCHER = {
    "type": "regions_folder",
    "fetcher": FolderFetcher("regions", "environment")
}

DB_RESULTS_WITH_CREATE_OBJECT = [
    {
        "name": "Mirantis-Liberty-Xiaocong-regions",
        "parent_type": "environment",
        "parent_id": "Mirantis-Liberty-Xiaocong",
        "text": "Regions",
        "create_object": True,
        "type": "regions_folder",
        "id": "Mirantis-Liberty-Xiaocong-regions"
    }
]

DB_RESULTS_WITHOUT_CREATE_OBJECT = [
    {
        "name": "Mirantis-Liberty-Xiaocong-regions",
        "parent_type": "environment",
        "parent_id": "Mirantis-Liberty-Xiaocong",
        "text": "Regions",
        "create_object": False,
        "type": "regions_folder",
        "id": "Mirantis-Liberty-Xiaocong-regions"
    }
]

DB_RESULTS_WITH_PROJECT = [
    {
        "name": "Mirantis-Liberty-Xiaocong-regions",
        "parent_type": "environment",
        "parent_id": "Mirantis-Liberty-Xiaocong",
        "text": "Regions", "create_object": True,
        "type": "regions_folder",
        "id": "Mirantis-Liberty-Xiaocong-regions",
        "in_project-OSDNA-project": "1",
    }
]

PROJECT_KEY = "in_project-OSDNA-project"

DB_RESULTS_WITH_MASTER_PARENT_IN_DB = [
    {
        "host": "node-6.cisco.com",
        "id": "qdhcp-413de095-01ed-49dc-aa50-4479f43d390e",
        "local_service_id": "qdhcp-413de095-01ed-49dc-aa50-4479f43d390e",
        "master_parent_id": "node-6.cisco.com-vservices",
        "master_parent_type": "vservices_folder",
        "name": "dhcp-aiya",
        "parent_id": "node-6.cisco.com-vservices-dhcps",
        "parent_text": "DHCP servers",
        "parent_type": "vservice_dhcps_folder",
        "service_type": "dhcp"
    }
]

DB_RESULTS_WITHOUT_MASTER_PARENT_IN_DB = [
    {
        "host": "node-6.cisco.com",
        "id": "qdhcp-413de095-01ed-49dc-aa50-4479f43d390e",
        "local_service_id": "qdhcp-413de095-01ed-49dc-aa50-4479f43d390e",
        "master_parent_id": "node-6.cisco.com-vservices",
        "master_parent_type": "vservices_folder",
        "name": "dhcp-aiya",
        "parent_id": "node-6.cisco.com-vservices-dhcps",
        "parent_text": "DHCP servers",
        "parent_type": "vservice_dhcps_folder",
        "service_type": "dhcp"
    }
]

DICTIONARY_DB_RESULTS = {
    "name": "Mirantis-Liberty-Xiaocong-regions",
    "parent_type": "environment",
    "parent_id": "Mirantis-Liberty-Xiaocong",
    "text": "Regions", "create_object": True,
    "type": "regions_folder",
    "id": "Mirantis-Liberty-Xiaocong-regions"
}

MASTER_PARENT = {
    "create_object": True,
    "environment": "Mirantis-Liberty-Xiaocong",
    "id": "node-6.cisco.com-vservices",
    "id_path": "/Mirantis-Liberty/Mirantis-Liberty-regions"
               "/RegionOne/RegionOne-availability_zones"
               "/internal/node-6.cisco.com/node-6.cisco.com-vservices",
    "name": "Vservices",
    "name_path": "/Mirantis-Liberty/Regions"
                 "/RegionOne/Availability Zones"
                 "/internal/node-6.cisco.com/Vservices",
    "object_name": "Vservices",
    "parent_id": "node-6.cisco.com",
    "parent_type": "host",
    "show_in_tree": True,
    "text": "Vservices",
    "type": "vservices_folder"
}

CONFIGURATIONS_WITHOUT_MECHANISM_DRIVERS = {
    "configuration": [
        {
            "mock": "True",
            "host": "10.56.20.239",
            "name": "mysql",
            "pwd": "102QreDdiD5sKcvNf9qbHrmr",
            "port": 3307.0,
            "user": "root",
            "schema": "nova"
        },
        {
            "name": "OpenStack",
            "host": "10.56.20.239",
            "admin_token": "38MUh19YWcgQQUlk2VEFQ7Ec",
            "port": "5000",
            "user": "admin",
            "pwd": "admin"
        },
        {
            "host": "10.56.20.239",
            "key": "/Users/ngrandhi/.ssh/id_rsa",
            "name": "CLI",
            "pwd": "",
            "user": "root"
        },
        {
            "name": "AMQP",
            "host": "10.56.20.239",
            "port": "5673",
            "user": "nova",
            "pwd": "NF2nSv3SisooxPkCTr8fbfOa"
        }
    ],
    "distribution": "Mirantis",
    "distribution_version": "8.0",
    "last_scanned:": "5/8/16",
    "name": "Mirantis-Liberty-Nvn",
    "operational": "yes",
    "type": "environment"
}

SCAN_TYPE_RESULTS = [
    {
        "description": "",
        "enabled": True,
        "id": "75c0eb79ff4a42b0ae4973c8375ddf40",
        "name": "OSDNA-project"
    },
    {
        "description": "admin tenant",
        "enabled": True,
        "id": "8c1751e0ce714736a63fee3c776164da",
        "name": "admin"
    }
]

LIMIT_TO_CHILD_ID = "75c0eb79ff4a42b0ae4973c8375ddf40"
