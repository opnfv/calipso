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

from discover.events.event_instance_add import EventInstanceAdd
from test.event_based_scan.test_data.event_payload_instance_add \
    import EVENT_PAYLOAD_INSTANCE_ADD, INSTANCES_ROOT, HOST, INSTANCE_DOCUMENT
from test.event_based_scan.test_event import TestEvent


class TestInstanceAdd(TestEvent):

    def insert_instance(self):
        self.set_item(INSTANCE_DOCUMENT)

    # Patch ScanHost entirely to negate its side effects and supply our own
    @patch("discover.events.event_instance_add.ScanHost")
    def test_handle_instance_add(self, scan_host_mock):
        self.values = EVENT_PAYLOAD_INSTANCE_ADD
        payload = self.values['payload']
        self.instance_id = payload['instance_id']
        host_id = payload['host']

        # prepare instances root, in case it's not there
        self.set_item(INSTANCES_ROOT)

        # prepare host, in case it's not existed.
        self.set_item(HOST)

        # check instance document
        instance = self.inv.get_by_id(self.env, self.instance_id)
        if instance:
            self.log.info('instance document exists, delete it first.')
            self.inv.delete('inventory', {'id': self.instance_id})

            instance = self.inv.get_by_id(self.env, self.instance_id)
            self.assertIsNone(instance)

        # simulate instance insertion after host scan
        scan_host_mock.return_value.scan_links.side_effect = self.insert_instance

        # check the return of instance handler.
        handler = EventInstanceAdd()
        ret = handler.handle(self.env, self.values)

        self.assertEqual(ret.result, True)

        # check host document
        host = self.inv.get_by_id(self.env, host_id)
        self.assertIsNotNone(host)

        # check instance document
        instance_document = self.inv.get_by_id(self.env, self.instance_id)
        self.assertIsNotNone(instance_document)
