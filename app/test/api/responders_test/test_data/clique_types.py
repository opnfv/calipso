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


URL = "/clique_types"

WRONG_ID = base.WRONG_OBJECT_ID
NONEXISTENT_ID = "58ca73ae3a8a836d10ff3b44"
CORRECT_ID = base.CORRECT_OBJECT_ID

WRONG_FOCAL_POINT_TYPE = base.WRONG_OBJECT_TYPE
CORRECT_FOCAL_POINT_POINT_TYPE = base.CORRECT_OBJECT_TYPE

WRONG_LINK_TYPE = base.WRONG_LINK_TYPE
NONEXISTENT_LINK_TYPE = "otep-pnic"
CORRECT_LINK_TYPE = base.CORRECT_LINK_TYPE

CLIQUE_TYPES_WITH_SPECIFIC_ID = [
    {
       "environment": "Mirantis-Liberty-API",
       "focal_point_type": "pnic",
       "id": CORRECT_ID
    }
]

CLIQUE_TYPES_WITH_SPECIFIC_FOCAL_POINT_TYPE = [
    {
       "environment": "Mirantis-Liberty-API",
       "focal_point_type": CORRECT_FOCAL_POINT_POINT_TYPE,
       "id": "58ca73ae3a8a836d10ff3b80"
    },
    {
       "environment": "Mirantis-Liberty-API",
       "focal_point_type": CORRECT_FOCAL_POINT_POINT_TYPE,
       "id": "58ca73ae3a8a836d10ff3b81"
    }
]

CLIQUE_TYPES_WITH_SPECIFIC_FOCAL_POINT_TYPE_RESPONSE = {
    "clique_types": CLIQUE_TYPES_WITH_SPECIFIC_FOCAL_POINT_TYPE
}

CLIQUE_TYPES_WITH_SPECIFIC_LINK_TYPE = [
    {
       "environment": "Mirantis-Liberty-API",
       "link_types": [
          CORRECT_LINK_TYPE
       ],
       "id": "58ca73ae3a8a836d10ff3b80"
    },
    {
       "environment": "Mirantis-Liberty-API",
       "link_types": [
           CORRECT_LINK_TYPE
       ],
       "id": "58ca73ae3a8a836d10ff3b81"
    }
]

CLIQUE_TYPES_WITH_SPECIFIC_LINK_TYPE_RESPONSE = {
    "clique_types": CLIQUE_TYPES_WITH_SPECIFIC_LINK_TYPE
}

CLIQUE_TYPES = [
    {
       "environment": "Mirantis-Liberty-API",
       "focal_point_type": "vnic",
       "id": "58ca73ae3a8a836d10ff3b80"
    },
    {
       "environment": "Mirantis-Liberty-API",
       "focal_point_type": "vnic",
       "id": "58ca73ae3a8a836d10ff3b81"
    }
]

CLIQUE_TYPES_RESPONSE = {
    "clique_types": CLIQUE_TYPES
}

NON_DICT_CLIQUE_TYPE = base.NON_DICT_OBJ

CLIQUE_TYPE_WITHOUT_ENVIRONMENT = {
    "name": "instance_vconnector_clique",
    "link_types": [
        "instance-vnic",
        "vnic-vconnector"
    ],
    "focal_point_type": "instance"
}

CLIQUE_TYPE_WITH_UNKNOWN_ENVIRONMENT = {
    "environment": base.UNKNOWN_ENV,
    "id": "589a3969761b0555a3ef6093",
    "name": "instance_vconnector_clique",
    "link_types": [
        "instance-vnic",
        "vnic-vconnector"
    ],
    "focal_point_type": "instance"
}

CLIQUE_TYPE_WITHOUT_FOCAL_POINT_TYPE = {
    "environment": "Mirantis-Liberty-API",
    "name": "instance_vconnector_clique",
    "link_types": [
        "instance-vnic",
        "vnic-vconnector"
    ]
}

CLIQUE_TYPE_WITH_WRONG_FOCAL_POINT_TYPE = {
    "environment": "Mirantis-Liberty-API",
    "name": "instance_vconnector_clique",
    "link_types": [
        "instance-vnic",
        "vnic-vconnector"
    ],
    "focal_point_type": WRONG_FOCAL_POINT_TYPE
}

CLIQUE_TYPE_WITHOUT_LINK_TYPES = {
    "environment": "Mirantis-Liberty-API",
    "name": "instance_vconnector_clique",
    "focal_point_type": "instance"
}

CLIQUE_TYPE_WITH_NON_LIST_LINK_TYPES = {
    "environment": "Mirantis-Liberty-API",
    "name": "instance_vconnector_clique",
    "link_types": "instance-vnic",
    "focal_point_type": "instance"
}

CLIQUE_TYPE_WITH_WRONG_LINK_TYPE = {
    "environment": "Mirantis-Liberty-API",
    "name": "instance_vconnector_clique",
    "link_types": [
        WRONG_LINK_TYPE,
        "vnic-vconnector"
    ],
    "focal_point_type": "instance"
}

CLIQUE_TYPE_WITHOUT_NAME = {
    "environment": "Mirantis-Liberty-API",
    "link_types": [
        "instance-vnic",
        "vnic-vconnector",
    ],
    "focal_point_type": "instance"
}

CLIQUE_TYPE = {
    "environment": "Mirantis-Liberty-API",
    "name": "instance_vconnector_clique",
    "link_types": [
        "instance-vnic",
        "vnic-vconnector"
    ],
    "focal_point_type": "instance"
}
