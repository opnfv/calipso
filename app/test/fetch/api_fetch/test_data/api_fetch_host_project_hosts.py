HOST_DOC = {
    "host": "node-6.cisco.com",
    "host_type": [],
    "id": "node-6.cisco.com",
    "name": "node-6.cisco.com",
    "parent_id": "internal",
    "parent_type": "availability_zone",
    "services": {
        "nova-cert": {
            "active": True,
            "available": True,
        },
        "nova-conductor": {
            "active": True,
            "available": True,
        },
        "nova-consoleauth": {
            "active": True,
            "available": True,
        },
        "nova-scheduler": {
            "active": True,
            "available": True,
        }
    },
    "zone": "internal"
}

NONEXISTENT_TYPE = "nova"
COMPUTE_TYPE = "Compute"
ZONE = "internal"
HOST_ZONE = "Test"

REGION_NAME = "RegionOne"
TEST_PROJECT_NAME = "Test"
PROJECT_NAME = "admin"

AVAILABILITY_ZONE_RESPONSE = {
    "availabilityZoneInfo": [
        {
            "hosts": {
                "node-6.cisco.com": {
                    "nova-cert": {
                        "active": True,
                        "available": True,
                    },
                    "nova-conductor": {
                        "active": True,
                        "available": True,
                    },
                    "nova-consoleauth": {
                        "active": True,
                        "available": True,
                    },
                    "nova-scheduler": {
                        "active": True,
                        "available": True,
                    }
                }
            },
            "zoneName": "internal",
            "zoneState": {
                "available": True
            }
        },
        {
            "hosts": {
                "node-5.cisco.com": {
                    "nova-compute": {
                        "active": True,
                        "available": True,
                    }
                }
            },
            "zoneName": "osdna-zone",
            "zoneState": {
                "available": True
            }
        }
    ]
}

AVAILABILITY_ERROR_RESPONSE = {'status': 400}

HYPERVISORS_RESPONSE = {
    "hypervisors": []
}

HYPERVISORS_ERROR_RESPONSE = {'status': 400}

HOST_TO_BE_FETCHED_IP = {
    "host": "node-5.cisco.com",
    "id": "node-5.cisco.com"
}

IP_ADDRESS_RESPONSE = [
    {
        "ip_address": "192.168.0.4"
    }
]

HOSTS_TO_BE_FETCHED_NETWORK_DETAILS = [
    {
        "host": "node-6.cisco.com",
        "host_type": [
            "Controller"
        ],
        "id": "node-6.cisco.com",
        "name": "node-6.cisco.com",
    },
    {
        "host": "node-5.cisco.com",
        "host_type": [
            "Compute"
        ],
        "id": "node-5.cisco.com",
        "name": "node-5.cisco.com",
    }
]

NETWORKS_DETAILS_RESPONSE = [
    {
        "configurations": "{}",
        "host": "node-6.cisco.com"
    },
    {
        "configurations": "{}",
        "host": "node-6.cisco.com",
    },
    {
        "configurations": "{}",
        "host": "node-6.cisco.com",
    }
]

REGION_URL = "http://192.168.0.2:8776/v2/329e0576da594c62a911d0dccb1238a7"
AVAILABILITY_ZONE = {
    "hosts": {
                "node-6.cisco.com": {
                    "nova-cert": {
                        "active": True,
                        "available": True,
                    },
                    "nova-conductor": {
                        "active": True,
                        "available": True,
                    },
                    "nova-consoleauth": {
                        "active": True,
                        "available": True,
                    },
                    "nova-scheduler": {
                        "active": True,
                        "available": True,
                    }
                }
            },
    "zoneName": "internal"
}

HOST_NAME = "node-6.cisco.com"

GET_FOR_REGION_INFO = [
    {
        "config": {
        },
        "host": "node-6.cisco.com",
        "host_type": [
            "Controller",
            "Network"
        ],
        "id": "node-6.cisco.com",
        "name": "node-6.cisco.com",
        "parent_id": "internal",
        "parent_type": "availability_zone",
        "services": {
            "nova-cert": {
                "active": True,
                "available": True,
            },
            "nova-conductor": {
                "active": True,
                "available": True,
            },
            "nova-consoleauth": {
                "active": True,
                "available": True,
            },
            "nova-scheduler": {
                "active": True,
                "available": True,
            }
        },
        "zone": "internal"
    },
    {
        "host": "node-5.cisco.com",
        "host_type": [
            "Compute"
        ],
        "id": "node-5.cisco.com",
        "ip_address": "192.168.0.4",
        "name": "node-5.cisco.com",
        "os_id": "1",
        "parent_id": "osdna-zone",
        "parent_type": "availability_zone",
        "services": {
            "nova-compute": {
                "active": True,
                "available": True,
                "updated_at": "2016-10-21T18:22:42.000000"
            }
        },
        "zone": "osdna-zone"
    }
]
