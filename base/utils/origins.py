###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from enum import Enum


class Origins(Enum):
    pass


class ScanOrigins(Origins):
    MANUAL = 'manual scan'
    SCHEDULED = 'scheduled scan'
    EVENT = 'event based scan'
    TEST = 'test'
    UNKNOWN = 'unknown'


class Origin:
    def __init__(self, origin_id=None,
                 origin_type: Origins = None):
        self.origin_id = origin_id
        self.origin_type = origin_type
        # Names of extra fields for mongo logging handler
        self.extra = []


class ScanOrigin(Origin):
    def __init__(self, origin_id=None,
                 origin_type: ScanOrigins = ScanOrigins.UNKNOWN):
        super().__init__(origin_id=origin_id,
                         origin_type=origin_type)
