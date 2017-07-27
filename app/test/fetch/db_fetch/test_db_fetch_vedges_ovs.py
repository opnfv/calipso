from discover.fetchers.db.db_fetch_vedges_ovs import DbFetchVedgesOvs
from test.fetch.test_fetch import TestFetch
from test.fetch.db_fetch.test_data.db_fetch_vedges_ovs import *
from unittest.mock import MagicMock


class TestDbFetchVedgesOvs(TestFetch):

    def setUp(self):
        self.configure_environment()
        self.fetcher = DbFetchVedgesOvs()
        self.fetcher.set_env(self.env)

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

        self.fetcher.get_objects_list_for_id = MagicMock(return_value=objects_from_db)
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
                         "Can' t get correct ports info from dpctl lines")

    def test_fetch_port_tags_from_vsctl(self):
        ports = self.fetcher.fetch_port_tags_from_vsctl(VSCTL_LINES,
                                                        FETCH__PORT_TAGS_INPUT)
        self.assertEqual(ports, FETCH_PORT_TAGS_RESULT,
                         "Can't fetch tag from vsctl")

    def test_get_overlay_tunnels(self):
        results = self.fetcher.get_overlay_tunnels(DOC_TO_GET_OVERLAY,
                                                   VSCTL_LINES)
        self.assertEqual(results, TUNNEL_PORTS)
