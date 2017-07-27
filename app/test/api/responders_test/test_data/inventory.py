###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
URL = "/inventory"

ID = "RegionOne-aggregates"
NONEXISTENT_ID = "Unkown-Id"


OBJECTS_LIST = [
    {
        "id": "Mirantis-Liberty-regions",
        "name": "Regions",
        "name_path": "/Mirantis-Liberty-API/Regions"
    },
    {
        "id": "Mirantis-Liberty-projects",
        "name": "Projects",
        "name_path": "/Mirantis-Liberty-API/Projects"
    }
]

OBJECT_IDS_RESPONSE = {
    "objects": OBJECTS_LIST
}


OBJECTS = [{
  "environment": "Mirantis-Liberty-API",
  "id": "RegionOne-aggregates"
}]
