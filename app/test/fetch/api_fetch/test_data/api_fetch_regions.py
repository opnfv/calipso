REGION = "RegionOne"
ENV = "Mirantis-Liberty"

AUTH_RESPONSE = {
    "access": {
        "serviceCatalog": [
            {
                "endpoints": [
                    {
                        "adminURL": "http://192.168.0.2:8774/v2/8c1751e0ce714736a63fee3c776164da",
                        "id": "274cbbd9fd6d4311b78e78dd3a1df51f",
                        "internalURL": "http://192.168.0.2:8774/v2/8c1751e0ce714736a63fee3c776164da",
                        "publicURL": "http://172.16.0.3:8774/v2/8c1751e0ce714736a63fee3c776164da",
                        "region": "RegionOne"
                    }
                ],
                "endpoints_links": [],
                "name": "nova",
                "type": "compute"
            }
        ]
    }
}

REGIONS_RESULT = [
    {
        "id": "RegionOne",
        "endpoints": {
            "nova": {
                "adminURL": "http://192.168.0.2:8774/v2/8c1751e0ce714736a63fee3c776164da",
                "id": "274cbbd9fd6d4311b78e78dd3a1df51f",
                "internalURL": "http://192.168.0.2:8774/v2/8c1751e0ce714736a63fee3c776164da",
                "publicURL": "http://172.16.0.3:8774/v2/8c1751e0ce714736a63fee3c776164da",
                "service_type": "compute"
            }
        },
        "name": "RegionOne",
        "parent_type": "regions_folder",
        "parent_id": ENV + "-regions",
    }
]
