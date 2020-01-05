###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import patch, call

import re
from bson import ObjectId

from listen.events.event_base import EventBase
from listen.test.event_based_scan.test_event import TestEvent


class TestEventDeleteBase(TestEvent):

    def setUp(self):
        super().setUp()
        self.values = {}

        self.cf = patch("discover.events.event_delete_base.CliqueFinder")
        self.clique_finder = self.cf.start().return_value
        self.clique_finder.find_links_by_source.return_value = []
        self.clique_finder.find_links_by_target.return_value = []

    def handle_delete(self, handler: EventBase, db_object: dict):
        with patch("discover.events.event_delete_base.CliqueFinder") as cf:
            self.inv.get_by_id.return_value = db_object

            event_result = handler.handle(self.env, self.values)
            self.assertTrue(event_result.result)

            self.check_inv_calls(db_object)

    def check_inv_calls(self, db_object):
        db_id = ObjectId(db_object['_id'])
        id_path_regex = re.compile('^{}/'.format(db_object['id_path']))

        delete_clique = call('cliques', {'focal_point': db_id})
        delete_source_links = call('links', {'source': db_id})
        delete_target_links = call('links', {'target': db_id})
        delete_object = call('inventory', {'_id': db_id})
        delete_id_path = call('inventory', {'id_path':
                                                {'$regex': id_path_regex}})

        self.inv.delete.assert_has_calls([delete_clique,
                                          delete_source_links,
                                          delete_target_links,
                                          delete_object,
                                          delete_id_path])

    def tearDown(self):
        super().tearDown()
        self.cf.stop()