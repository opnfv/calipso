###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import patch

from discover.events.event_subnet_add import EventSubnetAdd
from discover.fetchers.api.api_access import ApiAccess
from test.event_based_scan.test_data.event_payload_subnet_add import \
    EVENT_PAYLOAD_SUBNET_ADD, \
    EVENT_PAYLOAD_REGION, NETWORK_DOC, HOST_DOC, PORT_DOC
from test.event_based_scan.test_event import TestEvent


class TestSubnetAdd(TestEvent):

    def get_by_id(self, env, object_id):
        if object_id == self.network_id:
            return NETWORK_DOC
        elif object_id == self.host_id:
            return HOST_DOC
        else:
            return None

    def get_port_id(self, network_id):
        return self.port_id if network_id == self.network_id else None

    def get_port_docs(self, port_id):
        return [PORT_DOC] if port_id == self.port_id else []

    @patch("discover.events.event_subnet_add.Scanner")
    @patch("discover.events.event_subnet_add.FindLinksForVserviceVnics")
    @patch("discover.events.event_subnet_add.FindLinksForPnics")
    @patch("discover.events.event_subnet_add.EventPortAdd")
    @patch("discover.events.event_subnet_add.DbFetchPort")
    @patch("discover.events.event_subnet_add.ApiFetchPort")
    def test_handle_subnet_add(self,
                               api_fetch_port_class_mock,
                               db_fetch_port_class_mock,
                               event_port_add_class_mock,
                               find_links_for_pnics_class_mock,
                               find_links_for_vnics_class_mock,
                               scanner_class_mock):
        self.values = EVENT_PAYLOAD_SUBNET_ADD
        self.payload = self.values['payload']
        self.subnet = self.payload['subnet']
        self.subnet_id = self.subnet['id']
        self.network_id = self.subnet['network_id']
        self.host_id = self.values["publisher_id"].replace("network.", "", 1)
        self.port_id = PORT_DOC['id']

        db_fetch_port_mock = db_fetch_port_class_mock.return_value
        db_fetch_port_mock.get_id.side_effect = self.get_port_id

        api_fetch_port_mock = api_fetch_port_class_mock.return_value
        api_fetch_port_mock.get.side_effect = self.get_port_docs

        event_port_add_mock = event_port_add_class_mock.return_value
        find_links_for_pnics_mock = find_links_for_pnics_class_mock.return_value
        find_links_for_vnics_mock = find_links_for_vnics_class_mock.return_value
        scanner_mock = scanner_class_mock.return_value

        self.inv.get_by_id.side_effect = self.get_by_id

        if not ApiAccess.regions:
            ApiAccess.regions = EVENT_PAYLOAD_REGION

        res = EventSubnetAdd().handle(self.env, self.values)

        if ApiAccess.regions == EVENT_PAYLOAD_REGION:
            ApiAccess.regions = None

        self.assertTrue(res.result)

        # Assert that subnet has been added to network
        set_call = [call[0][0] for call in self.inv.set.call_args_list
                    if self.payload['subnet']['id']
                    in call[0][0].get('subnet_ids', [])]
        self.assertTrue(set_call)

        self.assertTrue(event_port_add_mock.add_network_services_folder.called)
        self.assertTrue(event_port_add_mock.add_dhcp_document.called)
        self.assertTrue(event_port_add_mock.add_vnics_folder.called)
        self.assertTrue(event_port_add_mock.add_vnic_document.called)
        self.assertTrue(find_links_for_pnics_mock.add_links.called)
        self.assertTrue(find_links_for_vnics_mock.add_links.called)
        self.assertTrue(scanner_mock.scan_cliques.called)

