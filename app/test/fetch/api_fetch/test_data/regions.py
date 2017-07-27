###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
REGIONS = {
            "RegionOne": {
            "endpoints": {
                "ceilometer": {
                    "adminURL": "http://192.168.0.2:8777",
                    "id": "617177a3dcb64560a5a79ab0a91a7225",
                    "internalURL": "http://192.168.0.2:8777",
                    "publicURL": "http://172.16.0.3:8777",
                    "service_type": "metering"
                },
                "cinder": {
                    "adminURL": "http://192.168.0.2:8776/v1/8c1751e0ce714736a63fee3c776164da",
                    "id": "05643f2cf9094265b432376571851841",
                    "internalURL": "http://192.168.0.2:8776/v1/8c1751e0ce714736a63fee3c776164da",
                    "publicURL": "http://172.16.0.3:8776/v1/8c1751e0ce714736a63fee3c776164da",
                    "service_type": "volume"
                },
                "cinderv2": {
                    "adminURL": "http://192.168.0.2:8776/v2/8c1751e0ce714736a63fee3c776164da",
                    "id": "2c30937688e944889db4a64fab6816e6",
                    "internalURL": "http://192.168.0.2:8776/v2/8c1751e0ce714736a63fee3c776164da",
                    "publicURL": "http://172.16.0.3:8776/v2/8c1751e0ce714736a63fee3c776164da",
                    "service_type": "volumev2"
                },
                "glance": {
                    "adminURL": "http://192.168.0.2:9292",
                    "id": "475c6c77a94e4e63a5a0f0e767f697a8",
                    "internalURL": "http://192.168.0.2:9292",
                    "publicURL": "http://172.16.0.3:9292",
                    "service_type": "image"
                },
                "heat": {
                    "adminURL": "http://192.168.0.2:8004/v1/8c1751e0ce714736a63fee3c776164da",
                    "id": "9e60268a5aaf422d9e42f0caab0a19b4",
                    "internalURL": "http://192.168.0.2:8004/v1/8c1751e0ce714736a63fee3c776164da",
                    "publicURL": "http://172.16.0.3:8004/v1/8c1751e0ce714736a63fee3c776164da",
                    "service_type": "orchestration"
                },
                "heat-cfn": {
                    "adminURL": "http://192.168.0.2:8000/v1",
                    "id": "0f04ec6ed49f4940822161bf677bdfb2",
                    "internalURL": "http://192.168.0.2:8000/v1",
                    "publicURL": "http://172.16.0.3:8000/v1",
                    "service_type": "cloudformation"
                },
                "keystone": {
                    "adminURL": "http://192.168.0.2:35357/v2.0",
                    "id": "404cceb349614eb39857742970408301",
                    "internalURL": "http://192.168.0.2:5000/v2.0",
                    "publicURL": "http://172.16.0.3:5000/v2.0",
                    "service_type": "identity"
                },
                "neutron": {
                    "adminURL": "http://192.168.0.2:9696",
                    "id": "8dc28584da224c4b9671171ead3c982a",
                    "internalURL": "http://192.168.0.2:9696",
                    "publicURL": "http://172.16.0.3:9696",
                    "service_type": "network"
                },
                "nova": {
                    "adminURL": "http://192.168.0.2:8774/v2/8c1751e0ce714736a63fee3c776164da",
                    "id": "274cbbd9fd6d4311b78e78dd3a1df51f",
                    "internalURL": "http://192.168.0.2:8774/v2/8c1751e0ce714736a63fee3c776164da",
                    "publicURL": "http://172.16.0.3:8774/v2/8c1751e0ce714736a63fee3c776164da",
                    "service_type": "compute"
                },
                "nova_ec2": {
                    "adminURL": "http://192.168.0.2:8773/services/Admin",
                    "id": "390dddc753cc4d378b489129d06c4b7d",
                    "internalURL": "http://192.168.0.2:8773/services/Cloud",
                    "publicURL": "http://172.16.0.3:8773/services/Cloud",
                    "service_type": "ec2"
                },
                "novav3": {
                    "adminURL": "http://192.168.0.2:8774/v3",
                    "id": "1df917160dfb4ce5b469764fde22b3ab",
                    "internalURL": "http://192.168.0.2:8774/v3",
                    "publicURL": "http://172.16.0.3:8774/v3",
                    "service_type": "computev3"
                },
                "swift": {
                    "adminURL": "http://192.168.0.2:8080/v1/AUTH_8c1751e0ce714736a63fee3c776164da",
                    "id": "12e78e06595f48339baebdb5d4309c70",
                    "internalURL": "http://192.168.0.2:8080/v1/AUTH_8c1751e0ce714736a63fee3c776164da",
                    "publicURL": "http://172.16.0.3:8080/v1/AUTH_8c1751e0ce714736a63fee3c776164da",
                    "service_type": "object-store"
                },
                "swift_s3": {
                    "adminURL": "http://192.168.0.2:8080",
                    "id": "4f655c8f2bef46a0a7ba4a20bba53666",
                    "internalURL": "http://192.168.0.2:8080",
                    "publicURL": "http://172.16.0.3:8080",
                    "service_type": "s3"
                }
            },
            "id": "RegionOne",
            "name": "RegionOne",
            "parent_id": "Mirantis-Liberty-Xiaocong-regions",
            "parent_type": "regions_folder"
        }
}