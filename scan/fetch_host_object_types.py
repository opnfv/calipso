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


class FetchHostObjectTypes(Fetcher):

    def get(self, parent):
        ret = {
            "id": "",
            "parent": parent,
            "rows": [
                {
                    "id": "instances_root",
                    "type": "instances_folder",
                    "text": "Instances"
                },
                {
                    "id": "networks_root",
                    "type": "networks_folder",
                    "text": "Networks"
                },
                {
                    "id": "vservices_root",
                    "type": "vservices_folder",
                    "text": "vServices"
                }
            ]
        }
        return ret
