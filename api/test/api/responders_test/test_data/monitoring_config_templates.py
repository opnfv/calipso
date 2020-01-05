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


URL = "/monitoring_config_templates"

WRONG_ID = base.WRONG_OBJECT_ID
UNKNOWN_ID = "583711893e149c14785d6da5"
CORRECT_ID = base.CORRECT_OBJECT_ID

NON_INT_ORDER = 1.3
INT_ORDER = 1

WRONG_SIDE = base.WRONG_MONITORING_SIDE
CORRECT_SIDE = base.CORRECT_MONITORING_SIDE

TYPE = "client.json"

TEMPLATES_WITH_SPECIFIC_ORDER = [
    {
      "order": INT_ORDER,
      "id": "583711893e149c14785d6daa"
    },
    {
      "order": INT_ORDER,
      "id": "583711893e149c14785d6da7"
    }
]

TEMPLATES_WITH_SPECIFIC_ORDER_RESPONSE = {
    "monitoring_config_templates":
        TEMPLATES_WITH_SPECIFIC_ORDER
}

TEMPLATES_WITH_SPECIFIC_SIDE = [
    {
      "side": CORRECT_SIDE,
      "id": "583711893e149c14785d6daa"
    },
    {
      "side": CORRECT_SIDE,
      "id": "583711893e149c14785d6da7"
    }
]

TEMPLATES_WITH_SPECIFIC_SIDE_RESPONSE = {
    "monitoring_config_templates":
        TEMPLATES_WITH_SPECIFIC_SIDE
}

TEMPLATES_WITH_SPECIFIC_TYPE = [
    {
      "type": TYPE,
      "id": "583711893e149c14785d6daa"
    },
    {
      "type": TYPE,
      "id": "583711893e149c14785d6da7"
    }
]

TEMPLATES_WITH_SPECIFIC_TYPE_RESPONSE = {
    "monitoring_config_templates":
        TEMPLATES_WITH_SPECIFIC_TYPE
}

TEMPLATES_WITH_SPECIFIC_ID = [
    {
      "type": "rabbitmq.json",
      "side": "client",
      "id": CORRECT_ID
    }
]

TEMPLATES = [
    {
      "type": "rabbitmq.json",
      "side": "client",
      "id": "583711893e149c14785d6daa"
    },
    {
      "type": "rabbitmq.json",
      "side": "client",
      "id": "583711893e149c14785d6da7"
    }
]

TEMPLATES_RESPONSE = {
    "monitoring_config_templates": TEMPLATES
}
