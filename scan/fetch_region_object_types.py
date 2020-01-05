###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.fetcher import Fetcher


class FetchRegionObjectTypes(Fetcher):

    def get(self, parent):
        ret = {
            "id": "",
            "parent": parent,
            "rows": [
                {
                    "id": "aggregates_root",
                    "type": "aggregates_folder",
                    "text": "Aggregates"
                },
                {
                    "id": "availability_zones_root",
                    "type": "availability_zones_folder",
                    "text": "Availability Zones"
                },
                {
                    "id": "network_agents_root",
                    "type": "network_agents_folder",
                    "text": "network Agents"
                }
            ]
        }
        return ret
