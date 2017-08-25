###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.events.event_instance_update import EventInstanceUpdate
from test.event_based_scan.test_data.event_payload_instance_update \
    import EVENT_PAYLOAD_INSTANCE_UPDATE, INSTANCE_DOCUMENT, \
    UPDATED_INSTANCE_FIELDS
from test.event_based_scan.test_event import TestEvent


class TestInstanceUpdate(TestEvent):

    def test_handle_normal_situation(self):
        self.values = EVENT_PAYLOAD_INSTANCE_UPDATE
        payload = self.values['payload']
        self.instance_id = payload['instance_id']

        instance = INSTANCE_DOCUMENT

        self.inv.get_by_id.return_value = instance

        # update instance document
        res = EventInstanceUpdate().handle(self.env, self.values)

        self.assertTrue(res.result)
        self.assertTrue(self.inv.values_replace.called)
        self.assertTrue(self.inv.set.called)

        # check that all changed fields are updated
        call_args, _ = self.inv.set.call_args
        self.assertTrue(all(item in call_args[0].items()
                            for item in UPDATED_INSTANCE_FIELDS.items()))
