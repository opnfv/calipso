###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.scanner import Scanner
from test.scan.test_scan import TestScan
from unittest.mock import MagicMock, patch

from discover.link_finders.find_links_metadata_parser \
    import FindLinksMetadataParser
from discover.scan_metadata_parser import ScanMetadataParser
from test.scan.test_data.scanner import *
from monitoring.setup.monitoring_setup_manager import MonitoringSetupManager


class TestScanner(TestScan):

    def setUp(self):
        super().setUp()
        ScanMetadataParser.parse_metadata_file = \
            MagicMock(return_value=METADATA)
        FindLinksMetadataParser.parse_metadata_file = \
            MagicMock(return_value=LINK_FINDERS_METADATA)
        self.scanner = Scanner()
        self.scanner.set_env(self.env)
        MonitoringSetupManager.create_setup = MagicMock()
        self.scanner.inv.monitoring_setup_manager = \
            MonitoringSetupManager(self.env)

    def test_check_type_env_without_environment_condition(self):
        result = self.scanner.check_type_env(TYPE_TO_FETCH_WITHOUT_ENV_CON)

        self.assertEqual(result, True,
                         "Can't get true when the type_to_fetch " +
                         "doesn't contain environment condition")

    def test_check_type_with_error_value(self):
        # store original method
        original_get_env_config = self.scanner.config.get_env_config

        # mock get_env_config method
        self.scanner.config.get_env_config =\
            MagicMock(return_value=CONFIGURATIONS)

        result = self.scanner.check_type_env(TYPE_TO_FETCH_WITH_ERROR_VALUE)

        # reset get_env_config method
        self.scanner.config.get_env_config = original_get_env_config

        self.assertEqual(result, False,
                         "Can't get false when the type_to_fetch " +
                         "contain error value")

    def test_check_type_env_without_mechanism_drivers_in_env_config(self):
        # store original method
        original_get_env_config = self.scanner.config.get_env_config

        # mock get_env_config_method
        self.scanner.config.get_env_config =\
            MagicMock(return_value=CONFIGURATIONS_WITHOUT_MECHANISM_DRIVERS)

        result = self.scanner.check_type_env(TYPE_TO_FETCH)
        # reset get_env_config method
        self.scanner.check_type_env = original_get_env_config

        self.assertEqual(result, False,
                         "Can't get false when configuration " +
                         "doesn't contain mechanism drivers")

    def test_check_type_env_with_wrong_mech_drivers_in_env_condition(self):
        # store original method
        original_get_env_config = self.scanner.config.get_env_config

        # mock get_env_config_method
        self.scanner.config.get_env_config =\
            MagicMock(return_value=CONFIGURATIONS)

        result = self.scanner.\
            check_type_env(TYPE_TO_FETCH_WITH_WRONG_ENVIRONMENT_CONDITION)
        # reset get_env_config method
        self.scanner.check_type_env = original_get_env_config

        self.assertEqual(result, False, "Can't get false when the mechanism " +
                         "drivers in type_to_fetch " +
                         "don't exist in configurations")

    def test_check_type_env(self):
        # store original method
        original_get_env_config = self.scanner.config.get_env_config

        # mock method
        self.scanner.config.get_env_config =\
            MagicMock(return_value=CONFIGURATIONS)

        result = self.scanner.check_type_env(TYPE_TO_FETCH)

        # reset method
        self.scanner.config.get_env_config = original_get_env_config

        self.assertEqual(result, True,
                         "Can't get True when the type_to_fetch is correct")

    def test_scan_error_type(self):
        # store original method
        original_check_type_env = self.scanner.check_type_env

        # mock method
        self.scanner.check_type_env = MagicMock(return_value=False)

        result = self.scanner.scan_type(TYPE_TO_FETCH_FOR_ENVIRONMENT, PARENT,
                                        ID_FIELD)

        # reset method
        self.scanner.check_type_env = original_check_type_env

        self.assertEqual(result, [],
                         "Can't get [], when the type_to_fetch is wrong")

    def test_scan_type_without_parent_id(self):
        try:
            self.scanner.scan_type(TYPE_TO_FETCH_FOR_ENVIRONMENT,
                                   PARENT_WITHOUT_ID, ID_FIELD)
            self.fail("Can't get error when the parent " +
                      "doesn't contain id attribute")
        except:
            pass

    @patch("discover.fetchers.folder_fetcher.FolderFetcher.get")
    def test_scan_type_with_get_exception(self, fetcher_get):
        fetcher_get.side_effect = Exception("get exception")

        try:
            self.scanner.scan_type(TYPE_TO_FETCH_FOR_ENVIRONMENT,
                                            PARENT, ID_FIELD)
            self.fail("Can't get exception when fetcher.get throws an exception")
        except:
            pass

    @patch("discover.fetchers.folder_fetcher.FolderFetcher.get")
    def test_scan_type_without_master_parent(self, fetcher_get):
        fetcher_get.return_value = DB_RESULTS_WITHOUT_MASTER_PARENT_IN_DB

        # store original get_by_id
        original_get_by_id = self.scanner.inv.get_by_id
        original_set = self.scanner.inv.set

        # mock methods
        self.scanner.inv.get_by_id = MagicMock(return_value=[])

        result = self.scanner.scan_type(TYPE_TO_FETCH_FOR_ENVIRONMENT, PARENT,
                                        ID_FIELD)

        # reset methods
        self.scanner.inv.get_by_id = original_get_by_id
        self.scanner.inv.set = original_set
        self.assertEqual(result, [], "Can't get [], when the master parent " +
                         "doesn't exist in database")

    @patch("discover.fetchers.folder_fetcher.FolderFetcher.get")
    def test_scan_type_with_master_parent(self, fetcher_get):
        fetcher_get.return_value = DB_RESULTS_WITH_MASTER_PARENT_IN_DB

        # store original methods
        original_get_by_id = self.scanner.inv.get_by_id
        original_set = self.scanner.inv.set

        # mock methods
        self.scanner.inv.get_by_id = MagicMock(return_value=MASTER_PARENT)
        self.scanner.inv.set = MagicMock()

        self.scanner.scan_type(TYPE_TO_FETCH_FOR_ENVIRONMENT, PARENT, ID_FIELD)
        self.assertEqual(self.scanner.inv.set.call_count, 2, "Can't create additional folder")
        self.assertNotIn("master_parent_type", DB_RESULTS_WITH_MASTER_PARENT_IN_DB, "Can't delete the master_parent_type")
        self.assertNotIn("master_parent_id", DB_RESULTS_WITH_MASTER_PARENT_IN_DB, "Can't delete the master_parent_id")

        # reset methods
        self.scanner.inv.get_by_id = original_get_by_id
        self.scanner.inv.set = original_set

    @patch("discover.fetchers.folder_fetcher.FolderFetcher.get")
    def test_scan_type_with_in_project(self, fetcher_get):
        fetcher_get.return_value = DB_RESULTS_WITH_PROJECT

        # store original method
        original_set = self.scanner.inv.set

        # mock method
        self.scanner.inv.set = MagicMock()

        self.scanner.scan_type(TYPE_TO_FETCH_FOR_ENVIRONMENT, PARENT, ID_FIELD)
        self.assertIn("projects", DB_RESULTS_WITH_PROJECT[0],
                      "Can't get the projects from DB result")
        self.assertNotIn(PROJECT_KEY, DB_RESULTS_WITH_PROJECT[0],
                         "Can't delete the project key in the object")

        self.scanner.inv.set = original_set

    @patch("discover.fetchers.folder_fetcher.FolderFetcher.get")
    def test_scan_type_without_create_object(self, fetcher_get):
        fetcher_get.return_value = DB_RESULTS_WITHOUT_CREATE_OBJECT

        original_set = self.scanner.inv.set

        self.scanner.inv.set = MagicMock()
        self.scanner.scan_type(TYPE_TO_FETCH_FOR_ENVIRONMENT, PARENT, ID_FIELD)

        self.assertEqual(self.scanner.inv.set.call_count, 0,
                         "Set the object when the create object is false")

        self.scanner.inv.set = original_set

    @patch("discover.fetchers.folder_fetcher.FolderFetcher.get")
    def test_scan_type_with_create_object(self, fetcher_get):
        fetcher_get.return_value = DB_RESULTS_WITH_CREATE_OBJECT

        original_set = self.scanner.inv.set

        self.scanner.inv.set = MagicMock()
        self.scanner.scan_type(TYPE_TO_FETCH_FOR_ENVIRONMENT, PARENT, ID_FIELD)

        self.assertEqual(self.scanner.inv.set.call_count, 1,
                         "Set the object when the create object is false")

        self.scanner.inv.set = original_set

    @patch("discover.fetchers.folder_fetcher.FolderFetcher.get")
    def test_scan_type_with_children_scanner(self, fetcher_get):
        fetcher_get.return_value = DB_RESULTS_WITH_CREATE_OBJECT

        original_set = self.scanner.inv.set
        original_queue_for_scan = self.scanner.queue_for_scan

        self.scanner.inv.set = MagicMock()
        self.scanner.queue_for_scan = MagicMock()

        self.scanner.scan_type(TYPE_TO_FETCH_FOR_ENVIRONMENT, PARENT, ID_FIELD)

        self.assertEqual(self.scanner.queue_for_scan.call_count, 1,
                         "Can't put children scanner in the queue")

        self.scanner.inv.set = original_set
        self.scanner.queue_for_scan = original_queue_for_scan

    @patch("discover.fetchers.folder_fetcher.FolderFetcher.get")
    def test_scan_type_without_children_scanner(self, fetcher_get):
        fetcher_get.return_value = DB_RESULTS_WITH_CREATE_OBJECT

        original_set = self.scanner.inv.set
        original_queue_for_scan = self.scanner.queue_for_scan

        self.scanner.inv.set = MagicMock()
        self.scanner.queue_for_scan = MagicMock()

        self.scanner.scan_type(TYPE_TO_FETCH_FOR_ENV_WITHOUT_CHILDREN_FETCHER,
                               PARENT, ID_FIELD)

        self.assertEqual(self.scanner.queue_for_scan.call_count, 0,
                         "Can't put children scanner in the queue")

        self.scanner.inv.set = original_set
        self.scanner.queue_for_scan = original_queue_for_scan

    @patch("discover.fetchers.folder_fetcher.FolderFetcher.get")
    def test_scan_type(self, fetcher_get):
        fetcher_get.return_value = DB_RESULTS_WITH_CREATE_OBJECT

        original_set = self.scanner.inv.set
        original_queue_for_scan = self.scanner.queue_for_scan

        self.scanner.inv.set = MagicMock()
        self.scanner.queue_for_scan = MagicMock()

        result = self.scanner.scan_type(TYPE_TO_FETCH_FOR_ENVIRONMENT, PARENT,
                                        ID_FIELD)

        self.assertNotEqual(result, [], "Can't get children form scan_type")

        self.scanner.inv.set = original_set
        self.scanner.queue_for_scan = original_queue_for_scan

    def test_scan_with_limit_to_child_type(self):
        original_scan_type = self.scanner.scan_type
        original_get_scanner = self.scanner.get_scanner

        self.scanner.scan_type = MagicMock(return_value=[])
        self.scanner.get_scanner = MagicMock(return_value=TYPES_TO_FETCH)

        limit_to_child_type = TYPES_TO_FETCH[0]['type']

        self.scanner.scan(SCANNER_TYPE_FOR_ENV, PARENT, limit_to_child_type=limit_to_child_type)

        # only scan the limit child type
        self.scanner.scan_type.assert_called_with(TYPES_TO_FETCH[0], PARENT,
                                                  ID_FIELD)

        self.scanner.scan_type = original_scan_type
        self.scanner.get_scanner = original_get_scanner

    def test_scan_with_limit_to_child_id(self):
        original_scan_type = self.scanner.scan_type
        original_get_scanner = self.scanner.get_scanner

        self.scanner.get_scanner = MagicMock(return_value=TYPES_TO_FETCH)
        limit_to_child_id = SCAN_TYPE_RESULTS[0][ID_FIELD]

        self.scanner.scan_type = MagicMock(return_value=SCAN_TYPE_RESULTS)

        children = self.scanner.scan(SCANNER_TYPE_FOR_ENV, PARENT, id_field=ID_FIELD,
                                     limit_to_child_id=limit_to_child_id)

        # only get the limit child
        self.assertEqual(children, SCAN_TYPE_RESULTS[0])

        self.scanner.scan_type = original_scan_type
        self.scanner.get_scanner = original_get_scanner

    def test_scan(self):
        original_scan_type = self.scanner.scan_type
        original_get_scanner = self.scanner.get_scanner

        self.scanner.get_scanner = MagicMock(return_values=TYPES_TO_FETCH)
        result = self.scanner.scan(SCANNER_TYPE_FOR_ENV, PARENT)

        self.assertEqual(PARENT, result,
                         "Can't get the original parent after the scan")

        self.scanner.get_scanner = original_get_scanner
        self.scanner.scan_type = original_scan_type

    def test_run_scan(self):
        original_scan = self.scanner.scan
        original_scan_from_queue = self.scanner.scan_from_queue

        self.scanner.scan = MagicMock()
        self.scanner.scan_from_queue = MagicMock()

        self.scanner.run_scan(SCANNER_TYPE_FOR_ENV, PARENT, ID_FIELD, LIMIT_TO_CHILD_ID,
                              LIMIT_TO_CHILD_TYPE)

        self.scanner.scan.assert_called_with(SCANNER_TYPE_FOR_ENV, PARENT, ID_FIELD,
                                             LIMIT_TO_CHILD_ID,
                                             LIMIT_TO_CHILD_TYPE)
        self.scanner.scan_from_queue.assert_any_call()

        self.scanner.scan = original_scan
        self.scanner.scan_from_queue = original_scan_from_queue

    @patch("discover.scanner.Scanner.scan")
    def test_scan_from_queue(self, scan):
        scan.return_value = []
        Scanner.scan_queue = SCAN_QUEUE

        self.scanner.scan_from_queue()

        self.assertEqual(self.scanner.scan.call_count, QUEUE_SIZE,
                         "Can't scan all the objects in the queue")
