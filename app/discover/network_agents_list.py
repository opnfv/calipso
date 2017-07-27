###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from utils.mongo_access import MongoAccess


class NetworkAgentsList(MongoAccess):
    def __init__(self):
        super(NetworkAgentsList, self).__init__()
        self.list = MongoAccess.db["network_agent_types"]

    def get_type(self, type):
        matches = self.list.find({"type": type})
        for doc in matches:
            doc["_id"] = str(doc["_id"])
            return doc
        return {}
