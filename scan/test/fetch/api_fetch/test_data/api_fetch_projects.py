###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
PROJECTS_CORRECT_RESPONSE = {
    "projects": [
        {
            "name": "Calipso-project"
        },
        {
            "name": "admin",
        }
    ]
}

PROJECT_RESULT = [
    "Calipso-project",
    "admin"
]

PROJECTS_RESPONSE_WITHOUT_PROJECTS = ""

REGION_PROJECTS = [
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

USERS_PROJECTS = [
    "OSDNA-project",
    "admin"
]

REGION_URL_NOVER = "http://10.56.20.239:35357"

REGION_RESPONSE = {
    "tenants": [
        {
            "name": "Calipso-project"
        },
        {
            "name": "admin"
        },
        {
            "name": "services"
        }
    ]
}

REGION_RESULT = [
    {
        "name": "Calipso-project"
    },
    {
        "name": "admin"
    }
]

REGION_RESULT_WITH_NON_USER_PROJECT = [
    {
        "name": "Calipso-project"
    },
    {
        "name": "admin"
    },
    {
        "name": "non-user project"
    }
]

REGION_ERROR_RESPONSE = []

REGION_NAME = "RegionOne"
PROJECT_ID = "admin"
