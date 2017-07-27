###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import MagicMock

from discover.events.event_port_add import EventPortAdd
from discover.events.event_router_add import EventRouterAdd
from discover.events.event_subnet_add import EventSubnetAdd
from discover.fetchers.cli.cli_fetch_host_vservice import CliFetchHostVservice
from test.event_based_scan.test_data.event_payload_router_add import EVENT_PAYLOAD_ROUTER_ADD, ROUTER_DOCUMENT, \
    HOST_DOC, NETWORK_DOC
from test.event_based_scan.test_event import TestEvent
from utils.util import encode_router_id


class TestRouterAdd(TestEvent):
    def test_handle_router_add(self):
        self.values = EVENT_PAYLOAD_ROUTER_ADD
        self.payload = self.values['payload']
        self.router = self.payload['router']
        self.host_id = self.values["publisher_id"].replace("network.", "", 1)
        self.router_id = encode_router_id(self.host_id, self.router['id'])

        self.set_item(HOST_DOC)
        self.host_id = HOST_DOC['id']
        gateway_info = self.router['external_gateway_info']
        if gateway_info:
            self.network_id = self.router['external_gateway_info']['network_id']
            self.inv.set(NETWORK_DOC)

        original_get_vservice = CliFetchHostVservice.get_vservice
        CliFetchHostVservice.get_vservice = MagicMock(return_value=ROUTER_DOCUMENT)
        self.gw_port_id = ROUTER_DOCUMENT['gw_port_id']

        original_add_port = EventSubnetAdd.add_port_document
        EventSubnetAdd.add_port_document = MagicMock()

        original_add_vnic = EventPortAdd.add_vnic_document
        EventPortAdd.add_vnic_document = MagicMock()

        handler = EventRouterAdd()
        handler.update_links_and_cliques = MagicMock()

        handler.handle(self.env, self.values)

        # reset the methods back
        CliFetchHostVservice.get_vservice = original_get_vservice
        EventSubnetAdd.add_port_document = original_add_port
        EventPortAdd.add_vnic_document = original_add_vnic

        # assert router document
        router_doc = self.inv.get_by_id(self.env, self.router_id)
        self.assertIsNotNone(router_doc, msg="router_doc not found.")
        self.assertEqual(ROUTER_DOCUMENT['name'], router_doc['name'])
        self.assertEqual(ROUTER_DOCUMENT['gw_port_id'], router_doc['gw_port_id'])

        # assert children documents
        vnics_id = '-'.join(['qrouter', self.router['id'], 'vnics'])
        vnics_folder = self.inv.get_by_id(self.env, vnics_id)
        self.assertIsNotNone(vnics_folder, msg="Vnics folder not found.")

    def tearDown(self):
        self.item_ids = [self.network_id, self.host_id, self.network_id+"-ports", self.gw_port_id,
                         self.router_id+'-vnics', self.router_id]
        for item_id in self.item_ids:
            self.inv.delete('inventory', {'id': item_id})
            item = self.inv.get_by_id(self.env, item_id)
            self.assertIsNone(item)

        # delete vnics document
        self.inv.delete('inventory', {'parent_id': self.router_id+'-vnics'})
        item = self.inv.get_by_field(self.env, 'vnic', 'parent_id', self.router_id+'-vnics', get_single=True)
        self.assertIsNone(item)
