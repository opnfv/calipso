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

from discover.events.event_router_update import EventRouterUpdate
from discover.fetchers.api.api_fetch_port import ApiFetchPort
from discover.fetchers.cli.cli_fetch_host_vservice import CliFetchHostVservice
from test.event_based_scan.test_data.event_payload_router_update import EVENT_PAYLOAD_ROUTER_UPDATE, ROUTER_DOCUMENT, \
    EVENT_PAYLOAD_ROUTER_SET_GATEWAY, EVENT_PAYLOAD_ROUTER_DEL_GATEWAY, ROUTER_VSERVICE, PORTS, NETWORK_DOC, HOST_DOC
from test.event_based_scan.test_event import TestEvent
from utils.util import encode_router_id


class TestRouterUpdate(TestEvent):
    def test_handle_router_update(self):
        for values in [EVENT_PAYLOAD_ROUTER_UPDATE, EVENT_PAYLOAD_ROUTER_SET_GATEWAY, EVENT_PAYLOAD_ROUTER_DEL_GATEWAY]:
            self.values = values
            self.payload = self.values['payload']
            self.router = self.payload['router']
            host_id = self.values['publisher_id'].replace("network.", "", 1)
            self.router_id = encode_router_id(host_id, self.router['id'])
            self.item_ids.append(self.router_id)

            # add document for testing
            self.set_item(ROUTER_DOCUMENT)
            self.set_item(PORTS)
            self.set_item(NETWORK_DOC)
            self.set_item(HOST_DOC)

            # mock the router document.
            original_get_vservice = CliFetchHostVservice.get_vservice
            CliFetchHostVservice.get_vservice = MagicMock(return_value=ROUTER_VSERVICE)
            self.gw_port_id = ROUTER_DOCUMENT['gw_port_id']

            # mock
            original_get_port = ApiFetchPort.get
            ApiFetchPort.get = MagicMock(return_value=[PORTS])

            handler = EventRouterUpdate()
            handler.handle(self.env, self.values)

            # reset the methods back
            CliFetchHostVservice.get_vservice = original_get_vservice
            ApiFetchPort.get = original_get_port
            # assert router document
            router_doc = self.inv.get_by_id(self.env, self.router_id)
            self.assertIsNotNone(router_doc, msg="router_doc not found.")
            self.assertEqual(self.router['name'], router_doc['name'])
            self.assertEqual(self.router['admin_state_up'], router_doc['admin_state_up'])

            if self.router['external_gateway_info'] is None:
                self.assertEqual(router_doc['gw_port_id'], None)
                self.assertEqual(router_doc['network'], [])
            else:
                self.assertIn(self.router['external_gateway_info']['network_id'], router_doc['network'])
