###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.events.event_network_update import EventNetworkUpdate
from test.event_based_scan.test_data.event_payload_network_update import EVENT_PAYLOAD_NETWORK_UPDATE, \
    NETWORK_DOCUMENT
from test.event_based_scan.test_event import TestEvent


class TestNetworkUpdate(TestEvent):

    def test_handle_network_update(self):
        self.values = EVENT_PAYLOAD_NETWORK_UPDATE
        self.payload = self.values['payload']
        self.network = self.payload['network']
        name = self.network['name']
        status = self.network['admin_state_up']

        self.network_id = self.network['id']
        self.item_ids.append(self.network_id)
        self.set_item(NETWORK_DOCUMENT)

        EventNetworkUpdate().handle(self.env, self.values)

        network_document = self.inv.get_by_id(self.env, self.network_id)
        self.assertEqual(network_document['name'], name)
        self.assertEqual(network_document['admin_state_up'], status)
