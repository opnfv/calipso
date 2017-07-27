import time

from discover.fetchers.cli.cli_access import CliAccess
from test.fetch.cli_fetch.test_data.cli_access import *
from test.fetch.test_fetch import TestFetch
from unittest.mock import MagicMock, patch
from utils.ssh_conn import SshConn


class TestCliAccess(TestFetch):

    def setUp(self):
        self.configure_environment()
        self.cli_access = CliAccess()

    @patch("utils.ssh_conn.SshConn.exec")
    def check_run_result(self, is_gateway_host,
                         enable_cache,
                         cached_command_result, exec_result,
                         expected_result, err_msg,
                         ssh_con_exec):
        # mock cached commands
        if not is_gateway_host:
            self.cli_access.cached_commands = {
                NON_GATEWAY_CACHED_COMMAND: cached_command_result
            }
        else:
            self.cli_access.cached_commands = {
                GATEWAY_CACHED_COMMAND: cached_command_result
            }
        original_is_gateway_host = SshConn.is_gateway_host
        SshConn.is_gateway_host = MagicMock(return_value=is_gateway_host)
        ssh_con_exec.return_value = exec_result
        result = self.cli_access.run(COMMAND, COMPUTE_HOST_ID,
                                     on_gateway=False, enable_cache=enable_cache)
        self.assertEqual(result, expected_result, err_msg)

        # reset the cached commands after testing
        self.cli_access.cached_commands = {}
        # reset method
        SshConn.is_gateway_host = original_is_gateway_host

    def test_run(self):
        curr_time = time.time()
        test_cases = [
            {
                "is_gateway_host": True,
                "enable_cache": False,
                "cached_command_result": None,
                "exec_result": RUN_RESULT,
                "expected_result": RUN_RESULT,
                "err_msg": "Can't get the " +
                           "result of the command"
            },
            {
                "is_gateway_host": True,
                "enable_cache": True,
                "cached_command_result": {
                    "timestamp": curr_time,
                    "result": CACHED_COMMAND_RESULT
                },
                "exec_result": None,
                "expected_result": CACHED_COMMAND_RESULT,
                "err_msg": "Can't get the cached " +
                           "result of the command " +
                           "when the host is a gateway host"
            },
            {
                "is_gateway_host": False,
                "enable_cache": True,
                "cached_command_result": {
                    "timestamp": curr_time,
                    "result": CACHED_COMMAND_RESULT
                },
                "exec_result": None,
                "expected_result": CACHED_COMMAND_RESULT,
                "err_msg": "Can't get the cached " +
                           "result of the command " +
                           "when the host is not a gateway host"
            },
            {
                "is_gateway_host": True,
                "enable_cache": True,
                "cached_command_result": {
                    "timestamp": curr_time - self.cli_access.cache_lifetime,
                    "result": CACHED_COMMAND_RESULT
                },
                "exec_result": RUN_RESULT,
                "expected_result": RUN_RESULT,
                "err_msg": "Can't get the result " +
                           "of the command when the cached result expired " +
                           "and the host is a gateway host"
            },
            {
                "is_gateway_host": False,
                "enable_cache": True,
                "cached_command_result": {
                    "timestamp": curr_time - self.cli_access.cache_lifetime,
                    "result": CACHED_COMMAND_RESULT
                },
                "exec_result": RUN_RESULT,
                "expected_result": RUN_RESULT,
                "err_msg": "Can't get the result " +
                           "of the command when the cached result expired " +
                           "and the host is a not gateway host"
            }
        ]

        for test_case in test_cases:
            self.check_run_result(test_case["is_gateway_host"],
                                  test_case["enable_cache"],
                                  test_case["cached_command_result"],
                                  test_case["exec_result"],
                                  test_case["expected_result"],
                                  test_case["err_msg"])

    def test_run_fetch_lines(self):
        original_run = self.cli_access.run
        self.cli_access.run = MagicMock(return_value=RUN_RESULT)

        result = self.cli_access.run_fetch_lines(COMMAND, COMPUTE_HOST_ID)

        self.assertEqual(result, FETCH_LINES_RESULT,
                         "Can't get correct result of the command line")
        self.cli_access.run = original_run

    def test_run_fetch_lines_with_empty_command_result(self):
        original_run = self.cli_access.run
        self.cli_access.run = MagicMock(return_value="")

        result = self.cli_access.run_fetch_lines(COMMAND, COMPUTE_HOST_ID)
        self.assertEqual(result, [], "Can't get [] when the command " +
                                     "result is empty")
        self.cli_access.run = original_run

    def test_merge_ws_spillover_lines(self):
        fixed_lines = self.cli_access.merge_ws_spillover_lines(LINES_FOR_FIX)
        self.assertEqual(fixed_lines, FIXED_LINES, "Can't merge the " +
                                                   "ws-separated spillover lines")

    def test_parse_line_with_ws(self):
        parse_line = self.cli_access.parse_line_with_ws(LINE_FOR_PARSE, HEADERS)
        self.assertEqual(parse_line, PARSED_LINE, "Can't parse the line with ws")

    def test_parse_cmd_result_with_whitespace(self):
        result = self.cli_access.parse_cmd_result_with_whitespace(FIXED_LINES,
                                                                  HEADERS,
                                                                  remove_first=False)
        self.assertEqual(result, PARSED_CMD_RESULT,
                         "Can't parse the cmd result with whitespace")
