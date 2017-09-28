###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import MagicMock, patch

from discover.events.event_router_update import EventRouterUpdate
from test.event_based_scan.test_data.event_payload_router_update import EVENT_PAYLOAD_ROUTER_UPDATE, ROUTER_DOCUMENT, \
    EVENT_PAYLOAD_ROUTER_SET_GATEWAY, EVENT_PAYLOAD_ROUTER_DEL_GATEWAY, ROUTER_VSERVICE, PORT, NETWORK_DOC, HOST_DOC
from test.event_based_scan.test_event import TestEvent
from utils.util import encode_router_id


class TestRouterUpdate(TestEvent):

    def get_by_id(self, env, object_id):
        if object_id == self.router_id:
            return ROUTER_DOCUMENT
        elif object_id == self.gw_port_id:
            return PORT
        elif object_id == self.host_id:
            return HOST_DOC
        else:
            return None

    @patch("discover.events.event_router_update.Scanner")
    def _do_test(self,
                 values,
                 scanner_class_mock):
        self.values = values
        self.payload = self.values['payload']
        self.router = self.payload['router']
        self.host_id = self.values['publisher_id'].replace("network.", "", 1)
        self.router_id = encode_router_id(self.router['id'])
        self.gw_port_id = ROUTER_DOCUMENT['gw_port_id']

        scanner_mock = scanner_class_mock.return_value

        self.inv.get_by_id.side_effect = self.get_by_id

        res = EventRouterUpdate().handle(self.env, self.values)

        self.assertTrue(res.result)
        self.assertTrue(scanner_mock.scan_cliques.called)

    @patch("discover.events.event_router_update.EventPortDelete")
    def test_handle_router_update(self,
                                  event_port_delete_class_mock):
        event_port_delete_mock = event_port_delete_class_mock.return_value
        self._do_test(EVENT_PAYLOAD_ROUTER_UPDATE)
        event_port_delete_mock.delete_port\
            .assert_called_with(self.env, self.gw_port_id)

    @patch("discover.events.event_router_update.FindLinksForVserviceVnics")
    @patch("discover.events.event_router_update.EventRouterAdd")
    @patch("discover.events.event_router_update.CliFetchHostVservice")
    def test_handle_router_set_gateway(self,
                                       cli_fetch_vservice_class_mock,
                                       event_router_add_class_mock,
                                       find_links_class_mock):
        cli_fetch_vservice_mock = cli_fetch_vservice_class_mock.return_value
        cli_fetch_vservice_mock.get_vservice.return_value = ROUTER_VSERVICE
        event_router_add_mock = event_router_add_class_mock.return_value
        find_links_mock = find_links_class_mock.return_value
        self._do_test(EVENT_PAYLOAD_ROUTER_SET_GATEWAY)
        cli_fetch_vservice_mock.get_vservice.assert_called_with(self.host_id,
                                                                self.router_id)
        self.assertTrue(event_router_add_mock.add_children_documents.called)
        self.assertTrue(find_links_mock.add_links.called)

    @patch("discover.events.event_router_update.EventPortDelete")
    def test_handle_router_delete_gateway(self,
                                          event_port_delete_class_mock):
        event_port_delete_mock = event_port_delete_class_mock.return_value
        self._do_test(EVENT_PAYLOAD_ROUTER_DEL_GATEWAY)
        event_port_delete_mock.delete_port \
            .assert_called_with(self.env, self.gw_port_id)

