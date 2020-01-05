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
from base.utils.inventory_mgr import InventoryMgr


class KubeFetchPodAggregates(Fetcher):

    AGGREGATE_ID_PREFIX = 'pod-aggregate-'

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def get(self, aggregate_id):
        aggregate = self.inv.get_by_id(self.env, aggregate_id)
        namespace = self.inv.get_by_id(self.env, aggregate['parent_id'])
        return [{
            'id': '{}{}'.format(self.AGGREGATE_ID_PREFIX, namespace['name']),
        }]
