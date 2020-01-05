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

from base.fetcher import Fetcher
from base.utils.inventory_mgr import InventoryMgr
from scan.fetchers.kube.kube_fetch_pod_aggregates import \
    KubeFetchPodAggregates


class KubeFetchAggregatePods(Fetcher):

    REF_SUFFIX = '-ref'

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def get(self, aggregate_id):
        id_prefix = KubeFetchPodAggregates.AGGREGATE_ID_PREFIX
        namespace = aggregate_id.split(id_prefix)[-1]

        pods = self.inv.get_by_field(environment=self.env,
                                     item_type="pod",
                                     field_name="namespace",
                                     field_value=namespace)

        return [{
            'id': "{}{}".format(pod['id'], self.REF_SUFFIX),
            'name': pod['name'],
            'ref_id': bson.ObjectId(pod['_id'])
        } for pod in pods]
