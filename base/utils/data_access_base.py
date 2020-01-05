###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import os
import tempfile

from base.utils.config_file import ConfigFile
from base.utils.logging.console_logger import ConsoleLogger
from base.utils.logging.file_logger import FileLogger
from base.utils.logging.logger import Logger
from base.utils.util import read_environment_variables


class DataAccessBase:
    class ConfigSource:
        ENV = 1
        FILE = 2
        DEFAULT_FILE = 3

    LOG_FILENAME = 'data_access_base.log'
    DEFAULT_LOG_DIR = os.path.join(os.path.abspath("."), LOG_FILENAME)
    TMP_DIR = tempfile.gettempdir()
    REQUIRED_ENV_VARIABLES = {}
    OPTIONAL_ENV_VARIABLES = {}

    default_conf_file = '/local_dir/data_access_base.conf'
    config_file = None
    config_source = None

    def __init__(self):
        super().__init__()
        self.log = ConsoleLogger()
        self.log = self.set_log()

    @staticmethod
    def set_config_file(_conf_file):
        DataAccessBase.config_file = _conf_file

    @staticmethod
    def get_logger(directory):
        if not os.path.isdir(directory):
            ConsoleLogger().warning('Can\'t use inexistent directory {} '
                                    'for logging'.format(directory))
            return None
        log_file = os.path.join(directory, DataAccessBase.LOG_FILENAME)

        try:
            log = FileLogger(log_file)
            return log
        except OSError as e:
            ConsoleLogger().warning("Couldn't use file {} for logging. "
                                    "Error: {}".format(log_file, e))
            return None

    def set_log(self) -> Logger:
        dirs_to_try = [
            FileLogger.LOG_DIRECTORY,
            self.DEFAULT_LOG_DIR,
            self.TMP_DIR
        ]
        for directory in dirs_to_try:
            log = self.get_logger(directory)
            if log:
                return log

        self.log.error('Unable to open log file {} in any of '
                       'the following directories: {}'
                       .format(self.LOG_FILENAME, ', '.join(dirs_to_try)))
        self.log.error('will use console logger for {} logging'.format(self.__class__.__name__))
        return self.log

    @classmethod
    def read_config_from_env_vars(cls):
        try:
            return read_environment_variables(
                required=cls.REQUIRED_ENV_VARIABLES,
                optional=cls.OPTIONAL_ENV_VARIABLES
            )
        except ValueError:
            return {}

    @classmethod
    def _get_connection_parameters(cls):
        config_params = cls.read_config_from_env_vars()
        if config_params:
            cls.config_source = cls.ConfigSource.ENV
            return config_params

        if cls.config_file:
            config_file_path = cls.config_file
            cls.config_source = cls.ConfigSource.FILE
        else:
            config_file_path = cls.default_conf_file
            cls.config_source = cls.ConfigSource.DEFAULT_FILE

        # read connection parameters from config file
        config_file = ConfigFile(config_file_path)
        config_params = config_file.read_config()
        return config_params

    def get_connection_parameters(self):
        try:
            return self._get_connection_parameters()
        except Exception as e:
            self.log.exception(e)
            raise

    @classmethod
    def get_source_text(cls):
        if not cls.config_source:
            return "{} not initialized".format(cls.__name__)
        template = "{} configuration taken from".format(cls.__name__)
        if cls.config_source == DataAccessBase.ConfigSource.ENV:
            return "{} environment variables".format(template)
        if cls.config_source == DataAccessBase.ConfigSource.FILE:
            return "{} file: {}".format(template, cls.config_file)
        if cls.config_source == DataAccessBase.ConfigSource.DEFAULT_FILE:
            return "{} default file: {}".format(template, cls.default_conf_file)

    def get_connection_text(self):
        return self.get_source_text()
