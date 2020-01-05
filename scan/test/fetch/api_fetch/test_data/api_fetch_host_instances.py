###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
PROJECT_LIST = [
    {
        'name': 'OSDNA-project',
    }, 
    {
        'name': 'admin',
    }
]

HOST = {
    'host_type': ['Compute'], 
}

NON_COMPUTE_HOST = {
    'host_type': [],
}

HOST_NAME = "node-5.cisco.com"

GET_INSTANCES_FROM_API = [
    {
        "host": "node-5.cisco.com",
        "id": "6f29c867-9150-4533-8e19-70d749b172fa",
        "local_name": "instance-00000002",
        "uuid": "6f29c867-9150-4533-8e19-70d749b172fa"
    },
    {
        "host": "node-5.cisco.com",
        "id": "79e20dbf-a46d-46ee-870b-e0c9f7b357d9",
        "local_name": "instance-0000001c",
        "uuid": "79e20dbf-a46d-46ee-870b-e0c9f7b357d9"
    },
    {
        "host": "node-5.cisco.com",
        "id": "bf0cb914-b316-486c-a4ce-f22deb453c52",
        "local_name": "instance-00000026",
        "uuid": "bf0cb914-b316-486c-a4ce-f22deb453c52"
    }
]

GET_SERVERS_RESPONSE = {
    "hypervisors": [
        {
            "hypervisor_hostname": "node-5.cisco.com",
            "id": 1,
            "servers": [
                {
                    "name": "instance-00000002",
                    "uuid": "6f29c867-9150-4533-8e19-70d749b172fa"
                },
                {
                    "name": "instance-0000001c",
                    "uuid": "79e20dbf-a46d-46ee-870b-e0c9f7b357d9"
                },
                {
                    "name": "instance-00000026",
                    "uuid": "bf0cb914-b316-486c-a4ce-f22deb453c52"
                }
            ]
        }
    ]
}

RESPONSE_WITHOUT_HYPERVISORS = {
    "text": "test"
}

RESPONSE_WITHOUT_SERVERS = {
    "hypervisors": [
        {

        }
    ]
}

INSTANCE_FOLDER_ID = "node-5.cisco.com-instances"
