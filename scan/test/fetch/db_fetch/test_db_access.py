###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import MagicMock, patch

from scan.fetchers.db.db_access import DbAccess
from scan.test.fetch.db_fetch.mock_cursor import MockCursor
from scan.test.fetch.db_fetch.test_data.db_access import *
from scan.test.fetch.test_fetch import TestFetch


class TestDbAccess(TestFetch):

    def setUp(self):
        super().setUp()
        self.configure_environment()
        self.fetcher = DbAccess()

    @patch("mysql.connector.connect")
    def test_db_connect(self, db_connect):
        DbAccess.conn = None
        db_conn = MagicMock()
        db_conn.ping = MagicMock()
        db_connect.return_value = db_conn

        self.fetcher.db_connect(DB_CONFIG['host'], DB_CONFIG['port'],
                                DB_CONFIG['user'], DB_CONFIG['pwd'],
                                DB_CONFIG['schema'])

        self.assertEqual(True, db_connect.called, "connect method has't been called")
        db_conn.ping.assert_called_once_with(True)

    def test_connect_to_db(self):
        DbAccess.conn = None
        self.fetcher.db_connect = MagicMock()
        self.fetcher.connect_to_db()

        self.assertEqual(True, self.fetcher.db_connect.called)

    def test_connect_to_db_with_force(self):
        DbAccess.conn = MagicMock()
        self.fetcher.db_connect = MagicMock()
        self.fetcher.connect_to_db(force=True)

        self.assertEqual(True, self.fetcher.db_connect.called)

    def test_connect_to_db_without_force(self):
        DbAccess.conn = MagicMock()
        self.fetcher.db_connect = MagicMock()
        self.fetcher.connect_to_db()

        self.assertEqual(False, self.fetcher.db_connect.called)

    def test_get_objects_list_for_id_with_id(self):
        # mock the initial_data cursor
        mock_cursor = MockCursor(OBJECTS_LIST)
        mock_cursor.execute = MagicMock()

        self.fetcher.connect_to_db = MagicMock()
        DbAccess.conn.cursor = MagicMock(return_value=mock_cursor)

        result = self.fetcher.get_objects_list_for_id(QUERY_WITH_ID, OBJECT_TYPE, ID)

        mock_cursor.execute.assert_called_once_with(QUERY_WITH_ID, [ID])
        self.assertEqual(result, OBJECTS_LIST, "Can't get objects list")

    def test_get_objects_list_for_id_without_id(self):
        mock_cursor = MockCursor(OBJECTS_LIST)

        self.fetcher.connect_to_db = MagicMock()
        DbAccess.conn.cursor = MagicMock(return_value=mock_cursor)
        mock_cursor.execute = MagicMock()

        result = self.fetcher.get_objects_list_for_id(QUERY_WITHOUT_ID, OBJECT_TYPE, None)

        mock_cursor.execute.assert_called_once_with(QUERY_WITHOUT_ID)
        self.assertEqual(result, OBJECTS_LIST, "Can't get objects list")

    def test_get_objects_list_for_id_with_id_with_exception(self):
        mock_cursor = MockCursor(OBJECTS_LIST)
        self.fetcher.connect_to_db = MagicMock()
        # mock exception
        DbAccess.conn.cursor = MagicMock(return_value=mock_cursor)
        mock_cursor.execute = MagicMock(side_effect=[AttributeError, ""])

        result = self.fetcher.get_objects_list_for_id(QUERY_WITH_ID, OBJECT_TYPE, ID)

        self.assertEqual(mock_cursor.execute.call_count, 2, "Can't invoke execute method " +
                                                            "twice when error occurs")
        self.assertEqual(result, OBJECTS_LIST, "Can't get objects list")

    def test_get_objects_list_for_id_without_id_with_exception(self):
        mock_cursor = MockCursor(OBJECTS_LIST)
        self.fetcher.connect_to_db = MagicMock()
        DbAccess.conn.cursor = MagicMock(return_value=mock_cursor)
        mock_cursor.execute = MagicMock(side_effect=[AttributeError, ""])

        result = self.fetcher.get_objects_list_for_id(QUERY_WITHOUT_ID,
                                                      OBJECT_TYPE,
                                                      None)

        self.assertEqual(mock_cursor.execute.call_count, 2, "Can't invoke execute method " +
                                                            "twice when error occurs")
        self.assertEqual(result, OBJECTS_LIST, "Can't get objects list")
