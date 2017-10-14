###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from api.validation import regex
from api.validation.data_validate import DataValidate
from api.responders.responder_base import ResponderBase
from bson.objectid import ObjectId
from datetime import datetime
from utils.constants import EnvironmentFeatures
from utils.inventory_mgr import InventoryMgr


class EnvironmentConfigs(ResponderBase):

    COLLECTION = "environments_config"
    ID = "name"
    PROJECTION = {
        ID: True,
        "_id": False,
        "name": True,
        "distribution": True
    }
    CONFIGURATIONS_NAMES = ["mysql", "OpenStack", "CLI", "AMQP",
                            "Monitoring", "NFV_provider", "ACI"]
    OPTIONAL_CONFIGURATIONS_NAMES = ["AMQP", "Monitoring",
                                     "NFV_provider", "ACI"]

    def __init__(self):
        super().__init__()

        self.provision_types = self.\
            get_constants_by_name("environment_provision_types")
        self.env_types = self.get_constants_by_name("env_types")
        self.monitoring_types = self.\
            get_constants_by_name("environment_monitoring_types")
        self.distributions = self.\
            get_constants_by_name("distributions")
        self.distribution_versions = self.\
            get_constants_by_name("distribution_versions")
        self.mechanism_drivers = self.\
            get_constants_by_name("mechanism_drivers")
        self.operational_values = self.\
            get_constants_by_name("environment_operational_status")
        self.type_drivers = self.\
            get_constants_by_name("type_drivers")

        self.CONFIGURATIONS_REQUIREMENTS = {
            "mysql": {
                "name": self.require(str, mandatory=True),
                "host": self.require(str,
                                     mandatory=True,
                                     validate=DataValidate.REGEX,
                                     requirement=[regex.IP, regex.HOSTNAME]),
                "pwd": self.require(str, mandatory=True),
                "port": self.require(int,
                                     mandatory=True,
                                     convert_to_type=True,
                                     validate=DataValidate.REGEX,
                                     requirement=regex.PORT),
                "user": self.require(str, mandatory=True)
            },
            "OpenStack": {
                "name": self.require(str, mandatory=True),
                "admin_token": self.require(str, mandatory=True),
                "host": self.require(str,
                                     mandatory=True,
                                     validate=DataValidate.REGEX,
                                     requirement=[regex.IP, regex.HOSTNAME]),
                "port": self.require(int,
                                     mandatory=True,
                                     convert_to_type=True,
                                     validate=DataValidate.REGEX,
                                     requirement=regex.PORT),
                "pwd": self.require(str, mandatory=True),
                "user": self.require(str, mandatory=True)
            },
            "CLI": {
                "name": self.require(str, mandatory=True),
                "host": self.require(str,
                                     mandatory=True,
                                     validate=DataValidate.REGEX,
                                     requirement=[regex.IP, regex.HOSTNAME]),
                "user": self.require(str, mandatory=True),
                "pwd": self.require(str),
                "key": self.require(str,
                                    validate=DataValidate.REGEX,
                                    requirement=regex.PATH)
            },
            "AMQP": {
                "name": self.require(str, mandatory=True),
                "host": self.require(str,
                                     mandatory=True,
                                     validate=DataValidate.REGEX,
                                     requirement=[regex.IP, regex.HOSTNAME]),
                "pwd": self.require(str, mandatory=True),
                "port": self.require(int,
                                     mandatory=True,
                                     convert_to_type=True,
                                     validate=DataValidate.REGEX,
                                     requirement=regex.PORT),
                "user": self.require(str, mandatory=True)
            },
            "Monitoring": {
                "name": self.require(str, mandatory=True),
                "config_folder": self.require(str,
                                              mandatory=True,
                                              validate=DataValidate.REGEX,
                                              requirement=regex.PATH),
                "provision": self.require(str,
                                          mandatory=True,
                                          validate=DataValidate.LIST,
                                          requirement=self.provision_types),
                "env_type": self.require(str,
                                         mandatory=True,
                                         validate=DataValidate.LIST,
                                         requirement=self.env_types),
                "api_port": self.require(int,
                                         mandatory=True,
                                         convert_to_type=True),
                "rabbitmq_pass": self.require(str, mandatory=True),
                "rabbitmq_user": self.require(str, mandatory=True),
                "rabbitmq_port": self.require(int,
                                              mandatory=True,
                                              convert_to_type=True,
                                              validate=DataValidate.REGEX,
                                              requirement=regex.PORT),
                "ssh_port": self.require(int,
                                         convert_to_type=True,
                                         validate=DataValidate.REGEX,
                                         requirement=regex.PORT),
                "ssh_user": self.require(str),
                "ssh_password": self.require(str),
                "server_ip": self.require(str,
                                          mandatory=True,
                                          validate=DataValidate.REGEX,
                                          requirement=[regex.IP, regex.HOSTNAME]),
                "server_name": self.require(str, mandatory=True),
                "type": self.require(str,
                                     mandatory=True,
                                     validate=DataValidate.LIST,
                                     requirement=self.monitoring_types)
            },
            "NFV_provider": {
                "name": self.require(str, mandatory=True),
                "host": self.require(str,
                                     mandatory=True,
                                     validate=DataValidate.REGEX,
                                     requirement=[regex.IP, regex.HOSTNAME]),
                "nfv_token": self.require(str, mandatory=True),
                "port": self.require(int,
                                     mandatory=True,
                                     convert_to_type=True,
                                     validate=DataValidate.REGEX,
                                     requirement=regex.PORT),
                "user": self.require(str, mandatory=True),
                "pwd": self.require(str, mandatory=True)
            },
            "ACI": {
                "name": self.require(str, mandatory=True),
                "host": self.require(str,
                                     mandatory=True,
                                     validate=DataValidate.REGEX,
                                     requirement=[regex.IP, regex.HOSTNAME]),
                "user": self.require(str, mandatory=True),
                "pwd": self.require(str, mandatory=True)
            }
        }
        self.AUTH_REQUIREMENTS = {
            "view-env": self.require(list, mandatory=True),
            "edit-env": self.require(list, mandatory=True)
        }

    def on_get(self, req, resp):
        self.log.debug("Getting environment config")
        filters = self.parse_query_params(req)

        filters_requirements = {
            "name": self.require(str),
            "distribution": self.require(str,
                                         validate=DataValidate.LIST,
                                         requirement=self.distributions),
            "distribution_version": self.require(str,
                                                 validate=DataValidate.LIST,
                                                 requirement=self.distribution_versions),
            "mechanism_drivers": self.require([str, list],
                                              validate=DataValidate.LIST,
                                              requirement=self.mechanism_drivers),
            "type_drivers": self.require(str,
                                         validate=DataValidate.LIST,
                                         requirement=self.type_drivers),
            "user": self.require(str),
            "listen": self.require(bool, convert_to_type=True),
            "scanned": self.require(bool, convert_to_type=True),
            "monitoring_setup_done": self.require(bool, convert_to_type=True),
            "operational": self.require(str,
                                        validate=DataValidate.LIST,
                                        requirement=self.operational_values),
            "page": self.require(int, convert_to_type=True),
            "page_size": self.require(int, convert_to_type=True)
        }

        self.validate_query_data(filters, filters_requirements)
        page, page_size = self.get_pagination(filters)

        query = self.build_query(filters)

        if self.ID in query:
            environment_config = self.get_object_by_id(self.COLLECTION, query,
                                                       [ObjectId, datetime], self.ID)
            self.set_successful_response(resp, environment_config)
        else:
            objects_ids = self.get_objects_list(self.COLLECTION, query,
                                                page, page_size, self.PROJECTION)
            self.set_successful_response(resp, {'environment_configs': objects_ids})

    def build_query(self, filters):
        query = {}
        filters_keys = ["name", "distribution", "distribution_version",
                        "type_drivers", "user", "listen",
                        "monitoring_setup_done", "scanned", "operational"]
        self.update_query_with_filters(filters, filters_keys, query)
        mechanism_drivers = filters.get("mechanism_drivers")
        if mechanism_drivers:
            if type(mechanism_drivers) != list:
                mechanism_drivers = [mechanism_drivers]
            query['mechanism_drivers'] = {'$all': mechanism_drivers}

        return query

    def on_post(self, req, resp):
        self.log.debug("Creating a new environment config")

        error, env_config = self.get_content_from_request(req)
        if error:
            self.bad_request(error)

        environment_config_requirement = {
            "app_path": self.require(str, mandatory=True),
            "configuration": self.require(list, mandatory=True),
            "distribution": self.require(str,
                                         mandatory=True,
                                         validate=DataValidate.LIST,
                                         requirement=self.distributions),
            "distribution_version": self.require(str, mandatory=True),
            "listen": self.require(bool,
                                   mandatory=True,
                                   convert_to_type=True),
            "user": self.require(str),
            "mechanism_drivers": self.require(list,
                                              mandatory=True,
                                              validate=DataValidate.LIST,
                                              requirement=self.mechanism_drivers),
            "name": self.require(str, mandatory=True),
            "operational": self.require(str,
                                        mandatory=True,
                                        convert_to_type=True,
                                        validate=DataValidate.LIST,
                                        requirement=self.operational_values),
            "scanned": self.require(bool, convert_to_type=True),
            "last_scanned": self.require(str),
            "type": self.require(str, mandatory=True),
            "type_drivers": self.require(str,
                                         mandatory=True,
                                         validate=DataValidate.LIST,
                                         requirement=self.type_drivers),
            "enable_monitoring": self.require(bool, convert_to_type=True),
            "monitoring_setup_done": self.require(bool, convert_to_type=True),
            "auth": self.require(dict),
            "aci_enabled": self.require(bool, convert_to_type=True)
        }
        self.validate_query_data(env_config,
                                 environment_config_requirement,
                                 can_be_empty_keys=["last_scanned"]
                                 )
        self.check_and_convert_datetime("last_scanned", env_config)
        # validate the configurations
        configurations = env_config['configuration']
        config_validation = self.validate_environment_config(configurations)

        if not config_validation['passed']:
            self.bad_request(config_validation['error_message'])

        err_msg = self.validate_env_config_with_supported_envs(env_config)
        if err_msg:
            self.bad_request(err_msg)

        err_msg = self.validate_env_config_with_constraints(env_config)
        if err_msg:
            self.bad_request(err_msg)

        if "auth" in env_config:
            err_msg = self.validate_data(env_config.get("auth"),
                                         self.AUTH_REQUIREMENTS)
            if err_msg:
                self.bad_request("auth error: " + err_msg)

        if "scanned" not in env_config:
            env_config["scanned"] = False

        self.write(env_config, self.COLLECTION)
        self.set_successful_response(resp,
                                     {"message": "created environment_config "
                                                 "for {0}"
                                                 .format(env_config["name"])},
                                     "201")

    def validate_environment_config(self, configurations,
                                    require_mandatory=True):
        configurations_of_names = {}
        validation = {"passed": True}
        if [config for config in configurations
            if 'name' not in config]:
            validation['passed'] = False
            validation['error_message'] = "configuration must have name"
            return validation

        unknown_configs = [config['name'] for config in configurations
                           if config['name'] not in self.CONFIGURATIONS_NAMES]
        if unknown_configs:
            validation['passed'] = False
            validation['error_message'] = 'Unknown configurations: {0}'. \
                format(' and '.join(unknown_configs))
            return validation

        for name in self.CONFIGURATIONS_NAMES:
            configs = self.get_configuration_by_name(name, configurations)
            if configs:
                if len(configs) > 1:
                    validation["passed"] = False
                    validation["error_message"] = "environment configurations can " \
                                                  "only contain one " \
                                                  "configuration for {0}".format(name)
                    return validation
                configurations_of_names[name] = configs[0]
            elif require_mandatory:
                if name not in self.OPTIONAL_CONFIGURATIONS_NAMES:
                    validation["passed"] = False
                    validation['error_message'] = "configuration for {0} " \
                                                  "is mandatory".format(name)
                    return validation

        for name, config in configurations_of_names.items():
            error_message = self.validate_configuration(name, config)
            if error_message:
                validation['passed'] = False
                validation['error_message'] = "{0} error: {1}".\
                    format(name, error_message)
                break
            if name is 'CLI':
                if 'key' not in config and 'pwd' not in config:
                    validation['passed'] = False
                    validation['error_message'] = 'CLI error: either key ' \
                                                  'or pwd must be provided'
        return validation

    def validate_env_config_with_supported_envs(self, env_config):
        # validate the environment config with supported environments
        matches = {
            'environment.distribution': env_config['distribution'],
            'environment.distribution_version':
                env_config['distribution_version'],
            'environment.type_drivers': env_config['type_drivers'],
            'environment.mechanism_drivers':
                {'$in': env_config['mechanism_drivers']}
        }

        err_prefix = 'configuration not accepted: '
        if not self.inv.is_feature_supported_in_env(matches,
                                                    EnvironmentFeatures.SCANNING):
            return err_prefix + 'scanning is not supported in this environment'

        configs = env_config['configuration']
        if not self.inv.is_feature_supported_in_env(matches,
                                                    EnvironmentFeatures.MONITORING) \
                and self.get_configuration_by_name('Monitoring', configs):
            return err_prefix + 'monitoring is not supported in this environment, ' \
                                'please remove the Monitoring configuration'

        if not self.inv.is_feature_supported_in_env(matches,
                                                    EnvironmentFeatures.LISTENING) \
                and self.get_configuration_by_name('AMQP', configs):
            return err_prefix + 'listening is not supported in this environment, ' \
                                'please remove the AMQP configuration'

        return None

    def validate_env_config_with_constraints(self, env_config):
        if env_config['listen'] and \
                not self.get_configuration_by_name('AMQP', env_config['configuration']):
            return 'configuration not accepted: ' \
                   'must provide AMQP configuration to listen the environment'

    def get_configuration_by_name(self, name, configurations):
        return [config for config in configurations if config['name'] == name]

    def validate_configuration(self, name, configuration):
        return self.validate_data(configuration,
                                  self.CONFIGURATIONS_REQUIREMENTS[name])
