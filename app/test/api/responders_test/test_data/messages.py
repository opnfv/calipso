###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from test.api.responders_test.test_data import base

# url
URL = "/messages"

NONEXISTENT_MESSAGE_ID = "80b5e074-0f1a-4b67-810c-fa9c92d41a9f"
MESSAGE_ID = "80b5e074-0f1a-4b67-810c-fa9c92d41a98"

WRONG_SEVERITY = base.WRONG_MESSAGE_SEVERITY
CORRECT_SEVERITY = base.CORRECT_MESSAGE_SEVERITY

WRONG_RELATED_OBJECT_TYPE = base.WRONG_OBJECT_TYPE
CORRECT_RELATED_OBJECT_TYPE = base.CORRECT_OBJECT_TYPE

RELATED_OBJECT = "instance"
NONEXISTENT_RELATED_OBJECT = "nonexistent-instance"

WRONG_FORMAT_TIME = base.WRONG_FORMAT_TIME
CORRECT_FORMAT_TIME = base.CORRECT_FORMAT_TIME

MESSAGES_WITH_SPECIFIC_TIME = [
    {
        "level": "info",
        "environment": "Mirantis-Liberty-API",
        "id": "3c64fe31-ca3b-49a3-b5d3-c485d7a452e7",
        "source_system": "OpenStack",
        "timestamp": CORRECT_FORMAT_TIME
    }
]

MESSAGES_WITH_SPECIFIC_TIME_RESPONSE = {
    "messages": MESSAGES_WITH_SPECIFIC_TIME
}

MESSAGES_WITH_SPECIFIC_SEVERITY = [
    {
        "level": CORRECT_SEVERITY,
        "environment": "Mirantis-Liberty-API",
        "id": "3c64fe31-ca3b-49a3-b5d3-c485d7a452e7",
        "source_system": "OpenStack"
    },
    {
        "level": CORRECT_SEVERITY,
        "environment": "Mirantis-Liberty-API",
        "id": "c7071ec0-04db-4820-92ff-3ed2b916738f",
        "source_system": "OpenStack"
    },
]

MESSAGES_WITH_SPECIFIC_SEVERITY_RESPONSE = {
    "messages": MESSAGES_WITH_SPECIFIC_SEVERITY
}

MESSAGES_WITH_SPECIFIC_RELATED_OBJECT_TYPE = [
    {
        "level": "info",
        "environment": "Mirantis-Liberty-API",
        "related_object_type": CORRECT_RELATED_OBJECT_TYPE,
        "id": "3c64fe31-ca3b-49a3-b5d3-c485d7a452e7"
    },
    {
        "level": "error",
        "environment": "Mirantis-Liberty-API",
        "related_object_type": CORRECT_RELATED_OBJECT_TYPE,
        "id": "c7071ec0-04db-4820-92ff-3ed2b916738f"
    },
]

MESSAGES_WITH_SPECIFIC_RELATED_OBJECT_TYPE_RESPONSE = {
    "messages": MESSAGES_WITH_SPECIFIC_RELATED_OBJECT_TYPE
}

MESSAGES_WITH_SPECIFIC_ID = [
    {
         "level": "info",
         "environment": "Mirantis-Liberty",
         "id": MESSAGE_ID,
         "source_system": "OpenStack"
    }
]

MESSAGES = [
    {
         "level": "info",
         "environment": "Mirantis-Liberty",
         "id": "3c64fe31-ca3b-49a3-b5d3-c485d7a452e7",
         "source_system": "OpenStack"
    },
    {
        "level": "info",
        "environment": "Mirantis-Liberty",
        "id": "c7071ec0-04db-4820-92ff-3ed2b916738f",
        "source_system": "OpenStack"
    },
]

MESSAGES_RESPONSE = {
    "messages": MESSAGES
}
