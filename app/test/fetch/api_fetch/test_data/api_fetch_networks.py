NETWORKS_RESPONSE = {
    "networks": [
        {
            "id": "8673c48a-f137-4497-b25d-08b7b218fd17",
            "subnets": [
                "cae3c81d-9a27-48c4-b8f6-32867ca03134"
            ],
            "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40"
        }
    ]
}

NETWORKS_RESULT = [
    {
        "id": "8673c48a-f137-4497-b25d-08b7b218fd17",
        "subnets": {
            "test23":  {
                "cidr": "172.16.12.0/24",
                "id": "cae3c81d-9a27-48c4-b8f6-32867ca03134",
                "name": "test23",
                "network_id": "0abe6331-0d74-4bbd-ad89-a5719c3793e4",
                "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40"
            }
        },
        "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
        "master_parent_type": "project",
        "master_parent_id": "75c0eb79ff4a42b0ae4973c8375ddf40",
        "parent_type": "networks_folder",
        "parent_id": "75c0eb79ff4a42b0ae4973c8375ddf40-networks",
        "parent_text": "Networks",
        "project": "Calipso-project",
        "cidrs": ["172.16.12.0/24"],
        "subnet_ids": ["cae3c81d-9a27-48c4-b8f6-32867ca03134"],
        "network": "8673c48a-f137-4497-b25d-08b7b218fd17"
    }
]

WRONG_NETWORK_RESPONSE = {
}

SUBNETS_RESPONSE = {
    "subnets": [
        {
            "cidr": "172.16.12.0/24",
            "id": "cae3c81d-9a27-48c4-b8f6-32867ca03134",
            "name": "test23",
            "network_id": "0abe6331-0d74-4bbd-ad89-a5719c3793e4",
            "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40"
        }
    ]
}

ENDPOINT = "http://10.56.20.239:9696"
WRONG_SUBNETS_RESPONSE = {}

PROJECT = {
        "description": "",
        "enabled": True,
        "id": "75c0eb79ff4a42b0ae4973c8375ddf40",
        "name": "Calipso-project"
    }

REGION_NAME = "RegionOne"
