###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.events.event_interface_delete import EventInterfaceDelete
from discover.fetchers.api.api_access import ApiAccess
from test.event_based_scan.test_data.event_payload_interface_delete import EVENT_PAYLOAD_INTERFACE_DELETE, NETWORK_DOC, \
    EVENT_PAYLOAD_REGION, PORT_DOC, ROUTER_DOCUMENT, HOST, VNIC_DOCS
from test.event_based_scan.test_event import TestEvent
from utils.util import encode_router_id


class TestInterfaceDelete(TestEvent):
    def test_handle_interface_delete(self):
        self.values = EVENT_PAYLOAD_INTERFACE_DELETE
        self.payload = self.values['payload']
        self.interface = self.payload['router_interface']

        self.port_id = self.interface['port_id']
        self.host_id = self.values["publisher_id"].replace("network.", "", 1)
        self.router_id = encode_router_id(self.host_id, self.interface['id'])

        # set document for instance deleting.
        self.set_item(NETWORK_DOC)
        self.set_item(PORT_DOC)
        self.set_item(ROUTER_DOCUMENT)
        self.set_item(HOST)
        self.set_item(VNIC_DOCS[0])
        ApiAccess.regions = EVENT_PAYLOAD_REGION

        # delete interface
        EventInterfaceDelete().handle(self.env, self.values)

        # assert data
        router_doc = self.inv.get_by_id(self.env, ROUTER_DOCUMENT['id'])
        self.assertNotIn(NETWORK_DOC['id'], router_doc['network'])

        self.assert_empty_by_id(PORT_DOC['id'])
        self.assert_empty_by_id(VNIC_DOCS[0]['id'])
