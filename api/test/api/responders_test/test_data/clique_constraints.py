###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from api.test.api.responders_test.test_data import base

URL = "/clique_constraints"

WRONG_ID = base.WRONG_OBJECT_ID
NONEXISTENT_ID = "576a4176a83d5313f21971f0"
CORRECT_ID = base.CORRECT_OBJECT_ID

WRONG_FOCAL_POINT_TYPE = base.WRONG_OBJECT_TYPE
CORRECT_FOCAL_POINT_TYPE = base.CORRECT_OBJECT_TYPE

CONSTRAINT = "network"

CLIQUE_CONSTRAINTS_WITH_SPECIFIC_ID = [
    {
       "id": CORRECT_ID
    }
]

CLIQUE_CONSTRAINTS_WITH_SPECIFIC_FOCAL_POINT_TYPE = [
    {
       "id": "576a4176a83d5313f21971f5",
       "focal_point_type": CORRECT_FOCAL_POINT_TYPE
    },
    {
        "id": "576ac7069f6ba3074882b2eb",
        "focal_point_type": CORRECT_FOCAL_POINT_TYPE
    }
]

CLIQUE_CONSTRAINTS_WITH_SPECIFIC_FOCAL_POINT_TYPE_RESPONSE = {
    "clique_constraints": CLIQUE_CONSTRAINTS_WITH_SPECIFIC_FOCAL_POINT_TYPE
}

CLIQUE_CONSTRAINTS_WITH_SPECIFIC_CONSTRAINT = [
    {
        "id": "576a4176a83d5313f21971f5",
        "constraints": [
            CONSTRAINT
        ]
    },
    {
        "id": "576ac7069f6ba3074882b2eb",
        "constraints": [
            CONSTRAINT
        ]
    }
]

CLIQUE_CONSTRAINTS_WITH_SPECIFIC_CONSTRAINT_RESPONSE = {
    "clique_constraints": CLIQUE_CONSTRAINTS_WITH_SPECIFIC_CONSTRAINT
}

CLIQUE_CONSTRAINTS = [
    {
       "id": "576a4176a83d5313f21971f5"
    },
    {
        "id": "576ac7069f6ba3074882b2eb"
    }
]

CLIQUE_CONSTRAINTS_RESPONSE = {
    "clique_constraints": CLIQUE_CONSTRAINTS
}
