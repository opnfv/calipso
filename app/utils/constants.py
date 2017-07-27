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


class ScanStatus(StringEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class OperationalStatus(StringEnum):
    STOPPED = "stopped"
    RUNNING = "running"
    ERROR = "error"


class EnvironmentFeatures(StringEnum):
    SCANNING = "scanning"
    MONITORING = "monitoring"
    LISTENING = "listening"
