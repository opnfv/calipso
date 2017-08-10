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


URL = "/links"

UNKNOWN_HOST = "unknown host"

WRONG_TYPE = base.WRONG_LINK_TYPE
CORRECT_TYPE = base.CORRECT_LINK_TYPE

WRONG_STATE = base.WRONG_LINK_STATE
CORRECT_STATE = base.CORRECT_LINK_STATE

LINK_ID = "58ca73ae3a8a836d10ff3b45"
WRONG_LINK_ID = "58ca73ae3a8a836d10ff3b4"
NONEXISTENT_LINK_ID = "58ca73ae3a8a836d10ff3b46"

LINKS_WITH_SPECIFIC_TYPE = [
    {
        "id": "58ca73ae3a8a836d10ff3bb5",
        "host": "node-1.cisco.com",
        "link_type": CORRECT_TYPE,
        "link_name": "Segment-103",
        "environment": "Mirantis-Liberty-API"
    },
    {
        "id": "58ca73ae3a8a836d10ff3b4d",
        "host": "node-1.cisco.com",
        "link_type": CORRECT_TYPE,
        "link_name": "Segment-104",
        "environment": "Mirantis-Liberty-API"
    }
]


LINKS_WITH_SPECIFIC_STATE = [
    {
        "id": "58ca73ae3a8a836d10ff3bb5",
        "host": "node-1.cisco.com",
        "state": CORRECT_STATE,
        "environment": "Mirantis-Liberty-API"
    },
    {
        "id": "58ca73ae3a8a836d10ff3b4d",
        "host": "node-1.cisco.com",
        "state": CORRECT_STATE,
        "environment": "Mirantis-Liberty-API"
    }
]

LINKS_WITH_SPECIFIC_STATE_RESPONSE = {
    "links": LINKS_WITH_SPECIFIC_STATE
}

LINKS_WITH_SPECIFIC_TYPE_RESPONSE = {
    "links": LINKS_WITH_SPECIFIC_TYPE
}

LINKS_WITH_SPECIFIC_ID = [
    {
        "id": LINK_ID,
        "host": "node-1.cisco.com",
        "link_type": "host_pnic-network",
        "link_name": "Segment-103",
        "environment": "Mirantis-Liberty-API"
    }
]

LINKS = [
    {
        "id": "58ca73ae3a8a836d10ff3b45",
        "host": "node-1.cisco.com",
        "link_type": "host_pnic-network",
        "link_name": "Segment-103",
        "environment": "Mirantis-Liberty-API"
    }
]

LINKS_LIST_RESPONSE = {
    "links": LINKS
}
