###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import patch

from listen.events.event_base import EventResult
from listen.events.event_delete_base import EventDeleteBase
from listen.events.event_subnet_delete import EventSubnetDelete
from listen.test.event_based_scan.test_data.event_payload_subnet_delete \
    import EVENT_PAYLOAD_SUBNET_DELETE, NETWORK_DOC, VNIC_DOC
from listen.test.event_based_scan.test_event import TestEvent


class TestSubnetDelete(TestEvent):

    def get_by_field(self, environment, item_type, field_name, field_value,
                     get_single=False):
        if item_type == "network":
            return NETWORK_DOC
        elif item_type == "vnic":
            return VNIC_DOC
        else:
            return None

    @patch.object(EventDeleteBase, "delete_handler",
                  return_value=EventResult(result=True))
    def test_handle_subnet_delete(self,
                                  delete_handler_mock):
        self.values = EVENT_PAYLOAD_SUBNET_DELETE
        self.subnet_id = self.values['payload']['subnet_id']
        self.network_doc = NETWORK_DOC
        self.network_id = self.network_doc['id']
        self.vnic_id = VNIC_DOC['id']
        self.vnic_folder_id = 'qdhcp-{}'.format(self.network_id)

        self.inv.get_by_field.side_effect = self.get_by_field

        res = EventSubnetDelete().handle(self.env, self.values)

        self.assertTrue(res.result)
        delete_handler_mock.assert_called_with(self.env,
                                               self.vnic_folder_id, "vservice")

        updated_network = [call[0][0] for call in self.inv.set.call_args_list
                           if call[0][0]['type'] == 'network']
        self.assertTrue(updated_network)
        self.assertTrue(self.subnet_id
                        not in updated_network[0].get('subnet_ids'))
        self.assertTrue(self.inv.delete.called)

