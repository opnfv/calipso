###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
PORTS_RESPONSE = {
    "ports": [
        {
            "id": "16620a58-c48c-4195-b9c1-779a8ba2e6f8",
            "mac_address": "fa:16:3e:d7:c5:16",
            "name": "",
            "network_id": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
            "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40"
        }
    ]
}

PORTS_RESULT_WITH_NET = [
    {
        "id": "16620a58-c48c-4195-b9c1-779a8ba2e6f8",
        "mac_address": "fa:16:3e:d7:c5:16",
        "name": "fa:16:3e:d7:c5:16",
        "network_id": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
        "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
        "type": "port",
        "master_parent_type": "network",
        "master_parent_id": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
        "parent_type": "ports_folder",
        "parent_id": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe-ports",
        "parent_text": "Ports",
    }
]

PORTS_RESULT_WITHOUT_NET = [
    {
        "id": "16620a58-c48c-4195-b9c1-779a8ba2e6f8",
        "mac_address": "fa:16:3e:d7:c5:16",
        "name": "16620a58-c48c-4195-b9c1-779a8ba2e6f8",
        "network_id": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
        "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
        "type": "port",
        "master_parent_type": "network",
        "master_parent_id": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
        "parent_type": "ports_folder",
        "parent_id": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe-ports",
        "parent_text": "Ports",
    }
]

PORTS_RESULT_WITH_PROJECT = [
    {
        "id": "16620a58-c48c-4195-b9c1-779a8ba2e6f8",
        "mac_address": "fa:16:3e:d7:c5:16",
        "name": "fa:16:3e:d7:c5:16",
        "network_id": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
        "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
        "type": "port",
        "master_parent_type": "network",
        "master_parent_id": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe",
        "parent_type": "ports_folder",
        "parent_id": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe-ports",
        "parent_text": "Ports",
        "project": "Calipso-project"
    }
]

ERROR_PORTS_RESPONSE = {}
NETWORK = {"id": "b6fd5175-4b22-4256-9b1a-9fc4b9dce1fe"}
TENANT = {"id": "75c0eb79ff4a42b0ae4973c8375ddf40", "name": "Calipso-project"}
ENDPOINT = "http://10.56.20.239:9696"
REGION_NAME = "RegionOne"
