###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
# HTTP status code
SUCCESSFUL_CODE = "200"
NOT_FOUND_CODE = "404"
CONFLICT_CODE = "409"
BAD_REQUEST_CODE = "400"
UNAUTHORIZED_CODE = "401"
CREATED_CODE = "201"

ENV_NAME = "Mirantis-Liberty-API"
UNKNOWN_ENV = "Unkown-Environment"
NON_INT_PAGE = 1.4
INT_PAGE = 1
NON_INT_PAGESIZE = 2.4
INT_PAGESIZE = 2

WRONG_LINK_TYPE = "instance-host"
CORRECT_LINK_TYPE= "instance-vnic"

WRONG_LINK_STATE = "wrong"
CORRECT_LINK_STATE = "up"

WRONG_SCAN_STATUS = "error"
CORRECT_SCAN_STATUS = "completed"

WRONG_MONITORING_SIDE = "wrong-side"
CORRECT_MONITORING_SIDE = "client"

WRONG_MESSAGE_SEVERITY = "wrong-severity"
CORRECT_MESSAGE_SEVERITY = "warn"

WRONG_TYPE_DRIVER = "wrong_type"
CORRECT_TYPE_DRIVER = "local"

WRONG_MECHANISM_DRIVER = "wrong-mechanism-dirver"
CORRECT_MECHANISM_DRIVER = "ovs"

WRONG_LOG_LEVEL = "wrong-log-level"
CORRECT_LOG_LEVEL = "critical"

WRONG_OBJECT_TYPE = "wrong-object-type"
CORRECT_OBJECT_TYPE = "vnic"

WRONG_ENV_TYPE = ""
CORRECT_ENV_TYPE = "development"

WRONG_DISTRIBUTION = "wrong-environment"
WRONG_DIST_VER = "wrong-environment"
CORRECT_DISTRIBUTION = "Mirantis"
CORRECT_DIST_VER = "6.0"

WRONG_OBJECT_ID = "58a2406e6a283a8bee15d43"
CORRECT_OBJECT_ID = "58a2406e6a283a8bee15d43f"

WRONG_FORMAT_TIME = "2017-01-25T23:34:333+TX0012"
CORRECT_FORMAT_TIME = "2017-01-25T14:28:32.400Z"

NON_BOOL = "falses"
BOOL = False
NON_DICT_OBJ = ""

# fake constants
CONSTANTS_BY_NAMES = {
    "link_types": [
        "instance-vnic",
        "otep-vconnector",
        "otep-host_pnic",
        "host_pnic-network",
        "vedge-otep",
        "vnic-vconnector",
        "vconnector-host_pnic",
        "vconnector-vedge",
        "vnic-vedge",
        "vedge-host_pnic",
        "vservice-vnic"
    ],
    "link_states": [
        "up",
        "down"
    ],
    "scan_statuses": [
        "draft",
        "pending",
        "running",
        "completed",
        "completed_with_errors",
        "failed",
        "aborted"
    ],
    "monitoring_sides": [
        "client",
        "server"
    ],
    "messages_severity": [
        "panic",
        "alert",
        "crit",
        "error",
        "warn",
        "notice",
        "info",
        "debug"
    ],
    "type_drivers": [
        "local",
        "vlan",
        "vxlan",
        "gre",
        "flat"
    ],
    "mechanism_drivers": [
        "ovs",
        "vpp",
        "LinuxBridge",
        "Arista",
        "Nexus"
    ],
    "log_levels": [
        "critical",
        "error",
        "warning",
        "info",
        "debug",
        "notset"
    ],
    "object_types": [
        "vnic",
        "vconnector",
        "vedge",
        "instance",
        "vservice",
        "host_pnic",
        "network",
        "port",
        "otep",
        "agent",
        "switch_pnic",
        "switch"
    ],
    "env_types": [
        "development",
        "testing",
        "staging",
        "production"
    ],
    "distributions": [
        "Mirantis",
        "RDO"
    ],
    "environment_operational_status": [
        "stopped",
        "running",
        "error"
    ],
    "environment_provision_types": [
        "None",
        "Deploy",
        "Files",
        "DB"
    ],
    "environment_monitoring_types": [
       "Sensu"
    ]
}

# path info
RESPONDER_BASE_PATH = "api.responders.responder_base.ResponderBase"
RESPONDER_BASE_GET_OBJECTS_LIST = RESPONDER_BASE_PATH + ".get_objects_list"
RESPONDER_BASE_GET_OBJECT_BY_ID = RESPONDER_BASE_PATH + ".get_object_by_id"
RESPONDER_BASE_CHECK_ENVIRONMENT_NAME = RESPONDER_BASE_PATH + ".check_environment_name"
RESPONDER_BASE_READ = RESPONDER_BASE_PATH + ".read"
RESPONDER_BASE_WRITE = RESPONDER_BASE_PATH + ".write"
RESPONDER_BASE_AGGREGATE = RESPONDER_BASE_PATH + ".aggregate"
