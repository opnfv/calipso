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

from discover.events.event_port_delete import EventPortDelete
from test.event_based_scan.test_data.event_payload_port_delete import \
    EVENT_PAYLOAD_PORT_DELETE, PORT_DOC, VNIC_DOC, INSTANCE_DOC, INSTANCE_DOCS
from test.event_based_scan.test_event_delete_base import TestEventDeleteBase


class TestPortDelete(TestEventDeleteBase):

    def get_by_id(self, env, object_id):
        if object_id == PORT_DOC['id']:
            return PORT_DOC
        elif object_id == VNIC_DOC['id']:
            return VNIC_DOC
        else:
            return None

    def get_by_field(self, environment, item_type, field_name, field_value,
                     get_single=False):
        if item_type == "vnic":
            return VNIC_DOC
        elif item_type == "instance":
            return INSTANCE_DOC
        else:
            return None

    @patch("discover.events.event_port_delete.ApiFetchHostInstances")
    def test_handle_port_delete(self,
                                api_fetch_instances_class_mock):
        self.values = EVENT_PAYLOAD_PORT_DELETE

        self.inv.get_by_id.side_effect = self.get_by_id
        self.inv.get_by_field.side_effect = self.get_by_field

        api_fetch_instances_mock = api_fetch_instances_class_mock.return_value
        api_fetch_instances_mock.get.return_value = INSTANCE_DOCS

        res = EventPortDelete().handle(self.env, self.values)

        self.assertTrue(res.result)
        self.check_inv_calls(VNIC_DOC)
        self.inv.delete.assert_any_call('inventory', {'id': PORT_DOC['id']})
