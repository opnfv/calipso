###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import bson

from base.utils.inventory_mgr import InventoryMgr
from scan.fetchers.db.db_access import DbAccess


class DbFetchAggregateHosts(DbAccess):
    def get(self, id):
        query = """
      SELECT CONCAT('aggregate-', a.name, '-', host) AS id, host AS name
      FROM nova.aggregate_hosts ah
        JOIN nova.aggregates a ON a.id = ah.aggregate_id
      WHERE ah.deleted = 0 AND aggregate_id = %s
    """
        hosts = self.get_objects_list_for_id(query, "host", id)
        if hosts:
            inv = InventoryMgr()
            for host_rec in hosts:
                host_id = host_rec['name']
                host = inv.get_by_id(self.get_env(), host_id)
                if not host:
                    self.log.error('unable to find host {} '
                                   'from aggregate {} in inventory'
                                   .format(host_id, id))
                    continue
                host_rec['ref_id'] = bson.ObjectId(host['_id'])
        return hosts
