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

URL = "/scheduled_scans"
WRONG_FREQ = "wrong_freq"
CORRECT_FREQ = "WEEKLY"
WRONG_ID = base.WRONG_OBJECT_ID
NONEXISTENT_ID = "58c96a075eb66a121cc4e750"
CORRECT_ID = "ff4d3e80e42e886bef13a084"
NON_DICT_SCHEDULED_SCAN = ""


SCHEDULED_SCANS = [
    {
        "id": "ff4d3e80e42e886bef13a084",
        "environment": base.ENV_NAME,
        "scheduled_timestamp": "2017-07-24T12:45:03.784+0000",
        "freq": "WEEKLY"
    },
    {
        "id": "58e4e1aa6df71e971324ea62",
        "environment": base.ENV_NAME,
        "scheduled_timestamp": "2017-07-24T12:45:03.784+0000",
        "freq": "WEEKLY"
    }
]

SCHEDULED_SCANS_RESPONSE = {
    "scheduled_scans": SCHEDULED_SCANS
}

SCHEDULED_SCAN_WITH_SPECIFIC_FREQ = [{
    "id": "ff4d3e80e42e886bef13a084",
    "environment": base.ENV_NAME,
    "scheduled_timestamp": "2017-07-24T12:45:03.784+0000",
    "freq": CORRECT_FREQ
}]

SCHEDULED_SCAN_WITH_SPECIFIC_FREQ_RESPONSE = {
    "scheduled_scans": SCHEDULED_SCAN_WITH_SPECIFIC_FREQ
}

SCHEDULED_SCAN_WITH_SPECIFIC_ID = [{
    "id": CORRECT_ID,
    "environment": base.ENV_NAME,
    "scheduled_timestamp": "2017-07-24T12:45:03.784+0000",
    "freq": CORRECT_FREQ
}]

SCHEDULED_SCAN = {
    "environment": base.ENV_NAME,
    "freq": CORRECT_FREQ,
    "submit_timestamp": "2017-07-24T12:45:03.784+0000"
}

SCHEDULED_SCAN_WITHOUT_ENV = {
    "freq": CORRECT_FREQ,
    "submit_timestamp": "2017-07-24T12:45:03.784+0000"
}

SCHEDULED_SCAN_WITH_UNKNOWN_ENV = {
    "environment": base.UNKNOWN_ENV,
    "freq": CORRECT_FREQ,
    "submit_timestamp": "2017-07-24T12:45:03.784+0000"
}

SCHEDULED_SCAN_WITHOUT_FREQ = {
    "environment": base.ENV_NAME,
    "submit_timestamp": "2017-07-24T12:45:03.784+0000"
}

SCHEDULED_SCAN_WITHOUT_SUBMIT_TIMESTAMP = {
    "environment": base.ENV_NAME,
    "freq": CORRECT_FREQ,
}

SCHEDULED_SCAN_WITH_WRONG_FREQ = {
    "environment": base.ENV_NAME,
    "freq": WRONG_FREQ,
    "submit_timestamp": "2017-07-24T12:45:03.784+0000"
}

SCHEDULED_SCAN_WITH_WRONG_LOG_LEVEL = {
    "environment": base.ENV_NAME,
    "freq": CORRECT_FREQ,
    "log_level": base.WRONG_LOG_LEVEL,
    "submit_timestamp": "2017-07-24T12:45:03.784+0000"
}

SCHEDULED_SCAN_WITH_WRONG_SUBMIT_TIMESTAMP = {
    "environment": base.ENV_NAME,
    "freq": CORRECT_FREQ,
    "submit_timestamp": base.WRONG_FORMAT_TIME
}

SCHEDULED_SCAN_WITH_NON_BOOL_CLEAR = {
    "environment": base.ENV_NAME,
    "freq": CORRECT_FREQ,
    "submit_timestamp": "2017-07-24T12:45:03.784+0000",
    "clear": base.NON_BOOL
}

SCHEDULED_SCAN_WITH_NON_BOOL_SCAN_ONLY_LINKS = {
    "environment": base.ENV_NAME,
    "freq": CORRECT_FREQ,
    "submit_timestamp": "2017-07-24T12:45:03.784+0000",
    "scan_only_links": base.NON_BOOL
}

SCHEDULED_SCAN_WITH_NON_BOOL_SCAN_ONLY_CLIQUES = {
    "environment": base.ENV_NAME,
    "freq": CORRECT_FREQ,
    "submit_timestamp": "2017-07-24T12:45:03.784+0000",
    "scan_only_cliques": base.NON_BOOL
}

SCHEDULED_SCAN_WITH_NON_BOOL_SCAN_ONLY_INVENTORY = {
    "environment": base.ENV_NAME,
    "freq": CORRECT_FREQ,
    "submit_timestamp": "2017-07-24T12:45:03.784+0000",
    "scan_only_inventory": base.NON_BOOL
}

SCHEDULED_SCAN_WITH_EXTRA_SCAN_ONLY_FLAGS = {
    "environment": base.ENV_NAME,
    "freq": CORRECT_FREQ,
    "submit_timestamp": "2017-07-24T12:45:03.784+0000",
    "scan_only_links": True,
    "scan_only_inventory": True
}
