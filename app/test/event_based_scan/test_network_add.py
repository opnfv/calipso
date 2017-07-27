###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.events.event_network_add import EventNetworkAdd
from test.event_based_scan.test_data.event_payload_network_add import EVENT_PAYLOAD_NETWORK_ADD
from test.event_based_scan.test_event import TestEvent


class TestNetworkAdd(TestEvent):

    def test_handle_network_add(self):
        self.values = EVENT_PAYLOAD_NETWORK_ADD
        self.payload = self.values['payload']
        self.network = self.payload['network']
        self.network_id = self.network['id']
        self.item_ids.append(self.network_id)

        network_document = self.inv.get_by_id(self.env, self.network_id)
        if network_document:
            self.log.info('network document existed already, deleting it first.')
            self.inv.delete('inventory', {'id': self.network_id})

            network_document = self.inv.get_by_id(self.env, self.network_id)
            self.assertIsNone(network_document)

        # build network document for adding network
        project_name = self.values['_context_project_name']
        project_id = self.values['_context_project_id']
        parent_id = project_id + '-networks'
        network_name = self.network['name']

        # add network document
        EventNetworkAdd().handle(self.env, self.values)

        # check network document
        network_document = self.inv.get_by_id(self.env, self.network_id)
        self.assertIsNotNone(network_document)
        self.assertEqual(network_document["project"], project_name)
        self.assertEqual(network_document["parent_id"], parent_id)
        self.assertEqual(network_document["name"], network_name)

