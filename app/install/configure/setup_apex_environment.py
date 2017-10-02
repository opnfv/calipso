#!/usr/bin/env python3
###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from abc import ABC
from logging.handlers import WatchedFileHandler
import argparse
import json
import logging
import re
import shlex
import subprocess
import sys


def run_command(cmd, raise_on_error=False) -> str:
    try:
        output = subprocess.check_output([cmd], shell=True)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        error_msg = 'Error running command: {}, output: {}'\
            .format(cmd, e.output.decode('utf-8'))
        if raise_on_error:
            raise RuntimeError(error_msg)
        return msg


class Logger(ABC):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'

    PROJECT_NAME = 'Calipso'

    levels = [DEBUG, INFO, WARNING, ERROR, CRITICAL]
    log_format = '%(asctime)s %(levelname)s: %(message)s'
    formatter = logging.Formatter(log_format)
    default_level = INFO

    def __init__(self, logger_name: str = PROJECT_NAME,
                 level: str = default_level):
        super().__init__()
        self.check_level(level)
        self.log = logging.getLogger(logger_name)
        logging.basicConfig(format=self.log_format,
                            level=level)
        self.log.propagate = False
        self.set_loglevel(level)
        self.env = None
        self.level = level

    def set_env(self, env):
        self.env = env

    @staticmethod
    def check_level(level):
        if level.upper() not in Logger.levels:
            raise ValueError('Invalid log level: {}. Supported levels: ({})'
                             .format(level, ", ".join(Logger.levels)))

    @staticmethod
    def get_numeric_level(loglevel):
        Logger.check_level(loglevel)
        numeric_level = getattr(logging, loglevel.upper(), Logger.default_level)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: {}'.format(loglevel))
        return numeric_level

    def set_loglevel(self, loglevel):
        # assuming loglevel is bound to the string value obtained from the
        # command line argument. Convert to upper case to allow the user to
        # specify --log=DEBUG or --log=debug
        numeric_level = self.get_numeric_level(loglevel)

        for handler in self.log.handlers:
            handler.setLevel(numeric_level)
        self.log.setLevel(numeric_level)
        self.level = loglevel

    def _log(self, level, message, *args, exc_info=False, **kwargs):
        self.log.log(level, message, *args, exc_info=exc_info, **kwargs)

    def debug(self, message, *args, **kwargs):
        self._log(logging.DEBUG, message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self._log(logging.INFO, message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self._log(logging.WARNING, message, *args, **kwargs)

    def warn(self, message, *args, **kwargs):
        self.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self._log(logging.ERROR, message, *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        self._log(logging.ERROR, message, exc_info=True, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self._log(logging.CRITICAL, message, *args, **kwargs)

    def add_handler(self, handler):
        handler_defined = handler.__class__ in map(lambda h: h.__class__,
                                                   self.log.handlers)

        if not handler_defined:
            handler.setLevel(self.level)
            handler.setFormatter(self.formatter)
            self.log.addHandler(handler)


class FileLogger(Logger):

    def __init__(self, log_file: str, level: str = Logger.default_level):
        super().__init__(logger_name="{}-File".format(self.PROJECT_NAME),
                         level=level)
        self.add_handler(WatchedFileHandler(log_file))


class ApexEnvironmentFetcher:

    DEFAULTS = {
        'logfile': '/home/calipso/log/apex_environment_fetch.log',
        'mongo_config': '/local_dir/calipso_mongo_access.conf',
        'config_dir': '/home/calipso/apex_setup_files',
        'install_db_dir': '/home/calipso/Calipso/app/install/db',
        'env': 'Apex-Euphrates',
        'loglevel': 'INFO',
        'git_repo': 'https://git.opnfv.org/calipso',
        'root': False
    }

    USER_NAME = 'calipso'
    USER_PWD = 'calipso_default'
    REPO_LOCAL_NAME = 'Calipso'
    INSTALLER = 'python3 app/install/calipso-installer.py --command start-all'
    CONFIG_FILE_NAME = 'apex-configuration.conf'
    ENV_CONFIG_FILE_NAME = 'environments_config.json'
    OVERCLOUDRC_FILE = 'overcloudrc.v3'
    SSH_DIR = '/home/calipso/.ssh'
    SSH_OPTIONS = '-q -o StrictHostKeyChecking=no'
    UNDERCLOUD_KEY_FILE = 'uc-id_rsa'
    UNDERCLOUD_PUBLIC_KEY_FILE = '{}/uc-id_rsa.pub'.format(SSH_DIR)
    OVERCLOUD_USER = 'heat-admin'
    OVERCLOUD_KEY_FILE = 'oc-id_rsa'
    MOUNT_SSH_DIR = '/local_dir/.ssh'
    OVERCLOUD_KEYSTONE_CONF = 'oc-keystone.conf'
    OVERCLOUD_ML2_CONF = 'overcloud_ml2_conf.ini'
    OVERCLOUD_RABBITMQ_CONF = 'overcloud_rabbitmq_conf.ini'

    def __init__(self):
        self.args = self.get_args()
        self.log = None
        self.config_file = '{}/{}'.format(self.args.config_dir,
                                          self.CONFIG_FILE_NAME)
        self.env_config_file = '{}/{}'.format(self.args.install_db_dir,
                                              self.ENV_CONFIG_FILE_NAME)
        self.undercloud_user = 'root'
        self.undercloud_host = '192.0.2.1'
        self.undercloud_key = '{}/{}'.format(self.SSH_DIR,
                                             self.UNDERCLOUD_KEY_FILE)
        self.overcloud_config_file = '{}/{}'\
            .format(self.args.config_dir, self.OVERCLOUDRC_FILE)
        self.overcloud_key = '{}/{}'.format(self.SSH_DIR,
                                            self.OVERCLOUD_KEY_FILE)
        self.overcloud_key_container = '{}/{}'.format(self.MOUNT_SSH_DIR,
                                                      self.OVERCLOUD_KEY_FILE)
        self.undercloud_ip = None
        self.overcloud_ip = None
        self.conf_lines = {}
        self.env_config = None

    def get_args(self):
        # try to read scan plan from command line parameters
        parser = argparse.ArgumentParser()
        parser.add_argument('-m', '--mongo_config', nargs='?', type=str,
                            default=self.DEFAULTS['mongo_config'],
                            help='name of config file ' +
                                 'with MongoDB server access details\n'
                                 '(Default: {})'
                                 .format(self.DEFAULTS['mongo_config']))
        parser.add_argument('-d', '--config_dir', nargs='?', type=str,
                            default=self.DEFAULTS['config_dir'],
                            help='path to directory with config data\n'
                                 '(Default: {})'
                            .format(self.DEFAULTS['config_dir']))
        parser.add_argument('-i', '--install_db_dir', nargs='?', type=str,
                            default=self.DEFAULTS['install_db_dir'],
                            help='path to directory with DB data\n'
                                 '(Default: {})'
                                 .format(self.DEFAULTS['install_db_dir']))
        parser.add_argument('-a', '--apex', nargs='?', type=str,
                            help='name of environment to Apex host')
        parser.add_argument('-e', '--env', nargs='?', type=str,
                            default=self.DEFAULTS['env'],
                            help='name of environment to create'
                                 '(Default: {})'
                                  .format(self.DEFAULTS['env']))
        parser.add_argument('-l', '--loglevel', nargs='?', type=str,
                            default=self.DEFAULTS['loglevel'],
                            help='logging level \n(default: "{}")'
                            .format(self.DEFAULTS['loglevel']))
        parser.add_argument('-f', '--logfile', nargs='?', type=str,
                            default=self.DEFAULTS['logfile'],
                            help='log file \n(default: "{}")'
                            .format(self.DEFAULTS['logfile']))
        parser.add_argument('-g', '--git', nargs='?', type=str,
                            help='URL to clone Git repository\n(default: {})'
                            .format(self.DEFAULTS['git_repo']),
                            default=self.DEFAULTS['git_repo'])
        parser.add_argument('--root', dest='root', action='store_true')
        parser.add_argument('--no-root', dest='root', action='store_false')
        parser.set_defaults(root=False)
        return parser.parse_args()

    @staticmethod
    def run_cmd(cmd: str ='', use_sudo=True, as_user=None):
        sudo_prefix = '' if not use_sudo \
            else 'sudo {} '.format(as_user if as_user else '')
        command = '{}{}'.format(sudo_prefix, cmd)
        output = run_command(cmd=command, raise_on_error=True)
        return output

    def get_undercloud_ip(self):
        output = self.run_cmd('ifconfig br-admin')
        lines = output.splitlines()
        if not lines or len(lines) < 2:
            self.log.error('Unable to feth inet address, output: {}'
                           .format(output))
            return
        inet_parts = lines[1].split()
        inet_address = inet_parts[1]
        return inet_address

    def get_overcloud_ip(self):
        with open('{}'.format(self.overcloud_config_file)) as rc_file:
            lines = rc_file.readlines()
            no_proxy_line = [l for l in lines if 'no_proxy=' in l]
            no_proxy_line = no_proxy_line[0]
            value = no_proxy_line[no_proxy_line.index('=')+2:]
            parts = value.strip().split(',')
            inet_address = parts[-1]
            return inet_address

    def set_ssh_dir(self):
        self.run_cmd('mkdir -p {}'.format(self.SSH_DIR))
        # will be used to access undercloud VM
        self.run_cmd('cp /root/.ssh/id_rsa {}'.format(self.undercloud_key))
        self.run_cmd('cp /root/.ssh/id_rsa.pub {}'
                     .format(self.UNDERCLOUD_PUBLIC_KEY_FILE))
        self.run_cmd('chown calipso.calipso {}/uc-id_rsa*'.format(self.SSH_DIR))
        self.copy_undercloud_file('/home/stack/.ssh/id_rsa',
                                  local_dir=self.SSH_DIR,
                                  local_name=self.OVERCLOUD_KEY_FILE)
        self.copy_undercloud_file('/home/stack/.ssh/id_rsa.pub',
                                  local_dir=self.SSH_DIR,
                                  local_name='oc-id_rsa.pub')
        self.run_cmd('chown calipso.calipso {}/oc-id_rsa*'.format(self.SSH_DIR))

    def copy_undercloud_file(self, file_path, local_dir=None, local_name=None):
        cmd = 'scp {} -i {} {}@{}:{} {}/{}' \
            .format(self.SSH_OPTIONS,
                    self.undercloud_key,
                    self.undercloud_user, self.undercloud_host,
                    file_path,
                    local_dir if local_dir else self.args.config_dir,
                    local_name if local_name else '')
        self.run_cmd(cmd)

    def copy_undercloud_conf_file(self, file_name, local_name=None):
        self.copy_undercloud_file('/home/stack/{}'.format(file_name),
                                  local_name)

    def get_undercloud_setup(self):
        self.copy_undercloud_conf_file('undercloud.conf')
        self.copy_undercloud_conf_file('opnfv-environment.yaml')
        self.copy_undercloud_conf_file('overcloudrc')
        self.copy_undercloud_conf_file('stackrc')
        self.copy_undercloud_conf_file('overcloudrc.v3')
        self.copy_undercloud_conf_file('deploy_command')
        self.copy_undercloud_conf_file('apex-undercloud-install.log')
        self.copy_undercloud_conf_file('undercloud-passwords.conf')
        self.copy_undercloud_file('/etc/keystone/keystone.conf',
                                  local_name='uc-keystone.conf')
        self.run_cmd('mkdir -p {}/deploy_logs'.format(self.args.config_dir))
        self.copy_undercloud_file('/home/stack/deploy_logs/*',
                                  local_name='deploy_logs/')

    def fetch_conf_file(self, file_name, target_file, lines_property=None):
        conf = \
            self.run_cmd('ssh -i {} {} {}@{} '
                         'sudo grep -v "^#" {}'
                         .format(self.overcloud_key,
                                 self.SSH_OPTIONS,
                                 self.OVERCLOUD_USER,
                                 self.overcloud_ip,
                                 file_name))
        conf_file_path = '{}/{}'.format(self.args.config_dir, target_file)
        if lines_property:
            self.conf_lines[lines_property] = conf.splitlines()
        with open(conf_file_path, 'w') as conf_file:
            conf_file.write(conf)

    def fetch_keystone_conf(self):
        self.fetch_conf_file('/etc/keystone/keystone.conf',
                             self.OVERCLOUD_KEYSTONE_CONF,
                             lines_property='keystone_conf')

    def fetch_ml2_conf(self):
        self.fetch_conf_file('/etc/neutron/plugins/ml2/ml2_conf.ini',
                             self.OVERCLOUD_ML2_CONF,
                             lines_property='ml2_conf')

    def fetch_rabbitmq_conf(self):
        self.fetch_conf_file('/etc/rabbitmq/rabbitmq.config',
                             self.OVERCLOUD_RABBITMQ_CONF,
                             lines_property='rabbitmq_conf')

    def copy_local_file_to_overcloud(self, local_file, remote_file_path,
                                     local_dir=None):
        source_dir = local_dir if local_dir else self.args.config_dir
        local_file_path = '{}/{}'.format(source_dir, local_file)
        cmd = 'scp {} -i {} {} {}@{}:{}' \
            .format(self.SSH_OPTIONS,
                    self.overcloud_key,
                    local_file_path,
                    self.OVERCLOUD_USER, self.overcloud_ip,
                    remote_file_path)
        self.run_cmd(cmd)

    def get_overcloud_keys(self):
        remote_ssh_dir = '/home/{}/.ssh'.format(self.OVERCLOUD_USER)
        remote_private_key = '{}/id_rsa'.format(remote_ssh_dir)
        self.copy_local_file_to_overcloud(self.OVERCLOUD_KEY_FILE,
                                          remote_private_key,
                                          local_dir=self.SSH_DIR)
        public_key = '{}.pub'.format(self.OVERCLOUD_KEY_FILE)
        remote_public_key = '{}/id_rsa.pub'.format(remote_ssh_dir)
        self.copy_local_file_to_overcloud(public_key, remote_public_key,
                                          local_dir=self.SSH_DIR)

    def get_overcloud_setup(self):
        self.get_overcloud_keys()
        self.fetch_keystone_conf()
        self.fetch_ml2_conf()
        self.fetch_rabbitmq_conf()

    def get_value_from_file(self, file_attr, attr, regex=None, separator='='):
        line_prefix = 'export ' if separator == '=' else ''
        prefix = '{}{}{}'.format(line_prefix, attr, separator)
        lines = self.conf_lines.get(file_attr, {})
        matches = [l for l in lines if l.startswith(prefix)]
        if not matches:
            self.log.error('failed to find attribute {}'.format(attr))
            return ''
        line = matches[0].strip()
        value = line[line.index(separator)+len(separator):]
        if not regex:
            return value
        matches = re.search(regex, value)
        if not matches:
            return ''
        match = matches.group(1)
        return match

    def get_value_from_rc_file(self, lines, attr, regex=None):
        return self.get_value_from_file(lines, attr, regex=regex)

    def get_api_config(self):
        with open('{}'.format(self.overcloud_config_file)) as rc_file:
            self.conf_lines['overcloudrc'] = rc_file.readlines()
        api_config = {
            'name': 'OpenStack',
            'host': self.overcloud_ip,
            'port': self.get_value_from_rc_file('overcloudrc',
                                                'OS_AUTH_URL',
                                                regex=':(\d+)/'),
            'user': self.get_value_from_rc_file('overcloudrc', 'OS_USERNAME'),
            'pwd': self.get_value_from_rc_file('overcloudrc', 'OS_PASSWORD'),
            'admin_token': self.get_value_from_file('keystone_conf',
                                                    'admin_token',
                                                    separator=' = ')
        }
        return api_config

    def run_command_on_overcloud(self, cmd):
        output = \
            self.run_cmd('ssh -i {} {} {}@{} {}'
                         .format(self.overcloud_key,
                                 self.SSH_OPTIONS,
                                 self.OVERCLOUD_USER,
                                 self.overcloud_ip,
                                 shlex.quote(cmd)))
        return output

    def create_mysql_user(self, host, pwd):
        mysql_file_name = '/tmp/create_user.sql'
        # create calipso MySQL user with access from jump host to all tables
        echo_cmd = "echo \"GRANT ALL PRIVILEGES ON *.* " \
                   "TO 'calipso'@'{}' " \
                   "IDENTIFIED BY '{}'; " \
                   "FLUSH PRIVILEGES;\" > {}"\
            .format(host, pwd, mysql_file_name)
        self.run_command_on_overcloud(echo_cmd)
        run_mysql_cmd = 'sudo mysql < {}'.format(mysql_file_name)
        self.run_command_on_overcloud(run_mysql_cmd)
        remove_file_cmd = 'rm {}'.format(mysql_file_name)
        self.run_command_on_overcloud(remove_file_cmd)
        return pwd

    def get_mysql_config(self):
        pwd = self.run_cmd('openssl rand -base64 18').strip()
        self.create_mysql_user(self.undercloud_ip, pwd)
        pwd = self.create_mysql_user(self.overcloud_ip, pwd)
        mysql_config = {
            'name': 'mysql',
            'host': self.overcloud_ip,
            'port': '3306',
            'user': 'calipso',
            'pwd': pwd
        }
        return mysql_config

    def get_cli_config(self):
        return {
            'name': 'CLI',
            'host': self.overcloud_ip,
            'user': self.OVERCLOUD_USER,
            'key': self.overcloud_key_container
        }

    def get_amqp_config(self):
        user = self.get_value_from_file('rabbitmq_conf',
                                        '    {default_user',
                                        separator=',',
                                        regex='"(.+)"')
        pwd = self.get_value_from_file('rabbitmq_conf',
                                       '    {default_pass',
                                       separator=',',
                                       regex='"(.+)"')
        port = self.get_value_from_file('rabbitmq_conf',
                                        '    {tcp_listeners',
                                        separator=',',
                                        regex=', (\d+)')
        port = int(port)
        return {
            'name': 'AMQP',
            'host': self.overcloud_ip,
            'port': port,
            'user': user,
            'pwd': pwd
        }

    def get_monitoring_config(self):
        return {
            'name': 'Monitoring',
            'config_folder': '/local_dir/sensu_config',
            'env_type': 'production',
            'rabbitmq_port': '5671',
            'rabbitmq_user': 'sensu',
            'server_ip': self.undercloud_ip,
            'server_name': 'sensu_server',
            'type': 'Sensu',
            'provision': 'None',
            'ssh_port': '20022',
            'ssh_user': 'root',
            'ssh_password': 'osdna',
            'api_port': 4567,
            'rabbitmq_pass': 'osdna'
        }

    def prepare_env_configuration_array(self):
        config_array = [
            self.get_api_config(),
            self.get_mysql_config(),
            self.get_cli_config(),
            self.get_amqp_config(),
            self.get_monitoring_config()
        ]
        self.env_config['configuration'] = config_array

    UI_USER = 'wNLeBJxNDyw8G7Ssg'

    def add_env_ui_conf(self):
        self.env_config.update({
            'user': self.UI_USER,
            'auth': {
                'view-env': [self.UI_USER],
                'edit-env': [self.UI_USER]
            }
        })

    def get_mechanism_driver(self):
        driver = self.get_value_from_file('ml2_conf', 'mechanism_drivers',
                                          separator=' =')
        return 'OVS' if driver == 'openvswitch' else driver

    def set_env_level_attributes(self):
        self.env_config.update({
            'distribution': 'Apex',
            'distribution_version': 'Euphrates',
            'type_drivers': self.get_value_from_file('ml2_conf',
                                                     'tenant_network_types',
                                                     separator=' = '),
            'mechanism_drivers': [self.get_mechanism_driver()],
            "operational": "running",
            "scanned": False,
            "type": "environment",
            "app_path": "/home/scan/calipso_prod/app",
            "listen": True,
            "enable_monitoring": True,
            "aci_enabled": False,
            "last_scanned": "",
            "monitoring_setup_done": False
        })

    def prepare_env_config(self):
        self.prepare_env_configuration_array()
        self.set_env_level_attributes()
        self.add_env_ui_conf()
        config_dump = json.dumps(self.env_config, sort_keys=True, indent=4,
                                 separators=(',', ': '))
        with open(self.env_config_file, 'w') as config_file:
            config_file.write(config_dump)

    def setup_environment_config(self, config_file):
        self.run_cmd('mkdir -p {}'.format(self.args.config_dir))
        self.env_config = {'name': self.args.env}
        self.undercloud_ip = self.get_undercloud_ip()
        config_file.write('jumphost_admin_ip {}\n'.format(self.undercloud_ip))
        self.set_ssh_dir()
        self.get_undercloud_setup()
        self.overcloud_ip = self.get_overcloud_ip()
        config_file.write('overcloud_admin_ip {}\n'.format(self.overcloud_ip))
        self.get_overcloud_setup()
        # now get correct IP of overcloud from RabbitMQ setup
        self.overcloud_ip = self.get_value_from_file('rabbitmq_conf',
                                                     '    {tcp_listeners',
                                                     regex='"(.*)"',
                                                     separator=',')
        self.prepare_env_config()

    def get(self):
        try:
            print('Fetching Apex environment settings')
            self.log = FileLogger(self.args.logfile)
            self.run_cmd('mkdir -p {}'.format(self.args.config_dir))
            with open(self.config_file, 'w') as config_file:
                self.setup_environment_config(config_file)
            print('Finished fetching Apex environment settings')
            return True, 'Environment setup finished successfully'
        except RuntimeError as e:
            return False, str(e)


if __name__ == '__main__':
    fetcher = ApexEnvironmentFetcher()
    ret, msg = fetcher.get()
    if not ret:
        if fetcher.log:
            fetcher.log.error(msg)
        else:
            print(msg)
    sys.exit(0 if ret else 1)
