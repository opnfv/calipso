###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
URL = "/aggregates"

CONSTANT_TYPE = "constant"
ENV_TYPE = "environment"
MESSAGE_TYPE = "message"
UNKNOWN_TYPE = "unknown"

CONSTANT_AGGREGATES = [
    {"name": "type_drivers", "total": 5},
    {"name": "environment_monitoring_types", "total": 1},
    {"name": "link_states", "total": 2}
]
ENVIRONMENT_AGGREGATES = [
    {'_id': 'otep', 'total': 3},
    {'_id': 'instance', 'total': 2},
    {'_id': 'network_agent', 'total': 6}
]
MESSAGE_ENV_AGGREGATES = [
    {'_id': 'Mirantis-Liberty-API', 'total': 15}
]
MESSAGE_LEVEL_AGGREGATES = [
    {'_id': 'info', 'total': 15}
]

CONSTANT_AGGREGATES_RESPONSE = {
            "type": "constant",
            "aggregates": {
                "names": {
                    "type_drivers": 5,
                    "environment_monitoring_types": 1,
                    "link_states": 2
                }
            }
        }

ENVIRONMENT_AGGREGATES_RESPONSE = {
    "aggregates": {
        "object_types": {
            "otep": 3,
            "instance": 2,
            "network_agent": 6
        }
    },
    "env_name": "Mirantis-Liberty-API",
    "type": "environment"
}

MESSAGE_AGGREGATES_RESPONSE = {
           "aggregates": {
                "environments": {
                    "Mirantis-Liberty-API": 15
                },
                "levels": {
                    "info": 15
                }
           },
           "type": "message"
        }
