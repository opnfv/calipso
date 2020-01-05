###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json

from base.utils.inventory_mgr import InventoryMgr
from scan.fetchers.db.db_access import DbAccess


class DbFetchHostNetworkAgents(DbAccess):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()
        self.env_config = self.config.get_env_config()

    def get(self, id):
        query = """
          SELECT * FROM {}.agents
          WHERE host = %s
        """.format(self.neutron_db)
        host_id = id[:-1 * len("-network_agents")]
        results = self.get_objects_list_for_id(query, "network_agent", host_id)
        for o in results:
            o["configurations"] = json.loads(o["configurations"])
            o["name"] = o["binary"]
            o['id'] = "{}-{}".format(o['name'], o['id'])
            if o.get('admin_state_up') in (0, 1):
                o['admin_state_up'] = bool(o['admin_state_up'])
        return results
