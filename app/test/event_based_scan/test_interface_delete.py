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

from discover.events.event_base import EventResult
from discover.events.event_interface_delete import EventInterfaceDelete
from test.event_based_scan.test_data.event_payload_interface_delete \
    import EVENT_PAYLOAD_INTERFACE_DELETE, PORT_DOC, ROUTER_DOCUMENT
from test.event_based_scan.test_event import TestEvent
from utils.util import encode_router_id


class TestInterfaceDelete(TestEvent):

    def get_by_id(self, env, object_id):
        if object_id == self.port_id:
            return PORT_DOC
        elif object_id == self.router_id:
            return ROUTER_DOCUMENT
        else:
            return None

    @patch("discover.events.event_interface_delete.EventPortDelete")
    def test_handle_interface_delete(self,
                                     port_delete_class_mock):
        self.values = EVENT_PAYLOAD_INTERFACE_DELETE
        self.payload = self.values['payload']
        self.interface = self.payload['router_interface']
        self.port_id = self.interface['port_id']
        self.router_id = encode_router_id(self.interface['id'])

        port_delete_mock = port_delete_class_mock.return_value
        port_delete_mock.delete_port.return_value = EventResult(result=True)

        self.inv.get_by_id.side_effect = self.get_by_id

        res = EventInterfaceDelete().handle(self.env, self.values)

        self.assertTrue(res.result)
        self.assertTrue(port_delete_mock.delete_port.called)
        self.inv.set.assert_called_with(ROUTER_DOCUMENT)

