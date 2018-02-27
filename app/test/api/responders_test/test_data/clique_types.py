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
from test.api.responders_test.test_data.base import WRONG_MECHANISM_DRIVER, \
    CORRECT_MECHANISM_DRIVER, CORRECT_TYPE_DRIVER, WRONG_TYPE_DRIVER, \
    CORRECT_DISTRIBUTION, CORRECT_DIST_VER

URL = "/clique_types"

WRONG_ID = base.WRONG_OBJECT_ID
NONEXISTENT_ID = "58ca73ae3a8a836d10ff3b44"
CORRECT_ID = base.CORRECT_OBJECT_ID
SAMPLE_IDS = ['58ca73ae3a8a836d10ff3b80', '58ca73ae3a8a836d10ff3b81']

RESERVED_ENV_NAME = 'ANY'

WRONG_FOCAL_POINT_TYPE = base.WRONG_OBJECT_TYPE
CORRECT_FOCAL_POINT_POINT_TYPE = base.CORRECT_OBJECT_TYPE

WRONG_LINK_TYPE = base.WRONG_LINK_TYPE
NONEXISTENT_LINK_TYPE = "otep-host_pnic"
CORRECT_LINK_TYPE = base.CORRECT_LINK_TYPE

CLIQUE_TYPE = {
    "environment": "Mirantis-Liberty-API",
    "name": "instance_vconnector_clique",
    "link_types": [
        "instance-vnic",
        "vnic-vconnector"
    ],
    "focal_point_type": "instance"
}

TEST_CONFIGURATION = {
    "distribution": CORRECT_DISTRIBUTION,
    "distribution_version": CORRECT_DIST_VER,
    "mechanism_drivers": CORRECT_MECHANISM_DRIVER,
    "type_drivers": CORRECT_TYPE_DRIVER
}


def get_payload(update: dict = None, delete: list = None):
    payload = CLIQUE_TYPE.copy()
    if update:
        payload.update(update)
    if delete:
        for k in delete:
            del payload[k]
    return payload


CLIQUE_TYPES_WITH_SPECIFIC_ID = [
    get_payload(update={'id': CORRECT_ID})
]

CLIQUE_TYPES_WITH_SPECIFIC_CONFIGURATION = [
    get_payload(update={'id': SAMPLE_IDS[0],
                        **TEST_CONFIGURATION},
                delete=['environment'])
]

CLIQUE_TYPES_WITH_SPECIFIC_CONFIGURATION_RESPONSE = {
    "clique_types": CLIQUE_TYPES_WITH_SPECIFIC_CONFIGURATION
}

CLIQUE_TYPES_WITH_SPECIFIC_FOCAL_POINT_TYPE = [
    get_payload(update={'id': _id,
                        'focal_point_type': CORRECT_FOCAL_POINT_POINT_TYPE})
    for _id in SAMPLE_IDS
]

CLIQUE_TYPES_WITH_SPECIFIC_FOCAL_POINT_TYPE_RESPONSE = {
    "clique_types": CLIQUE_TYPES_WITH_SPECIFIC_FOCAL_POINT_TYPE
}

CLIQUE_TYPES_WITH_SPECIFIC_LINK_TYPE = [
    get_payload(update={'id': _id,
                        'link_types': [CORRECT_LINK_TYPE]})
    for _id in SAMPLE_IDS
]

CLIQUE_TYPES_WITH_SPECIFIC_LINK_TYPE_RESPONSE = {
    "clique_types": CLIQUE_TYPES_WITH_SPECIFIC_LINK_TYPE
}

CLIQUE_TYPES = [
    get_payload(update={'id': _id}) for _id in SAMPLE_IDS
]

CLIQUE_TYPES_RESPONSE = {
    "clique_types": CLIQUE_TYPES
}

NON_DICT_CLIQUE_TYPE = base.NON_DICT_OBJ

CLIQUE_TYPE_WITH_RESERVED_NAME = get_payload(
    update={'environment': RESERVED_ENV_NAME}
)

CLIQUE_TYPE_WITHOUT_ENV_NAME_AND_CONF = get_payload(
    delete=['environment']
)

CLIQUE_TYPE_WITH_BOTH_ENV_AND_CONF = get_payload(
    update=TEST_CONFIGURATION
)

CLIQUE_TYPE_WITH_INSUFFICIENT_CONF = get_payload(
    update={'distribution_version': CORRECT_DIST_VER}
)

CLIQUE_TYPE_WITH_UNKNOWN_ENVIRONMENT = get_payload(
    update={'environment': base.UNKNOWN_ENV}
)

CLIQUE_TYPE_WITHOUT_FOCAL_POINT_TYPE = get_payload(delete=['focal_point_type'])

CLIQUE_TYPE_WITH_WRONG_FOCAL_POINT_TYPE = get_payload(
    update={'focal_point_type': WRONG_FOCAL_POINT_TYPE}
)

CLIQUE_TYPE_WITHOUT_LINK_TYPES = get_payload(delete=['link_types'])

CLIQUE_TYPE_WITH_NON_LIST_LINK_TYPES = get_payload(
    update={'link_types': "instance-vnic"}
)

CLIQUE_TYPE_WITH_WRONG_LINK_TYPE = get_payload(
    update={'link_types': [WRONG_LINK_TYPE, "vnic-vconnector"]}
)

CLIQUE_TYPE_WITHOUT_NAME = get_payload(delete=['name'])

CLIQUE_TYPE_WITH_WRONG_MECH_DRIVERS = get_payload(
    update={'mechanism_drivers': WRONG_MECHANISM_DRIVER}
)

CLIQUE_TYPE_WITH_WRONG_TYPE_DRIVERS = get_payload(
    update={'type_drivers': WRONG_TYPE_DRIVER}
)