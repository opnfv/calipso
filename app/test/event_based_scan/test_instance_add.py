###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import patch, ANY, call

from discover.events.event_instance_add import EventInstanceAdd
from test.event_based_scan.test_data.event_payload_instance_add \
    import EVENT_PAYLOAD_INSTANCE_ADD, INSTANCES_ROOT, HOST
from test.event_based_scan.test_event import TestEvent


class TestInstanceAdd(TestEvent):

    def get_by_id(self, env, object_id):
        instance_root_id = '-'.join((self.payload['host'], 'instances'))
        if object_id == instance_root_id:
            return INSTANCES_ROOT
        elif object_id:
            return HOST
        else:
            return None

    # Patch ScanHost entirely to negate its side effects and supply our own
    @patch("discover.events.event_instance_add.Scanner")
    def test_handle_instance_add(self, scanner_mock):
        self.values = EVENT_PAYLOAD_INSTANCE_ADD
        self.payload = self.values['payload']
        instance_id = self.payload['instance_id']

        self.inv.get_by_id.side_effect = self.get_by_id

        handler = EventInstanceAdd()
        ret = handler.handle(self.env, self.values)

        self.assertEqual(ret.result, True)

        root_call = call(ANY, INSTANCES_ROOT,
                         limit_to_child_id=instance_id,
                         limit_to_child_type='instance')
        host_call = call(ANY, HOST,
                         limit_to_child_type=ANY)

        scanner = scanner_mock.return_value
        scanner.scan.assert_has_calls([root_call, host_call])
