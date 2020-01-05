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

import copy

from scan.fetchers.db.db_fetch_vedges_ovs import DbFetchVedgesOvs
from scan.test.fetch.db_fetch.test_data.db_fetch_vedges_ovs import *
from scan.test.fetch.test_fetch import TestFetch


class TestDbFetchVedgesOvs(TestFetch):

    def setUp(self):
        super().setUp()
        self.configure_environment()
        self.fetcher = DbFetchVedgesOvs()
        self.fetcher.set_env(self.env)
        self.original_inv_set = self.fetcher.inv.set
        self.fetcher.inv.set = MagicMock()

    def tearDown(self):
        super().tearDown()
        self.fetcher.inv.set = self.original_inv_set

    def check_get_result(self,
                         objects_from_db, host,
                         vsctl_lines, ports, tunnel_ports,
                         expected_result, err_msg):
        # store original methods
        original_get_objects_list_by_id = self.fetcher.get_objects_list_for_id
        original_get_by_id = self.fetcher.inv.get_by_id
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        original_fetch_ports = self.fetcher.fetch_ports
        original_get_overlay_tunnels = self.fetcher.get_overlay_tunnels

        self.fetcher.get_objects_list_for_id = \
            MagicMock(return_value=objects_from_db)
        self.fetcher.inv.get_by_id = MagicMock(return_value=host)
        self.fetcher.run_fetch_lines = MagicMock(return_value=vsctl_lines)
        self.fetcher.fetch_ports = MagicMock(return_value=ports)
        self.fetcher.get_overlay_tunnels = MagicMock(return_value=tunnel_ports)

        results = self.fetcher.get(VEDGES_FOLDER_ID)
        self.assertEqual(results, expected_result, err_msg)

        # restore methods
        self.fetcher.get_objects_list_for_id = original_get_objects_list_by_id
        self.fetcher.inv.get_by_id = original_get_by_id
        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.fetcher.fetch_ports = original_fetch_ports
        self.fetcher.get_overlay_tunnels = original_get_overlay_tunnels

    def test_get(self):
        test_cases = [
            {
                "objects_from_db": OBJECTS_FROM_DB,
                "host": HOST,
                "vsctl_lines": "",
                "ports": PORTS,
                "tunnel_ports": TUNNEL_PORTS,
                "expected_result": GET_RESULTS,
                "err_msg": "Can't get correct vedges"
            },
            {
                "objects_from_db": OBJECTS_FROM_DB,
                "host": [],
                "vsctl_lines": "",
                "ports": {},
                "tunnel_ports": [],
                "expected_result": [],
                "err_msg": "Can't get [] when the host " +
                           "doesn't exist"
            },
            {
                "objects_from_db": OBJECTS_FROM_DB,
                "host": HOST_WITHOUT_REQUIRED_HOST_TYPES,
                "vsctl_lines": "",
                "ports": {},
                "tunnel_ports": [],
                "expected_result": [],
                "err_msg": "Can't get [] when the host " +
                           "doesn't have required host types"
            }
        ]
        for test_case in test_cases:
            self.check_get_result(test_case["objects_from_db"],
                                  test_case["host"],
                                  test_case["vsctl_lines"],
                                  test_case["ports"],
                                  test_case["tunnel_ports"],
                                  test_case["expected_result"],
                                  test_case["err_msg"])

    def test_fetch_ports_from_dpctl(self):
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        self.fetcher.run_fetch_lines = MagicMock(return_value=DPCTL_LINES)

        results = self.fetcher.fetch_ports_from_dpctl(HOST['id'])
        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.assertEqual(results, DPCTL_RESULTS,
                         "Can't get correct ports info from dpctl lines")

    def test_fetch_port_tags_from_vsctl(self):
        ports = self.fetcher.fetch_port_tags_from_vsctl(VSCTL_LINES,
                                                        FETCH__PORT_TAGS_INPUT)
        self.assertEqual(ports, FETCH_PORT_TAGS_RESULT,
                         "Can't fetch tag from vsctl")

    def test_get_overlay_tunnels(self):
        results = self.fetcher.get_overlay_tunnels(DOC_TO_GET_OVERLAY,
                                                   VSCTL_LINES)
        self.assertEqual(results, TUNNEL_PORTS)

    @staticmethod
    def get_test_pnic_for_interface_mirantis(search: dict,
                                             get_single: bool=True):
        if not get_single:
            # we're only supposed to get calls with get_single == True
            return []
        return PNICS_MIRANTS.get(search.get('name'), {})

    @staticmethod
    def get_test_pnic_for_interface(search: dict,
                                    get_single: bool=True):
        if not get_single:
            # we're only supposed to get calls with get_single == True
            return []
        return PNICS.get(search.get('name'), {})

    @staticmethod
    def get_expected_results_for_get_pnics(test_pnics: dict, ports: dict,
                                           ifaces_names: list) -> dict:
        expected_results = {}
        for p in test_pnics.values():
            if p.get("name") not in ifaces_names:
                continue
            p1 = copy.deepcopy(p)
            name = p1["name"]
            port = ports[name]
            p1["port_id"] = port["id"]
            expected_results[name] = p1
        return expected_results

    def test_get_pnics(self):
        expected_results = \
            self.get_expected_results_for_get_pnics(PNICS_MIRANTS,
                                                    VEDGE_MIRANTIS["ports"],
                                                    LIST_IFACES_NAMES_MIRANTIS)
        self.check_get_pnics_for_dist(VEDGE_MIRANTIS,
                                      LIST_IFACES_LINES_MIRANTIS,
                                      LIST_IFACES_NAMES_MIRANTIS,
                                      expected_results,
                                      self.get_test_pnic_for_interface_mirantis,
                                      self.fetcher.MIRANTIS_DIST,
                                      ver="6.0",
                                      msg="Incorrect get_pnics result "
                                          "(Mirantis)")
        expected_results = \
            self.get_expected_results_for_get_pnics(PNICS,
                                                    VEDGE["ports"],
                                                    LIST_IFACES_NAMES)
        self.check_get_pnics_for_dist(VEDGE,
                                      LIST_IFACES_LINES,
                                      LIST_IFACES_NAMES,
                                      expected_results,
                                      self.get_test_pnic_for_interface,
                                      ANOTHER_DIST,
                                      msg="Incorrect get_pnics result")

    def check_get_pnics_for_dist(self, test_vedge,
                                 ifaces_list_output, ifaces_list_clear,
                                 expected_results,
                                 pnic_find_func,
                                 dist, ver=None, msg=None):
        self.fetcher.configuration.environment = {
            "distribution": dist,
            "distribution_version": ver
        }
        original_run_fetch_lines = self.fetcher.run_fetch_lines
        self.fetcher.run_fetch_lines = \
            MagicMock(return_value=ifaces_list_output)
        original_find_items = self.fetcher.inv.find_items
        self.fetcher.inv.find_items = pnic_find_func
        vedge = copy.deepcopy(test_vedge)
        results = self.fetcher.get_pnics(vedge)
        self.fetcher.run_fetch_lines = original_run_fetch_lines
        self.fetcher.inv.find_items = original_find_items
        self.assertTrue(vedge.get("pnic") in ifaces_list_clear)
        self.assertEqual(results, expected_results, msg)
