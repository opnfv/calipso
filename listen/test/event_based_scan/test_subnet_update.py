###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from listen.events.event_subnet_update import EventSubnetUpdate
from listen.test.event_based_scan.test_data.event_payload_subnet_add import EVENT_PAYLOAD_REGION
from listen.test.event_based_scan.test_data.event_payload_subnet_update \
    import EVENT_PAYLOAD_SUBNET_UPDATE, NETWORK_DOC, HOST_DOC
from listen.test.event_based_scan.test_event import TestEvent
from scan.fetchers.api.api_access import ApiAccess


class TestSubnetUpdate(TestEvent):

    def get_by_id(self, env, object_id):
        if object_id == self.network_id:
            return NETWORK_DOC
        elif object_id == self.host_id:
            return HOST_DOC
        else:
            return None

    def test_handle_subnet_add(self):
        self.values = EVENT_PAYLOAD_SUBNET_UPDATE
        self.payload = self.values['payload']
        self.subnet = self.payload['subnet']
        self.subnet_id = self.subnet['id']
        self.network_id = self.subnet['network_id']
        self.host_id = self.values["publisher_id"].replace("network.", "", 1)
        old_subnet_name = list(NETWORK_DOC['subnets'].keys())[0]
        new_subnet_name = self.subnet['name']

        self.inv.get_by_id.side_effect = self.get_by_id

        if not ApiAccess.regions:
            ApiAccess.regions = EVENT_PAYLOAD_REGION

        res = EventSubnetUpdate().handle(self.env, self.values)

        self.assertTrue(res.result)
        updated_network = [call[0][0] for call in self.inv.set.call_args_list
                           if call[0][0]['type'] == 'network']
        self.assertTrue(updated_network)
        self.assertFalse(updated_network[0]['subnets'].get(old_subnet_name))
        self.assertTrue(updated_network[0]['subnets'].get(new_subnet_name))

        if ApiAccess.regions == EVENT_PAYLOAD_REGION:
            ApiAccess.regions = None

    # TODO: write tests for "enable_dhcp" change handling
