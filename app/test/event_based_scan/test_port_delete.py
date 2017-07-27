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

from discover.events.event_port_delete import EventPortDelete
from discover.fetchers.api.api_fetch_host_instances import ApiFetchHostInstances
from test.event_based_scan.test_data.event_payload_port_delete import EVENT_PAYLOAD_PORT_DELETE, PORT_DOC, VNIC_DOCS, \
    INSTANCE_DOC, INSTANCE_DOCS
from test.event_based_scan.test_event import TestEvent


class TestPortDelete(TestEvent):
    def test_handle_port_delete(self):
        self.values = EVENT_PAYLOAD_PORT_DELETE
        self.payload = self.values['payload']
        self.port_id = self.payload['port_id']
        self.item_ids.append(self.port_id)

        # set port data firstly.
        self.set_item(PORT_DOC)
        self.set_item(VNIC_DOCS[0])
        self.set_item(INSTANCE_DOC)

        # mock methods
        original_get_instance = ApiFetchHostInstances.get
        ApiFetchHostInstances.get = MagicMock(return_value=INSTANCE_DOCS)
        self.item_ids.append(INSTANCE_DOCS[0]['id'])

        # delete port
        EventPortDelete().handle(self.env, self.values)

        # assert data
        self.assert_empty_by_id(self.port_id)
        self.assert_empty_by_id(VNIC_DOCS[0]['id'])
        instance = self.inv.get_by_id(self.env, INSTANCE_DOC['id'])
        self.assertEqual(instance['mac_address'], None)
        self.assertEqual(instance['network'], [])
        self.assertEqual(instance['network_info'], [])

        ApiFetchHostInstances.get = original_get_instance
