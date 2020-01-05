###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from listen.events.event_network_add import EventNetworkAdd
from listen.test.event_based_scan.test_data.event_payload_network_add \
    import EVENT_PAYLOAD_NETWORK_ADD, NETWORK_DOCUMENT
from listen.test.event_based_scan.test_event import TestEvent


class TestNetworkAdd(TestEvent):

    def test_handle_network_add(self):
        self.values = EVENT_PAYLOAD_NETWORK_ADD

        self.inv.get_by_id.return_value = None

        # add network document
        res = EventNetworkAdd().handle(self.env, self.values)

        self.assertTrue(res.result)
        self.inv.set.assert_called_with(NETWORK_DOCUMENT)
