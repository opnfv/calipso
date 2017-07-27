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
from test.event_based_scan.test_data.event_payload_instance_update import EVENT_PAYLOAD_INSTANCE_UPDATE, INSTANCE_DOCUMENT
from test.event_based_scan.test_event import TestEvent


class TestInstanceUpdate(TestEvent):

    def test_handle_normal_situation(self):
        self.values = EVENT_PAYLOAD_INSTANCE_UPDATE
        payload = self.values['payload']
        self.instance_id = payload['instance_id']
        self.item_ids.append(self.instance_id)
        new_name = payload['display_name']

        # preparing instance to be updated
        instance = self.inv.get_by_id(self.env, self.instance_id)
        if not instance:
            self.log.info("instance document is not found, add document for updating")

            # add instance document for updating
            self.set_item(INSTANCE_DOCUMENT)
            instance = self.inv.get_by_id(self.env, self.instance_id)
            self.assertIsNotNone(instance)
            self.assertEqual(instance['name'], INSTANCE_DOCUMENT['name'])

        name_path = instance['name_path']
        new_name_path = name_path[:name_path.rindex('/') + 1] + new_name

        # update instance document
        EventInstanceUpdate().handle(self.env, self.values)

        # get new document
        instance = self.inv.get_by_id(self.env, self.instance_id)

        # check update result.
        self.assertEqual(instance['name'], new_name)
        self.assertEqual(instance['name_path'], new_name_path)
