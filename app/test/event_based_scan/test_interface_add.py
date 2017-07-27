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

from discover.events.event_interface_add import EventInterfaceAdd
from discover.fetchers.api.api_access import ApiAccess
from discover.fetchers.api.api_fetch_port import ApiFetchPort
from discover.fetchers.cli.cli_fetch_host_vservice import CliFetchHostVservice
from discover.fetchers.cli.cli_fetch_vservice_vnics import CliFetchVserviceVnics
from discover.find_links_for_vservice_vnics import FindLinksForVserviceVnics
from test.event_based_scan.test_data.event_payload_interface_add import EVENT_PAYLOAD_INTERFACE_ADD, NETWORK_DOC, \
    EVENT_PAYLOAD_REGION, PORT_DOC, ROUTER_DOCUMENT, HOST, VNIC_DOCS
from test.event_based_scan.test_event import TestEvent
from utils.util import encode_router_id


class TestInterfaceAdd(TestEvent):
    def test_handle_interface_add(self):
        self.values = EVENT_PAYLOAD_INTERFACE_ADD
        self.payload = self.values['payload']
        self.interface = self.payload['router_interface']

        self.port_id = self.interface['port_id']
        self.host_id = self.values["publisher_id"].replace("network.", "", 1)
        self.router_id = encode_router_id(self.host_id, self.interface['id'])

        self.set_item(NETWORK_DOC)
        ApiAccess.regions = EVENT_PAYLOAD_REGION

        # mock port data,
        original_api_get_port = ApiFetchPort.get
        ApiFetchPort.get = MagicMock(return_value=[PORT_DOC])
        self.item_ids.append(PORT_DOC['id'])

        # set router document
        self.set_item(ROUTER_DOCUMENT)

        # set host document
        self.set_item(HOST)

        # mock add_links
        original_add_links = FindLinksForVserviceVnics.add_links
        FindLinksForVserviceVnics.add_links = MagicMock()

        # mock get_vservice
        original_get_vservice = CliFetchHostVservice.get_vservice
        CliFetchHostVservice.get_vservice = MagicMock(return_value=ROUTER_DOCUMENT)

        # mock handle_vservice
        original_handle_service = CliFetchVserviceVnics.handle_service
        CliFetchVserviceVnics.handle_service = MagicMock(return_value=VNIC_DOCS)

        # handle the notification
        EventInterfaceAdd().handle(self.env, self.values)

        # reset the method.
        ApiFetchPort.get = original_api_get_port
        FindLinksForVserviceVnics.add_links = original_add_links
        CliFetchHostVservice.get_vservice = original_get_vservice
        CliFetchVserviceVnics.handle_service = original_handle_service

        # check port and router document
        port_doc = self.inv.get_by_id(self.env, self.port_id)
        self.assertIsNotNone(port_doc)

        router_doc = self.inv.get_by_id(self.env, self.router_id)
        self.assertIn(NETWORK_DOC['id'], router_doc['network'])
