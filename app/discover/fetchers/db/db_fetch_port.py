###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.db.db_access import DbAccess
from utils.inventory_mgr import InventoryMgr


class DbFetchPort(DbAccess):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()
        self.env_config = self.config.get_env_config()

    def get(self, id=None):
        query = """SELECT * FROM {}.ports where network_id = %s""" \
            .format(self.neutron_db)
        return self.get_objects_list_for_id(query, "port", id)

    def get_id(self, id=None):
        query = """SELECT id FROM {}.ports where network_id = %s""" \
            .format(self.neutron_db)
        result = self.get_objects_list_for_id(query, "port", id)
        return result[0]['id'] if result != [] else None

    def get_id_by_field(self, id, search=''):
        query = """SELECT id FROM {}.ports where network_id = %s AND {}"""\
                .format(self.neutron_db, search)
        result = self.get_objects_list_for_id(query, "port", id)
        return result[0]['id'] if result != [] else None
