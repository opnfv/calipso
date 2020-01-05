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

from scan.fetchers.aci.aci_fetch_switch_pnic import AciFetchSwitchPnic
from scan.test.fetch.aci_fetch.aci_test_base import AciTestBase
from scan.test.fetch.aci_fetch.test_data.aci_access import ACI_CONFIG, \
    LOGIN_RESPONSE, EMPTY_RESPONSE
from scan.test.fetch.aci_fetch.test_data.aci_fetch_switch_pnic import HOST_PNIC, \
    SWITCH_PNIC_RESPONSE, SWITCH_RESPONSE, FVCEP_RESPONSE, L1PHYSIF_RESPONSE
from scan.test.fetch.logger_patcher import LoggerPatcher


class TestAciFetchSwitchPnic(AciTestBase, LoggerPatcher):

    RESPONSES = {
        'aaaRefresh.json': LOGIN_RESPONSE,
        'epmMacEp.json': SWITCH_PNIC_RESPONSE,
        'sys.json': SWITCH_RESPONSE,
        'fvCEp.json': FVCEP_RESPONSE,
        'phys-\[.*\].json': L1PHYSIF_RESPONSE
    }

    def setUp(self):
        super().setUp()

        self.inv_patcher = patch(
            'discover.fetchers.aci.aci_fetch_switch_pnic.InventoryMgr'
        )
        self.inv_class = self.inv_patcher.start()
        self.inv = self.inv_class.return_value

        self.fetcher = AciFetchSwitchPnic(config=ACI_CONFIG)

    def _get_by_id(self, environment, item_id):
        if item_id == HOST_PNIC['id']:
            return HOST_PNIC
        else:
            return None

    def test_get(self):
        self.inv.get_by_id.side_effect = self._get_by_id

        self.requests.get.side_effect = self._requests_get
        pnics = self.fetcher.get(HOST_PNIC['id'])

        self.assertEqual(1, len(pnics))

    def test_get_no_pnic(self):
        self.inv.get_by_id.return_value = None
        pnics = self.fetcher.get(HOST_PNIC['id'])

        self.assertEqual(0, len(pnics))

    def test_get_no_mac_address(self):
        host_pnic = HOST_PNIC
        del host_pnic['mac_address']
        self.inv.get_by_id.return_value = HOST_PNIC
        pnics = self.fetcher.get(HOST_PNIC['id'])

        self.assertEqual(0, len(pnics))

    def test_get_no_switch_pnic(self):
        old_responses = deepcopy(self.RESPONSES)
        self.RESPONSES['epmMacEp.json'] = EMPTY_RESPONSE

        self.requests.get.side_effect = self._requests_get
        pnics = self.fetcher.get(HOST_PNIC['id'])
        self.RESPONSES = old_responses

        self.assertEqual(0, len(pnics))

    def test_get_no_switch(self):
        old_responses = deepcopy(self.RESPONSES)
        self.RESPONSES['sys.json'] = EMPTY_RESPONSE

        self.requests.get.side_effect = self._requests_get
        pnics = self.fetcher.get(HOST_PNIC['id'])
        self.RESPONSES = old_responses

        self.assertEqual(0, len(pnics))

    def tearDown(self):
        self.aci_access.reset_token()
        self.inv_patcher.stop()
        super().tearDown()
