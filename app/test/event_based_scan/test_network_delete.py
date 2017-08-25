###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.events.event_network_delete import EventNetworkDelete
from test.event_based_scan.test_data.event_payload_network_delete import EVENT_PAYLOAD_NETWORK_DELETE, \
    NETWORK_DOCUMENT
from test.event_based_scan.test_event_delete_base import TestEventDeleteBase


class TestNetworkDelete(TestEventDeleteBase):

    def setUp(self):
        super().setUp()
        self.values = EVENT_PAYLOAD_NETWORK_DELETE

    def test_handle_network_delete(self):
        self.handle_delete(handler=EventNetworkDelete(),
                           db_object=NETWORK_DOCUMENT)
