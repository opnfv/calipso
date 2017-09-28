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

from discover.events.event_port_add import EventPortAdd
from discover.events.event_router_add import EventRouterAdd
from discover.events.event_subnet_add import EventSubnetAdd
from discover.fetchers.cli.cli_fetch_host_vservice import CliFetchHostVservice
from test.event_based_scan.test_data.event_payload_router_add import EVENT_PAYLOAD_ROUTER_ADD, ROUTER_DOCUMENT, \
    HOST_DOC, NETWORK_DOC
from test.event_based_scan.test_event import TestEvent
from utils.util import encode_router_id


class TestRouterAdd(TestEvent):

    def get_by_id(self, env, object_id):
        if object_id == self.host_id:
            return HOST_DOC
        elif object_id == self.network_id:
            return NETWORK_DOC
        else:
            return None

    @patch("discover.events.event_router_add.EventPortAdd")
    @patch("discover.events.event_router_add.EventSubnetAdd")
    @patch("discover.events.event_router_add.Scanner")
    @patch("discover.events.event_router_add.FindLinksForVserviceVnics")
    @patch("discover.events.event_router_add.CliFetchHostVservice")
    def test_handle_router_add(self,
                               cli_fetch_vservice_class_mock,
                               find_links_class_mock,
                               scanner_class_mock,
                               subnet_add_class_mock,
                               port_add_class_mock):
        self.values = EVENT_PAYLOAD_ROUTER_ADD
        self.payload = self.values['payload']
        self.router = self.payload['router']
        self.network_id = self.router['external_gateway_info']['network_id']
        self.host_id = self.values["publisher_id"].replace("network.", "", 1)
        self.router_id = encode_router_id(self.router['id'])

        self.inv.get_by_id.side_effect = self.get_by_id

        cli_fetch_vservice_mock = cli_fetch_vservice_class_mock.return_value
        cli_fetch_vservice_mock.get_vservice.return_value = ROUTER_DOCUMENT

        find_links_mock = find_links_class_mock.return_value
        scanner_mock = scanner_class_mock.return_value
        subnet_add_mock = subnet_add_class_mock.return_value
        subnet_add_mock.add_port_document.return_value = True
        port_add_mock = port_add_class_mock.return_value
        port_add_mock.add_vnic_document.return_value = True
        port_add_mock.add_vnic_folder.return_value = True

        res = EventRouterAdd().handle(self.env, self.values)

        self.assertTrue(res.result)

        # Assert that router has been added to db
        router_insertions = [call_args for call_args
                             in self.inv.set.call_args_list
                             if call_args[0][0]['type'] == 'vservice']
        self.assertTrue(router_insertions)
        self.assertTrue(subnet_add_mock.add_ports_folder.called)
        self.assertTrue(subnet_add_mock.add_port_document.called)
        self.assertTrue(port_add_mock.add_vnics_folder.called)
        self.assertTrue(port_add_mock.add_vnic_document.called)
        find_links_mock.add_links\
            .assert_called_with(search={"parent_id": self.router_id})
        self.assertTrue(scanner_mock.scan_cliques.called)

