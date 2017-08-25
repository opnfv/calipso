###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import copy

from discover.fetchers.api.api_access import ApiAccess


class TestRegions:
    def __init__(self, test_regions):
        super().__init__()
        self.original_regions = copy.deepcopy(ApiAccess.regions)
        self.test_regions = test_regions

    def __enter__(self):
        ApiAccess.regions = self.test_regions

    def __exit__(self, exc_type, exc_val, exc_tb):
        ApiAccess.regions = self.original_regions