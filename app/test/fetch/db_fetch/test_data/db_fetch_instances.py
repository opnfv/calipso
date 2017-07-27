INSTANCES_FROM_API = [
    {
        "host": "node-5.cisco.com",
        "id": "6f29c867-9150-4533-8e19-70d749b172fa",
    }
]

INSTANCES_FROM_DB = [
    {
        "host": "node-5.cisco.com",
        "id": "6f29c867-9150-4533-8e19-70d749b172fa",
        "network_info": "[{\"network\": {\"id\": \"7e59b726-d6f4-451a-a574-c67a920ff627\"}}]",
        "project": "Calipso-project",
    },
    {
        "host": "node-5.cisco.com",
        "id": "bf0cb914-b316-486c-a4ce-f22deb453c52",
        "network_info": "[{\"network\": {\"id\": \"7e59b726-d6f4-451a-a574-c67a920ff627\"}}]",
        "project": "Calipso-project",
    }
]

UPDATED_INSTANCES_DATA = [
    {
        "host": "node-5.cisco.com",
        "id": "6f29c867-9150-4533-8e19-70d749b172fa",
        "network": ["7e59b726-d6f4-451a-a574-c67a920ff627"],
        "type": "instance",
        "parent_type": "instances_folder",
        "parent_id": "node-5.cisco.com-instances",
        "in_project-Calipso-project": "1",
        "network_info": [
            {
                "network": {
                    "id": "7e59b726-d6f4-451a-a574-c67a920ff627"
                }
            }
        ]
    }
]

INSTANCE_WITH_NETWORK = {
    "host": "node-5.cisco.com",
    "id": "6f29c867-9150-4533-8e19-70d749b172fa",
    "network_info": "[{\"network\": {\"id\": \"7e59b726-d6f4-451a-a574-c67a920ff627\"}}]",
    "project": "Calipso-project",
}

INSTANCE_WITH_NETWORK_RESULT = {
    "host": "node-5.cisco.com",
    "id": "6f29c867-9150-4533-8e19-70d749b172fa",
    "network": ["7e59b726-d6f4-451a-a574-c67a920ff627"],
    "type": "instance",
    "parent_type": "instances_folder",
    "parent_id": "node-5.cisco.com-instances",
    "in_project-Calipso-project": "1",
    "network_info": [
        {
            "network": {
                "id": "7e59b726-d6f4-451a-a574-c67a920ff627"
            }
        }
    ]
}

INSTANCE_WITHOUT_NETWORK = {
    "host": "node-5.cisco.com",
    "id": "6f29c867-9150-4533-8e19-70d749b172fa",
    "network_info": "[]",
    "project": "Calipso-project",
}

INSTANCE_WITHOUT_NETWORK_RESULT = {
    "host": "node-5.cisco.com",
    "id": "6f29c867-9150-4533-8e19-70d749b172fa",
    "network": [],
    "type": "instance",
    "parent_type": "instances_folder",
    "parent_id": "node-5.cisco.com-instances",
    "in_project-Calipso-project": "1",
    "network_info": []
}
