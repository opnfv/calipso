###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import MagicMock

import bson

from base.utils.inventory_mgr import InventoryMgr
from scan.link_finders.find_implicit_links import FindImplicitLinks
from scan.test.fetch.link_finders.test_data.test_find_implicit_links import *
from scan.test.fetch.test_fetch import TestFetch


class TestFindImplicitLinks(TestFetch):

    def setUp(self):
        super().setUp()
        self.configure_environment()
        self.fetcher = FindImplicitLinks()
        self.fetcher.set_env(ENV)
        self.fetcher.constraint_attributes = ['network']
        self.original_write_link = self.inv.write_link
        self.inv.write_link = lambda x: x
        self.original_objectid = bson.ObjectId
        bson.ObjectId = lambda x: x

    def tearDown(self):
        super().tearDown()
        bson.ObjectId = self.original_objectid
        self.inv.write_link = self.original_write_link

    def test_get_constraint_attributes(self):
        original_find = InventoryMgr.find
        InventoryMgr.find = MagicMock(return_value=CLIQUE_CONSTRAINTS)
        constraint_types = self.fetcher.get_constraint_attributes()
        self.assertEqual(sorted(constraint_types), sorted(CONSTRAINTS))
        InventoryMgr.find = original_find

    def test_constraints_match(self):
        matcher = self.fetcher.constraints_match
        self.assertTrue(matcher(LINK_ATTRIBUTES_NONE, LINK_ATTRIBUTES_NONE_2))
        self.assertTrue(matcher(LINK_ATTRIBUTES_NONE, LINK_ATTRIBUTES_EMPTY))
        self.assertTrue(matcher(LINK_ATTRIBUTES_NONE, LINK_ATTR_V1))
        self.assertTrue(matcher(LINK_ATTRIBUTES_EMPTY, LINK_ATTR_V1))
        self.assertTrue(matcher(LINK_ATTR_V1, LINK_ATTR_V1_2))
        self.assertTrue(matcher(LINK_ATTR_V1,
                                LINK_ATTR_V1_AND_A2V2))
        self.assertFalse(matcher(LINK_ATTR_V1, LINK_ATTR_V2))

    def test_links_match(self):
        matcher = self.fetcher.links_match
        self.assertFalse(matcher(LINK_TYPE_1, LINK_TYPE_1_2))
        self.assertFalse(matcher(LINK_TYPE_1, LINK_TYPE_1_REVERSED))
        self.assertFalse(matcher(LINK_TYPE_4_NET1, LINK_TYPE_5_NET2))
        self.assertFalse(matcher(LINK_TYPE_1_2, LINK_TYPE_2))
        self.assertTrue(matcher(LINK_TYPE_1, LINK_TYPE_2))

    def test_get_link_constraint_attributes(self):
        getter = self.fetcher.get_link_constraint_attributes
        self.assertEqual(getter(LINK_TYPE_1, LINK_TYPE_1_2), {})
        self.assertEqual(getter(LINK_TYPE_1, LINK_TYPE_4_NET1),
                         LINK_TYPE_4_NET1.get('attributes'))
        self.assertEqual(getter(LINK_TYPE_4_NET1, LINK_TYPE_1),
                         LINK_TYPE_4_NET1.get('attributes'))
        self.assertEqual(getter(LINK_TYPE_1, LINK_TYPE_5_NET2),
                         LINK_TYPE_5_NET2.get('attributes'))
        self.assertEqual(getter(LINK_TYPE_4_NET1, LINK_TYPE_6_NET1),
                         LINK_TYPE_4_NET1.get('attributes'))

    def test_get_attr(self):
        getter = self.fetcher.get_attr
        self.assertIsNone(getter('host', {}, {}))
        self.assertIsNone(getter('host', {'host': 'v1'}, {'host': 'v2'}))
        self.assertEqual(getter('host', {'host': 'v1'}, {}), 'v1')
        self.assertEqual(getter('host', {}, {'host': 'v2'}), 'v2')
        self.assertEqual(getter('host', {'host': 'v1'}, {'host': 'v1'}), 'v1')

    def test_add_implicit_link(self):
        original_write_link = self.inv.write_link
        self.inv.write_link = lambda x: x
        original_objectid = bson.ObjectId
        bson.ObjectId = lambda x: x
        add_func = self.fetcher.add_implicit_link
        original_get_existing_link = self.fetcher.get_existing_link
        self.fetcher.get_existing_link = self.mock_get_existing_link
        self.assertEqual(add_func(LINK_TYPE_4_NET1, LINK_TYPE_6_NET1),
                         LINK_TYPE_7_NET1)
        self.fetcher.get_existing_link = original_get_existing_link
        bson.ObjectId = original_objectid
        self.inv.write_link = original_write_link

    @staticmethod
    def mock_get_existing_link(link_type=None,
                               source_id=None, target_id=None):
        matches = [l for l in BASE_LINKS
                   if l['link']['link_type'] == link_type
                   and l['link']['source_id'] == source_id
                   and l['link']['target_id'] == target_id]
        return matches[0] if matches else None

    def test_get_transitive_closure(self):
        self.fetcher.links = BASE_LINKS
        original_get_existing_link = self.fetcher.get_existing_link
        self.fetcher.get_existing_link = self.mock_get_existing_link
        self.fetcher.get_transitive_closure()
        self.fetcher.get_existing_link = original_get_existing_link
        last_pass = max(l['pass'] for l in IMPLICIT_LINKS) + 1
        for pass_no in range(1, last_pass):
            actual_implicit_links = [l for l in self.fetcher.links
                                     if l['pass'] == pass_no]
            expected_implicit_links = [l for l in IMPLICIT_LINKS
                                       if l['pass'] == pass_no]
            self.assertEqual(actual_implicit_links, expected_implicit_links,
                             'incorrect links for pass #{}'.format(pass_no))
