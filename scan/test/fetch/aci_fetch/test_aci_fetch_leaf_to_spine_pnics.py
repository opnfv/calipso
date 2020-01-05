###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import patch

from copy import deepcopy

from scan.fetchers.aci.aci_fetch_leaf_to_spine_pnics import \
    AciFetchLeafToSpinePnics
from scan.test.fetch.aci_fetch.aci_test_base import AciTestBase
from scan.test.fetch.aci_fetch.test_data.aci_access import ACI_CONFIG, \
    LOGIN_RESPONSE, EMPTY_RESPONSE
from scan.test.fetch.aci_fetch.test_data.aci_fetch_leaf_to_spine_pnics import \
    HOSTLINK_PNIC, SPINES_RESPONSE, ADJACENT_SPINES_RESPONSE
from scan.test.fetch.aci_fetch.test_data.aci_fetch_switch_pnic import \
    L1PHYSIF_RESPONSE


class TestAciFetchLeafToSpinePnics(AciTestBase):

    RESPONSES = {
        'aaaRefresh.json': LOGIN_RESPONSE,
        'fabricNode.json': SPINES_RESPONSE,
        'sys.json': ADJACENT_SPINES_RESPONSE,
        'phys-\[.*\].json': L1PHYSIF_RESPONSE
    }

    def setUp(self):
        super().setUp()

        self.inv_patcher = patch(
            'discover.fetchers.aci.aci_fetch_leaf_to_spine_pnics.InventoryMgr'
        )
        self.inv_class = self.inv_patcher.start()
        self.inv = self.inv_class.return_value

        self.fetcher = AciFetchLeafToSpinePnics(config=ACI_CONFIG)

    @staticmethod
    def _get_by_id(environment, item_id):
        if item_id == HOSTLINK_PNIC['id']:
            return HOSTLINK_PNIC
        else:
            return None

    def test_get(self):
        self.inv.get_by_id.side_effect = self._get_by_id

        self.requests.get.side_effect = self._requests_get
        pnics = self.fetcher.get(HOSTLINK_PNIC['id'])

        self.assertEqual(2, len(pnics))

    def test_get_no_spines(self):
        self.inv.get_by_id.side_effect = self._get_by_id

        self.requests.get.side_effect = self._requests_get

        old_responses = deepcopy(self.RESPONSES)
        self.RESPONSES['sys.json'] = EMPTY_RESPONSE
        pnics = self.fetcher.get(HOSTLINK_PNIC['id'])
        self.RESPONSES = old_responses

        self.assertEqual(0, len(pnics))

    def tearDown(self):
        self.aci_access.reset_token()
        self.inv_patcher.stop()
        super().tearDown()