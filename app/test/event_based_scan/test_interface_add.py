###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import copy
from unittest.mock import MagicMock, patch, Mock

from discover.events.event_base import EventResult
from discover.events.event_interface_add import EventInterfaceAdd
from test.event_based_scan.test_data.event_payload_interface_add import \
    EVENT_PAYLOAD_INTERFACE_ADD, NETWORK_DOC, \
    EVENT_PAYLOAD_REGION, PORT_DOC, ROUTER_DOCUMENT, HOST, VNIC_DOCS
from test.event_based_scan.test_event import TestEvent
from test.event_based_scan.util import TestRegions
from utils.util import encode_router_id


class TestInterfaceAdd(TestEvent):

    def get_by_id(self, env, object_id):
        interface = self.values["payload"]["router_interface"]
        host_id = self.values["publisher_id"].replace("network.", "", 1)
        router_id = encode_router_id(host_id, interface['id'])

        if object_id == host_id:
            return HOST
        elif object_id == router_id:
            return ROUTER_DOCUMENT
        elif object_id == ROUTER_DOCUMENT["gw_port_id"]:
            return PORT_DOC
        else:
            return None

    @patch("discover.events.event_interface_add.FindLinksForVserviceVnics")
    @patch("discover.events.event_interface_add.Scanner")
    @patch("discover.events.event_interface_add.CliFetchHostVservice")
    @patch("discover.events.event_interface_add.EventPortAdd")
    @patch("discover.events.event_interface_add.EventSubnetAdd")
    def test_handle_interface_add(self, subnet_add_class_mock,
                                        port_add_class_mock,
                                        fetcher_class_mock,
                                        scanner_class_mock,
                                        find_links_class_mock):
        self.values = EVENT_PAYLOAD_INTERFACE_ADD

        self.inv.get_by_field.return_value = NETWORK_DOC
        self.inv.get_by_id.side_effect = self.get_by_id

        subnet_add_mock = subnet_add_class_mock.return_value
        subnet_add_mock.add_port_document.return_value = PORT_DOC

        port_add_mock = port_add_class_mock.return_value
        port_add_mock.add_vnic_document = \
            Mock(return_value=EventResult(result=True))

        fetcher_mock = fetcher_class_mock.return_value
        fetcher_mock.get_vservice.return_value = ROUTER_DOCUMENT
        fetcher_mock.handle_service.return_value = VNIC_DOCS

        scanner_mock = scanner_class_mock.return_value
        find_links_mock = find_links_class_mock.return_value

        with patch("discover.fetcher.FullLogger"):
            with TestRegions(EVENT_PAYLOAD_REGION):
                res = EventInterfaceAdd().handle(self.env, self.values)

        self.assertTrue(res.result)
        self.inv.set.assert_called_with(ROUTER_DOCUMENT)
        self.assertTrue(port_add_mock.add_vnic_document.called)
        self.assertTrue(scanner_mock.scan_cliques.called)
        self.assertTrue(find_links_mock.add_links.called)
