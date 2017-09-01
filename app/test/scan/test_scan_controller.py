###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import sys
from unittest.mock import MagicMock

from discover.scan import ScanController, ScanPlan
from discover.scanner import Scanner
from test.scan.test_scan import TestScan
from test.scan.test_data.scan import *
from utils.inventory_mgr import InventoryMgr


class TestScanController(TestScan):

    def setUp(self):
        super().setUp()
        self.scan_controller = ScanController()

    def arg_validate(self, args, expected, key, err=None):
        if key not in expected:
            return
        err = err if err else 'The value of {} is wrong'.format(key)
        self.assertEqual(args.get(key, None), expected[key.upper()], err)

    def check_args_values(self, args, expected):
        self.arg_validate(args, expected, 'env',
                          'The value of environment is wrong')
        keys = ['mongo_config', 'mongo_config', 'type', 'inventory',
                'scan_self', 'id', 'parent_id', 'parent_type', 'id_field',
                'loglevel', 'inventory_only', 'links_only', 'cliques_only',
                'clear']
        for key in keys:
            self.arg_validate(args, expected, key)

    def test_get_args_with_default_arguments(self):
        sys.argv = DEFAULT_COMMAND_ARGS
        args = self.scan_controller.get_args()
        # check the default value of each argument
        self.check_args_values(args, DEFAULT_ARGUMENTS)

    def test_get_args_with_short_command_args(self):
        sys.argv = SHORT_COMMAND_ARGS
        args = self.scan_controller.get_args()
        # check the value parsed by short arguments
        self.check_args_values(args, SHORT_FLAGS_ARGUMENTS)

    def test_get_args_with_full_command_args(self):
        sys.argv = LONG_COMMAND_ARGS
        args = self.scan_controller.get_args()
        # check the value parsed by long arguments
        self.check_args_values(args, ARGUMENTS_FULL)

    def test_get_args_with_full_command_args_clear_all(self):
        sys.argv = LONG_COMMAND_ARGS_CLEAR_ALL
        args = self.scan_controller.get_args()
        # check the value parsed by long arguments
        self.check_args_values(args, ARGUMENTS_FULL_CLEAR_ALL)

    def test_get_args_with_full_command_args_inventory_only(self):
        sys.argv = LONG_COMMAND_ARGS_INVENTORY_ONLY
        args = self.scan_controller.get_args()
        # check the value parsed by long arguments
        self.check_args_values(args, ARGUMENTS_FULL_INVENTORY_ONLY)

    def test_get_args_with_full_command_args_links_only(self):
        sys.argv = LONG_COMMAND_ARGS_LINKS_ONLY
        args = self.scan_controller.get_args()
        # check the value parsed by long arguments
        self.check_args_values(args, ARGUMENTS_FULL_LINKS_ONLY)

    def test_get_args_with_full_command_args_cliques_only(self):
        sys.argv = LONG_COMMAND_ARGS_CLIQUES_ONLY
        args = self.scan_controller.get_args()
        # check the value parsed by long arguments
        self.check_args_values(args, ARGUMENTS_FULL_CLIQUES_ONLY)

    def side_effect(self, key, default):
        if key in FORM.keys():
            return FORM[key]
        else:
            return default

    def check_plan_values(self, plan, scanner_type, obj_id,
                          child_type, child_id):
        self.assertEqual(scanner_type, plan.scanner_type,
                         'The scanner class is wrong')
        self.assertEqual(child_type, plan.child_type,
                         'The child type is wrong')
        self.assertEqual(child_id, plan.child_id,
                         'The child id is wrong')
        self.assertEqual(obj_id, plan.object_id, 'The object is wrong')

    def test_prepare_scan_plan(self):
        scan_plan = ScanPlan(SCAN_ENV_PLAN_TO_BE_PREPARED)
        plan = self.scan_controller.prepare_scan_plan(scan_plan)
        self.check_plan_values(plan, SCANNER_TYPE_FOR_ENV,
                               OBJ_ID_FOR_ENV, CHILD_TYPE_FOR_ENV,
                               CHILD_ID_FOR_ENV)

    def test_prepare_scan_region_plan(self):
        original_get_by_id = self.inv.get_by_id
        self.inv.get_by_id = MagicMock(return_value=REGIONS_FOLDER)

        self.scan_controller.inv = self.inv
        scan_plan = ScanPlan(SCAN_REGION_PLAN_TO_BE_PREPARED)
        plan = self.scan_controller.prepare_scan_plan(scan_plan)

        self.check_plan_values(plan, SCANNER_TYPE_FOR_REGION,
                               OBJ_ID_FOR_REGION, CHILD_TYPE_FOR_REGION,
                               CHILD_ID_FOR_REGION)
        self.inv.get_by_id = original_get_by_id

    def test_prepare_scan_region_folder_plan(self):
        scan_plan = ScanPlan(SCAN_REGION_FOLDER_PLAN_TO_BE_PREPARED)
        plan = self.scan_controller.prepare_scan_plan(scan_plan)
        self.check_plan_values(plan, SCANNER_CLASS_FOR_REGION_FOLDER,
                               OBJ_ID_FOR_REGION_FOLDER,
                               CHILD_TYPE_FOR_REGION_FOLDER,
                               CHILD_ID_FOR_REGION_FOLDER)

    def check_scan_method_calls(self, mock, count):
        if count:
            self.assertTrue(mock.called)
        else:
            mock.assert_not_called()

    def check_scan_counts(self, run_scan_count, scan_links_count,
                          scan_cliques_count, deploy_monitoring_setup_count):
        self.check_scan_method_calls(Scanner.scan, run_scan_count)
        self.check_scan_method_calls(Scanner.scan_links, scan_links_count)
        self.check_scan_method_calls(Scanner.scan_cliques, scan_cliques_count)
        self.check_scan_method_calls(Scanner.deploy_monitoring_setup,
                                     deploy_monitoring_setup_count)

    def prepare_scan_mocks(self):
        self.load_link_finders_metadata = Scanner.load_scanners_metadata
        self.load_scanners_metadata = Scanner.load_scanners_metadata
        self.scan = Scanner.scan
        self.scan_links = Scanner.scan_links
        self.scan_cliques = Scanner.scan_cliques
        self.deploy_monitoring_setup = Scanner.deploy_monitoring_setup

        Scanner.load_link_finders_metadata = MagicMock()
        Scanner.load_scanners_metadata = MagicMock()
        Scanner.scan = MagicMock()
        Scanner.scan_links = MagicMock()
        Scanner.scan_cliques = MagicMock()
        Scanner.deploy_monitoring_setup = MagicMock()

    def reset_methods(self):
        Scanner.load_link_finders_metadata = self.load_link_finders_metadata
        Scanner.load_scanners_metadata = self.load_scanners_metadata
        Scanner.scan = self.scan
        Scanner.scan_links = self.scan_links
        Scanner.scan_cliques = self.scan_cliques
        Scanner.deploy_monitoring_setup = self.deploy_monitoring_setup

    def test_scan(self):
        self.scan_controller.get_args = MagicMock()
        InventoryMgr.is_feature_supported = MagicMock(return_value=False)
        plan = self.scan_controller.prepare_scan_plan(ScanPlan(SCAN_ENV_PLAN_TO_BE_PREPARED))
        self.scan_controller.get_scan_plan = MagicMock(return_value=plan)
        self.prepare_scan_mocks()

        self.scan_controller.run()
        self.check_scan_counts(1, 1, 1, 0)
        self.reset_methods()

    def test_scan_with_monitoring_setup(self):
        self.scan_controller.get_args = MagicMock()
        InventoryMgr.is_feature_supported = MagicMock(return_value=True)
        plan = self.scan_controller.prepare_scan_plan(ScanPlan(SCAN_ENV_PLAN_TO_BE_PREPARED))
        self.scan_controller.get_scan_plan = MagicMock(return_value=plan)
        self.prepare_scan_mocks()

        self.scan_controller.run()
        self.check_scan_counts(1, 1, 1, 1)
        self.reset_methods()

    def test_scan_with_inventory_only(self):
        self.scan_controller.get_args = MagicMock()
        scan_plan = ScanPlan(SCAN_ENV_INVENTORY_ONLY_PLAN_TO_BE_PREPARED)
        plan = self.scan_controller.prepare_scan_plan(scan_plan)
        self.scan_controller.get_scan_plan = MagicMock(return_value=plan)
        self.prepare_scan_mocks()

        self.scan_controller.run()
        self.check_scan_counts(1, 0, 0, 0)
        self.reset_methods()

    def test_scan_with_links_only(self):
        self.scan_controller.get_args = MagicMock()
        scan_plan = ScanPlan(SCAN_ENV_LINKS_ONLY_PLAN_TO_BE_PREPARED)
        plan = self.scan_controller.prepare_scan_plan(scan_plan)
        self.scan_controller.get_scan_plan = MagicMock(return_value=plan)
        self.prepare_scan_mocks()

        self.scan_controller.run()
        self.check_scan_counts(0, 1, 0, 0)
        self.reset_methods()

    def test_scan_with_cliques_only(self):
        self.scan_controller.get_args = MagicMock()
        scan_plan = ScanPlan(SCAN_ENV_CLIQUES_ONLY_PLAN_TO_BE_PREPARED)
        plan = self.scan_controller.prepare_scan_plan(scan_plan)
        self.scan_controller.get_scan_plan = MagicMock(return_value=plan)
        self.prepare_scan_mocks()

        self.scan_controller.run()
        self.check_scan_counts(0, 0, 1, 0)
        self.reset_methods()
