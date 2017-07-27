###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.db.db_access import DbAccess
from discover.scan_metadata_parser import ScanMetadataParser
from test.scan.test_scan import TestScan
from test.scan.test_data.metadata import *
from unittest import mock
from utils.mongo_access import MongoAccess


SCANNERS_FILE = 'scanners.json'

JSON_REQUIRED_FIELDS_ERROR = 'Metadata json should contain all the ' + \
                             'following fields: scanners_package, scanners'

JSON_NO_SCANNERS = 'no scanners found in scanners list'
JSON_ERRORS_FOUND = 'Errors encountered during metadata file parsing:\n'


class TestScanMetadataParser(TestScan):
    def setUp(self):
        super().setUp()
        DbAccess.conn = mock.MagicMock()
        self.prepare_constants()
        self.parser = ScanMetadataParser(self.inv)

        self.parser.check_metadata_file_ok = mock.MagicMock()

    def prepare_metadata(self, content):
        self.parser._load_json_file = mock.MagicMock(return_value=content)

    def prepare_constants(self):
        MongoAccess.db = mock.MagicMock()
        MongoAccess.db["constants"].find_one = mock.MagicMock(side_effect=
                                                              lambda input:
                                                              CONSTANTS[input["name"]]
                                                              if CONSTANTS.get(input["name"])
                                                              else []
                                                              )

    def handle_error_scenario(self, input_content, expected_error,
                              add_errors_encountered_pretext=True):
        self.prepare_metadata(input_content)
        found_exception = False
        expected_message = expected_error
        metadata = None
        try:
            metadata = self.parser.parse_metadata_file(SCANNERS_FILE)
        except ValueError as e:
            found_exception = True
            expected_message = expected_error \
                if not add_errors_encountered_pretext \
                else JSON_ERRORS_FOUND + expected_error
            self.assertEqual(str(e), expected_message)
        self.assertTrue(found_exception,
                        'failed to throw exception, expected_message: {}'
                        .format(expected_message))
        self.assertIsNone(metadata)

    def handle_json_missing_field(self, json_content):
        self.handle_error_scenario(json_content, JSON_REQUIRED_FIELDS_ERROR,
                                   add_errors_encountered_pretext=False)

    def test_missing_field(self):
        for content in [METADATA_EMPTY, METADATA_NO_PACKAGE,
                        METADATA_NO_SCANNERS]:
            self.handle_json_missing_field(content)

    def test_json_no_scanners(self):
        self.handle_error_scenario(METADATA_ZERO_SCANNERS, JSON_NO_SCANNERS)

    def test_json_scanner_errors(self):
        errors_scenarios = [
            {
                'input': METADATA_ZERO_SCANNERS,
                'msg': JSON_NO_SCANNERS
            },
            {
                'input': METADATA_SCANNER_UNKNOWN_ATTRIBUTE,
                'msg': 'unknown attribute xyz in scanner ScanAggregate, type #1'
            },
            {
                'input': METADATA_SCANNER_NO_TYPE,
                'msg': 'scanner ScanAggregate, type #1: ' +
                       'missing attribute "type"'
            },
            {
                'input': METADATA_SCANNER_NO_FETCHER,
                'msg': 'scanner ScanAggregate, type #1: ' +
                       'missing attribute "fetcher"'
            },
            {
                'input': METADATA_SCANNER_INCORRECT_TYPE,
                'msg': 'scanner ScanAggregate: value not in types: t1'
            },
            {
                'input': METADATA_SCANNER_INCORRECT_FETCHER,
                'msg': 'failed to find fetcher class f1 '
                       'in scanner ScanAggregate type #1'
            },
            {
                'input': METADATA_SCANNER_WITH_INCORRECT_CHILD,
                'msg': 'scanner ScanAggregatesRoot type #1: '
                       'children_scanner must be a string'
            },
            {
                'input': METADATA_SCANNER_WITH_MISSING_CHILD,
                'msg': 'scanner ScanAggregatesRoot type #1: '
                       'children_scanner ScanAggregate not found '
            },
            {
                'input': METADATA_SCANNER_FETCHER_INVALID_DICT,
                'msg': 'scanner ScanEnvironment type #1: '
                       'only folder dict accepted in fetcher'
            },
            {
                'input': METADATA_SCANNER_WITH_INVALID_CONDITION,
                'msg': 'scanner ScanHost type #1: condition must be dict'
            }
        ]
        for scenario in errors_scenarios:
            self.handle_error_scenario(scenario['input'], scenario['msg'])

    def check_json_is_ok(self, json_content):
        self.prepare_metadata(json_content)
        found_exception = False
        metadata = None
        msg = None
        try:
            metadata = self.parser.parse_metadata_file(SCANNERS_FILE)
        except ValueError as e:
            found_exception = True
            msg = str(e)
        self.assertFalse(found_exception, 'Exception: {}'.format(msg))
        self.assertIsNotNone(metadata)

    def test_json_valid_content(self):
        valid_content = [
            METADATA_SIMPLE_SCANNER,
            METADATA_SCANNER_WITH_CHILD,
            METADATA_SCANNER_WITH_FOLDER,
            METADATA_SCANNER_WITH_CONDITION
        ]
        for content in valid_content:
            self.check_json_is_ok(content)
