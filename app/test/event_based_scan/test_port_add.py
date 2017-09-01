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

from discover.events.event_port_add import EventPortAdd
from test.event_based_scan.test_data.event_payload_port_add import \
    EVENT_PAYLOAD_PORT_INSTANCE_ADD, NETWORK_DOC, \
    INSTANCE_DOC, INSTANCES_ROOT, VNIC_DOCS, INSTANCE_DOCS, PORTS_FOLDER, \
    PORT_DOC
from test.event_based_scan.test_event import TestEvent


class TestPortAdd(TestEvent):

    def get_by_id(self, env, object_id):
        if object_id == self.network_id:
            return NETWORK_DOC
        elif object_id == "{}-ports".format(self.network_id):
            return PORTS_FOLDER
        elif object_id == self.instance_id:
            return INSTANCE_DOC
        elif object_id == "{}-instances".format(self.host_id):
            return INSTANCES_ROOT
        elif [call for call in self.inv.set.call_args_list
                   if call[0][0].get('type') == 'port']:
            self.port_set = True
            return PORT_DOC
        else:
            return None

    @patch("discover.events.event_port_add.Scanner")
    @patch("discover.events.event_port_add.FindLinksForVedges")
    @patch("discover.events.event_port_add.FindLinksForInstanceVnics")
    @patch("discover.events.event_port_add.CliFetchInstanceVnics")
    @patch("discover.events.event_port_add.ApiFetchHostInstances")
    def test_handle_port_add(self,
                             api_fetch_instances_class_mock,
                             cli_fetch_instances_class_mock,
                             fl_for_vnics_class_mock,
                             fl_for_vedges_class_mock,
                             scanner_class_mock):
        self.values = EVENT_PAYLOAD_PORT_INSTANCE_ADD
        self.payload = self.values['payload']
        self.port = self.payload['port']
        self.host_id = self.port['binding:host_id']
        self.instance_id = INSTANCE_DOC['id']
        self.network_id = NETWORK_DOC['id']

        self.inv.get_by_id.side_effect = self.get_by_id

        api_fetch_instances_mock = api_fetch_instances_class_mock.return_value
        api_fetch_instances_mock.get.return_value = INSTANCE_DOCS

        cli_fetch_instances_mock = cli_fetch_instances_class_mock.return_value
        cli_fetch_instances_mock.get.return_value = VNIC_DOCS

        scanner_mock = scanner_class_mock.return_value
        fl_for_vnics_mock = fl_for_vnics_class_mock.return_value
        fl_for_vedges_mock = fl_for_vedges_class_mock.return_value

        res = EventPortAdd().handle(self.env, self.values)

        self.assertTrue(res.result)
        # Assert that port has been added to db
        self.assertTrue(self.port_set)
        self.assertTrue(fl_for_vnics_mock.add_links.called)
        self.assertTrue(fl_for_vedges_mock.add_links.called)
        self.assertTrue(scanner_mock.scan_cliques.called)
