###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json

from api.responders.resource.environment_configs import EnvironmentConfigs
from test.api.responders_test.test_data import base
from test.api.responders_test.test_data.base import CONSTANTS_BY_NAMES
from test.api.test_base import TestBase
from test.api.responders_test.test_data import environment_configs
from utils.constants import EnvironmentFeatures
from utils.inventory_mgr import InventoryMgr
from unittest.mock import patch


class TestEnvironmentConfigs(TestBase):

    @patch(base.RESPONDER_BASE_READ)
    def test_get_environment_configs_list(self, read):
        self.validate_get_request(environment_configs.URL,
                                  params={},
                                  mocks={read: environment_configs.ENV_CONFIGS},
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=environment_configs.
                                  ENV_CONFIGS_RESPONSE)

    def test_get_environment_configs_list_with_invalid_filters(self):
        self.validate_get_request(environment_configs.URL,
                                  params={"unknown": "unknown"},
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_environment_configs_list_with_name(self, read):
        mocks = {read: environment_configs.ENV_CONFIGS_WITH_SPECIFIC_NAME}
        self.validate_get_request(environment_configs.URL,
                                  params={"name": environment_configs.NAME},
                                  mocks=mocks,
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=environment_configs.
                                  ENV_CONFIGS_WITH_SPECIFIC_NAME[0])

    @patch(base.RESPONDER_BASE_READ)
    def test_get_environment_configs_list_with_unknown_name(self, read):
        self.validate_get_request(environment_configs.URL,
                                  params={
                                      "name": environment_configs.UNKNOWN_NAME
                                  },
                                  mocks={
                                      read: []
                                  },
                                  expected_code=base.NOT_FOUND_CODE)

    def test_get_environment_configs_list_with_wrong_distribution(self):
        self.validate_get_request(environment_configs.URL,
                                  params={
                                      "distribution":
                                          environment_configs.WRONG_DISTRIBUTION
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_environment_configs_list_with_wrong_distribution_version(self):
        self.validate_get_request(environment_configs.URL,
                                  params={
                                      "distribution_version":
                                          environment_configs.WRONG_DIST_VER
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_environment_configs_list_with_distribution(self, read):
        config = environment_configs.ENV_CONFIGS_WITH_SPECIFIC_DISTRIBUTION
        config_response = \
            environment_configs.ENV_CONFIGS_WITH_SPECIFIC_DISTRIBUTION_RESPONSE
        self.validate_get_request(environment_configs.URL,
                                  params={
                                      "distribution":
                                          environment_configs.
                                          CORRECT_DISTRIBUTION
                                  },
                                  mocks={read: config},
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=config_response)

    def test_get_environment_configs_list_with_wrong_mechanism_driver(self):
        config = environment_configs.WRONG_MECHANISM_DRIVER
        self.validate_get_request(environment_configs.URL,
                                  params={"mechanism_drivers": config},
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_environment_configs_list_with_mechanism_driver(self, read):
        mechanism = environment_configs.CORRECT_MECHANISM_DRIVER
        config = environment_configs.ENV_CONFIGS_WITH_SPECIFIC_MECHANISM_DRIVER
        config_response = environment_configs.\
            ENV_CONFIGS_WITH_SPECIFIC_MECHANISM_DRIVER_RESPONSE
        self.validate_get_request(environment_configs.URL,
                                  params={"mechanism_drivers": mechanism},
                                  mocks={read: config},
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=config_response)

    def test_get_environment_configs_list_with_wrong_type_driver(self):
        driver = environment_configs.WRONG_TYPE_DRIVER
        self.validate_get_request(environment_configs.URL,
                                  params={"type_drivers": driver},
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_environment_configs_list_with_type_driver(self, read):
        driver = environment_configs.CORRECT_TYPE_DRIVER
        config = environment_configs.ENV_CONFIGS_WITH_SPECIFIC_TYPE_DRIVER
        config_response = environment_configs.\
            ENV_CONFIGS_WITH_SPECIFIC_TYPE_DRIVER_RESPONSE
        self.validate_get_request(environment_configs.URL,
                                  params={"type_drivers": driver},
                                  mocks={read: config},
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=config_response
                                  )

    @patch(base.RESPONDER_BASE_READ)
    def test_get_environment_configs_list_with_user(self, read):
        config = environment_configs.ENV_CONFIGS_WITH_SPECIFIC_USER
        config_response = \
            environment_configs.ENV_CONFIGS_WITH_SPECIFIC_USER_RESPONSE
        self.validate_get_request(environment_configs.URL,
                                  params={"user": environment_configs.USER},
                                  mocks={read: config},
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=config_response)

    def test_get_environment_configs_list_with_non_bool_listen(self):
        self.validate_get_request(environment_configs.URL,
                                  params={"listen": environment_configs.
                                          NON_BOOL_LISTEN},
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_environment_configs_list_with_bool_listen(self, read):
        config = environment_configs.ENV_CONFIGS_WITH_SPECIFIC_LISTEN
        config_response = \
            environment_configs.ENV_CONFIGS_WITH_SPECIFIC_LISTEN_RESPONSE
        self.validate_get_request(environment_configs.URL,
                                  params={"listen": environment_configs.
                                          BOOL_LISTEN},
                                  mocks={read: config},
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=config_response)

    def test_get_environment_configs_list_with_non_bool_scanned(self):
        self.validate_get_request(environment_configs.URL,
                                  params={"scanned": environment_configs.
                                          NON_BOOL_SCANNED},
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_environment_configs_list_with_bool_scanned(self, read):
        config = environment_configs.ENV_CONFIGS_WITH_SPECIFIC_SCANNED
        config_response = \
            environment_configs.ENV_CONFIGS_WITH_SPECIFIC_SCANNED_RESPONSE
        self.validate_get_request(environment_configs.URL,
                                  params={"scanned": environment_configs.
                                          BOOL_SCANNED},
                                  mocks={read: config},
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=config_response
                                  )

    def test_get_env_configs_list_with_non_bool_monitoring_setup_done(self):
        self.validate_get_request(environment_configs.URL,
                                  params={"listen": environment_configs.
                                          NON_BOOL_MONITORING_SETUP_DONE},
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_environment_configs_list_with_bool_monitoring_setup_done(self,
                                                                          read):
        config = environment_configs.\
            ENV_CONFIGS_WITH_SPECIFIC_MONITORING_SETUP_DONE
        config_response = environment_configs.\
            ENV_CONFIGS_WITH_SPECIFIC_MONITORING_SETUP_DONE_RESPONSE
        self.validate_get_request(environment_configs.URL,
                                  params={"scanned": environment_configs.
                                          BOOL_MONITORING_SETUP_DONE},
                                  mocks={read: config},
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=config_response)

    def test_get_environment_configs_list_with_non_int_page(self):
        self.validate_get_request(environment_configs.URL,
                                  params={"page": base.NON_INT_PAGE},
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_environment_configs_list_with_int_page(self, read):
        config_response = environment_configs.ENV_CONFIGS_RESPONSE
        self.validate_get_request(environment_configs.URL,
                                  params={"page": base.INT_PAGE},
                                  mocks={read: environment_configs.ENV_CONFIGS},
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=config_response)

    def test_get_environment_configs_list_with_non_int_page_size(self):
        self.validate_get_request(environment_configs.URL,
                                  params={"page_size": base.NON_INT_PAGESIZE},
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_environment_configs_list_with_int_page_size(self, read):
        config_response = environment_configs.ENV_CONFIGS_RESPONSE
        self.validate_get_request(environment_configs.URL,
                                  params={"page_size": base.INT_PAGESIZE},
                                  mocks={read: environment_configs.ENV_CONFIGS},
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=config_response)

    def test_post_environment_config_without_app_path(self):
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          deleted_keys=["app_path"])
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_without_configuration(self):
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          deleted_keys=["configuration"])
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_without_distribution(self):
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          deleted_keys=["distribution"])
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_with_wrong_distribution(self):
        dist = environment_configs.WRONG_DISTRIBUTION
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          updates={"distribution": dist})
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_without_listen(self):
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          deleted_keys=["listen"])
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_with_wrong_listen(self):
        listen_val = environment_configs.NON_BOOL_LISTEN
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          updates={"listen": listen_val})
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_without_mechanism_driver(self):
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          deleted_keys=["mechanism_drivers"])
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_with_wrong_mechanism_driver(self):
        mechanism = environment_configs.WRONG_MECHANISM_DRIVER
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          updates={
                                             "mechanism_drivers": [mechanism]
                                          })
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_without_name(self):
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          deleted_keys=["name"])
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_without_operational(self):
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          deleted_keys=["operational"])
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_with_wrong_scanned(self):
        scanned_val = environment_configs.NON_BOOL_SCANNED
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          updates={"scanned": scanned_val})
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_with_wrong_last_scanned(self):
        scanned_val = base.WRONG_FORMAT_TIME
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          updates={"last_scanned": scanned_val})
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_without_type(self):
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          deleted_keys=["type"])
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_without_type_drivers(self):
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          deleted_keys=["type_drivers"])
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_with_wrong_type_drivers(self):
        driver = environment_configs.WRONG_TYPE_DRIVER
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          updates={"type_drivers": [driver]})
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_with_duplicate_configurations(self):
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG)
        test_data["configuration"].append({
            "name": "OpenStack"
        })
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_with_empty_configuration(self):
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG)
        test_data["configuration"].append({})
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_with_unknown_configuration(self):
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG)
        test_data["configuration"].append({
            "name": "Unknown configuration",
        })
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_without_required_configurations(self):
        for env_type in CONSTANTS_BY_NAMES["environment_types"]:
            required_conf_list = (
                EnvironmentConfigs.REQUIRED_CONFIGURATIONS_NAMES.get(env_type,
                                                                     [])
            )
            if required_conf_list:
                test_data = \
                    self.get_updated_data(environment_configs.ENV_CONFIG)
                test_data['environment_type'] = env_type
                test_data['configuration'] = [
                    c
                    for c in test_data['configuration']
                    if c['name'] != required_conf_list[0]
                ]

                self.validate_post_request(environment_configs.URL,
                                           body=json.dumps(test_data),
                                           expected_code=base.BAD_REQUEST_CODE)

    def test_post_environment_config_with_incomplete_configuration(self):
        test_data = self.get_updated_data(environment_configs.ENV_CONFIG,
                                          updates={
                                              "configuration": [{
                                                  "host": "10.56.20.239",
                                                  "name": "mysql",
                                                  "user": "root"
                                              }, {
                                                  "name": "OpenStack",
                                                  "host": "10.56.20.239",
                                              }, {
                                                  "host": "10.56.20.239",
                                                  "name": "CLI",
                                                  "user": "root"
                                              }]
                                          })
        self.validate_post_request(environment_configs.URL,
                                   body=json.dumps(test_data),
                                   expected_code=base.BAD_REQUEST_CODE)

    @staticmethod
    def mock_validate_env_config_with_supported_envs(scanning, monitoring,
                                                     listening):
        InventoryMgr.is_feature_supported_in_env = \
            lambda self, matches, feature: {
                EnvironmentFeatures.SCANNING: scanning,
                EnvironmentFeatures.MONITORING: monitoring,
                EnvironmentFeatures.LISTENING: listening
            }[feature]

    @patch(base.RESPONDER_BASE_WRITE)
    def test_post_environment_config(self, write):
        self.mock_validate_env_config_with_supported_envs(True, True, True)
        post_body = json.dumps(environment_configs.ENV_CONFIG)
        self.validate_post_request(environment_configs.URL,
                                   mocks={
                                       write: None
                                   },
                                   body=post_body,
                                   expected_code=base.CREATED_CODE)

    def test_post_unsupported_environment_config(self):
        test_cases = [
            {
                "scanning": False,
                "monitoring": True,
                "listening": True
            },
            {
                "scanning": True,
                "monitoring": False,
                "listening": True
            },
            {
                "scanning": True,
                "monitoring": True,
                "listening": False
            }
        ]
        mock_validate = self.mock_validate_env_config_with_supported_envs
        config = environment_configs.ENV_CONFIG
        for test_case in test_cases:
            mock_validate(test_case["scanning"], test_case["monitoring"],
                          test_case["listening"])
            self.validate_post_request(environment_configs.URL,
                                       body=json.dumps(config),
                                       expected_code=base.BAD_REQUEST_CODE)
