###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from bson.objectid import ObjectId


AGGREGATE = {
    "id": "1",
}

HOSTS = [
    {
        "id": "aggregate-osdna-agg-node-5.cisco.com",
        "name": "node-5.cisco.com"
    }
]

HOST_IN_INVENTORY = {
    "_id": "595ac4b6d7c037efdb8918a7"
}

HOSTS_RESULT = [
    {
        "id": "aggregate-osdna-agg-node-5.cisco.com",
        "name": "node-5.cisco.com",
        "ref_id": ObjectId(HOST_IN_INVENTORY["_id"])
    }
]
