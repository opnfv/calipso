###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from enum import Enum


class StringEnum(Enum):
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)


class ConnectionTestType(StringEnum):
    AMQP = "AMQP"
    CLI = "CLI"
    ACI = "ACI"
    MYSQL = "mysql"
    OPENSTACK = "OpenStack"
    MONITORING = "Monitoring"


class ConnectionTestStatus(StringEnum):
    REQUEST = "request"
    RESPONSE = "response"


class ScanStatus(StringEnum):
    DRAFT = "draft"
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
    FAILED = "failed"
    ABORTED = "aborted"


class OperationalStatus(StringEnum):
    STOPPED = "stopped"
    RUNNING = "running"
    ERROR = "error"


class EnvironmentFeatures(StringEnum):
    SCANNING = "scanning"
    MONITORING = "monitoring"
    LISTENING = "listening"
