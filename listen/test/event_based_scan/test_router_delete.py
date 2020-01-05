###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from listen.events.event_router_delete import EventRouterDelete
from listen.test.event_based_scan.test_data.event_payload_router_delete \
    import EVENT_PAYLOAD_ROUTER_DELETE, ROUTER_DOCUMENT
from listen.test.event_based_scan.test_event_delete_base import TestEventDeleteBase


class TestRouterDelete(TestEventDeleteBase):

    def setUp(self):
        super().setUp()
        self.values = EVENT_PAYLOAD_ROUTER_DELETE

    def test_handle_router_delete(self):
        self.handle_delete(handler=EventRouterDelete(),
                           db_object=ROUTER_DOCUMENT)
