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

URL = "/cliques"

WRONG_CLIQUE_ID = "58a2406e6a283a8bee15d43"
CORRECT_CLIQUE_ID = "58a2406e6a283a8bee15d43f"
NONEXISTENT_CLIQUE_ID = "58a2406e6a283a8bee15d43e"

WRONG_FOCAL_POINT = "58a2406e6a283a8bee15d43"
CORRECT_FOCAL_POINT = "58a2406e6a283a8bee15d43f"

WRONG_LINK_ID = "58a2406e6a283a8bee15d43"
CORRECT_LINK_ID = "58a2406e6a283a8bee15d43f"
NONEXISTENT_LINK_ID = "58a2406e6a283a8bee15d43e"

WRONG_FOCAL_POINT_TYPE = base.WRONG_OBJECT_TYPE
CORRECT_FOCAL_POINT_TYPE = base.CORRECT_OBJECT_TYPE

WRONG_LINK_TYPE = base.WRONG_LINK_TYPE
CORRECT_LINK_TYPE = base.CORRECT_LINK_TYPE

CLIQUES_WITH_SPECIFIC_ID = [
    {
        "environment": "Mirantis-Liberty-API",
        "focal_point_type": "vnic",
        "id": CORRECT_CLIQUE_ID
    }
]

CLIQUES_WITH_SPECIFIC_FOCAL_POINT_TYPE = [
    {
        "environment": "Mirantis-Liberty-API",
        "focal_point_type": CORRECT_FOCAL_POINT_TYPE,
        "id": "576c119a3f4173144c7a75c5"
    },
    {
        "environment": "Mirantis-Liberty-API",
        "focal_point_type": CORRECT_FOCAL_POINT_TYPE,
        "id": "576c119a3f4173144c7a75cc6"
    }
]

CLIQUES_WITH_SPECIFIC_FOCAL_POINT_TYPE_RESPONSE = {
    "cliques": CLIQUES_WITH_SPECIFIC_FOCAL_POINT_TYPE
}

CLIQUES_WITH_SPECIFIC_FOCAL_POINT = [
    {
        "environment": "Mirantis-Liberty-API",
        "focal_point": CORRECT_FOCAL_POINT,
        "id": "576c119a3f4173144c7a75c5"
    },
    {
        "environment": "Mirantis-Liberty-API",
        "focal_point": CORRECT_FOCAL_POINT,
        "id": "576c119a3f4173144c7a758e"
    }
]

CLIQUES_WITH_SPECIFIC_FOCAL_POINT_RESPONSE = {
    "cliques": CLIQUES_WITH_SPECIFIC_FOCAL_POINT
}

CLIQUES_WITH_SPECIFIC_LINK_TYPE = [
    {
        "links_detailed": [
            {
                "link_type": CORRECT_LINK_TYPE,
                "_id": "58a2405a6a283a8bee15d42f"
            },
            {
                "link_type": "vnic-vconnector",
                "_id": "58a240056a283a8bee15d3f2"
            }
        ],
        "environment": "Mirantis-Liberty-API",
        "focal_point_type": "vnic",
        "id": "576c119a3f4173144c7a75c5"
    },
    {
        "links_detailed": [
            {
                "link_type": CORRECT_LINK_TYPE,
                "_id": "58a2405a6a283a8bee15d42f"
            }
        ],
        "environment": "Mirantis-Liberty-API",
        "focal_point_type": "pnic",
        "id": "576c119a3f4173144c7a75c7"
    }
]

CLIQUES_WITH_SPECIFIC_LINK_TYPE_RESPONSE = {
    "cliques": CLIQUES_WITH_SPECIFIC_LINK_TYPE
}

CLIQUES_WITH_SPECIFIC_LINK_ID = [
    {
        "links_detailed": [
            {
                "_id": CORRECT_LINK_ID
            },
            {
                "_id": "58a240056a283a8bee15d3f2"
            }
        ],
        "environment": "Mirantis-Liberty-API",
        "focal_point_type": "vnic",
        "id": "576c119a3f4173144c7a75c5"
    },
    {
        "links_detailed": [
            {
                "_id": CORRECT_LINK_ID
            }
        ],
        "environment": "Mirantis-Liberty-API",
        "focal_point_type": "pnic",
        "id": "576c119a3f4173144c7a75c7"
    }
]

CLIQUES_WITH_SPECIFIC_LINK_ID_RESPONSE = {
    "cliques": CLIQUES_WITH_SPECIFIC_LINK_ID
}

# response
CLIQUES = [{
    "links_detailed": [
        {
            "link_type": "instance-vnic",
            "_id": "58a2405a6a283a8bee15d42f"
        },
        {
            "link_type": "vnic-vconnector",
            "_id": "58a240056a283a8bee15d3f2"
        }
    ],
    "environment": "Mirantis-Liberty-API",
    "focal_point_type": "vnic",
    "id": "576c119a3f4173144c7a75c5"
    },
    {
    "links_detailed": [
        {
            "link_type": "instance-vnic",
            "_id": "58a2405a6a283a8bee15d42f"
        },
        {
            "link_type": "vnic-vconnector",
            "_id": "58a240056a283a8bee15d3f2"
        }
    ],
    "environment": "Miratis-Liberty-API",
    "focal_point_type": "pnic",
    "id": "576c119a3f4173144c7a75c6"
    }
]

CLIQUES_RESPONSE = {
    "cliques": CLIQUES
}
