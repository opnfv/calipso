###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from listen.events.event_network_update import EventNetworkUpdate
from listen.test.event_based_scan.test_data.event_payload_network_update \
    import EVENT_PAYLOAD_NETWORK_UPDATE, NETWORK_DOCUMENT, UPDATED_NETWORK_FIELDS
from listen.test.event_based_scan.test_event import TestEvent


class TestNetworkUpdate(TestEvent):

    def test_handle_network_update(self):
        self.values = EVENT_PAYLOAD_NETWORK_UPDATE
        self.payload = self.values['payload']

        network = NETWORK_DOCUMENT
        self.inv.get_by_id.return_value = network

        res = EventNetworkUpdate().handle(self.env, self.values)

        self.assertTrue(res.result)
        self.assertTrue(self.inv.values_replace.called)
        self.assertTrue(self.inv.set.called)

        # check that all changed fields are updated
        call_args, _ = self.inv.set.call_args
        # Assert that all updated fields have been added to initial_data
        self.assertTrue(all(item in call_args[0].items()
                            for item in UPDATED_NETWORK_FIELDS.items()))
