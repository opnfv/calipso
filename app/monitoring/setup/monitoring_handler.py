###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
# handle specific setup of monitoring

import os
import json
import subprocess
from socket import *

import copy
import pymongo
import shutil
import stat
import tempfile
from boltons.iterutils import remap

from discover.configuration import Configuration
from discover.fetchers.cli.cli_access import CliAccess
from utils.binary_converter import BinaryConverter
from utils.deep_merge import remerge
from utils.inventory_mgr import InventoryMgr
from utils.logging.full_logger import FullLogger
from utils.mongo_access import MongoAccess
from utils.ssh_conn import SshConn
from utils.ssh_connection import SshConnection, SshError


class MonitoringHandler(MongoAccess, CliAccess, BinaryConverter):
    PRODUCTION_CONFIG_DIR = '/etc/sensu/conf.d'
    APP_SCRIPTS_FOLDER = 'monitoring/checks'
    REMOTE_SCRIPTS_FOLDER = '/etc/sensu/plugins'

    provision_levels = {
        'none': 0,
        'db': 1,
        'files': 2,
        'deploy': 3
    }

    pending_changes = {}

    fetch_ssl_files = []

    def __init__(self, env):
        super().__init__()
        self.log = FullLogger()
        self.configuration = Configuration()
        self.mechanism_drivers = \
            self.configuration.environment['mechanism_drivers']
        self.env = env
        self.had_errors = False
        self.monitoring_config = self.db.monitoring_config_templates
        try:
            self.env_monitoring_config = self.configuration.get('Monitoring')
        except IndexError:
            self.env_monitoring_config = {}
        self.local_host = self.env_monitoring_config.get('server_ip', '')
        self.scripts_prepared_for_host = {}
        self.replacements = self.env_monitoring_config
        self.inv = InventoryMgr()
        self.config_db = self.db[self.inv.get_coll_name('monitoring_config')]
        self.provision = self.provision_levels['none']
        if self.env_monitoring_config:
            provision = self.env_monitoring_config.get('provision', 'none')
            provision = str.lower(provision)
            self.provision =\
                self.provision_levels.get(provision,
                                          self.provision_levels['none'])

    # create a directory if it does not exist
    @staticmethod
    def make_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def get_config_dir(self, sub_dir=''):
        config_folder = self.env_monitoring_config['config_folder'] + \
            (os.sep + sub_dir if sub_dir else '')
        return self.make_directory(config_folder).rstrip(os.sep)

    def prepare_config_file(self, file_type, base_condition):
        condition = base_condition
        condition['type'] = file_type
        sort = [('order', pymongo.ASCENDING)]
        docs = self.monitoring_config.find(condition, sort=sort)
        content = {}
        for doc in docs:
            if not self.check_env_condition(doc):
                return {}
            content.update(doc)
        self.replacements['app_path'] = \
            self.configuration.environment['app_path']
        config = self.content_replace({'config': content.get('config', {})})
        return config

    def check_env_condition(self, doc):
        if 'condition' not in doc:
            return True
        condition = doc['condition']
        if 'mechanism_drivers' not in condition:
            return True
        required_mechanism_drivers = condition['mechanism_drivers']
        if not isinstance(required_mechanism_drivers, list):
            required_mechanism_drivers = [required_mechanism_drivers]
        intersection = [val for val in required_mechanism_drivers
                        if val in self.mechanism_drivers]
        return bool(intersection)

    def content_replace(self, content):
        content_remapped = remap(content, visit=self.fill_values)
        return content_remapped

    def format_string(self, val):
        formatted = val if not isinstance(val, str) or '{' not in val \
            else val.format_map(self.replacements)
        return formatted

    def fill_values(self, path, key, value):
        if not path:
            return key, value
        key_formatted = self.format_string(key)
        value_formatted = self.format_string(value)
        return key_formatted, value_formatted

    def get_config_from_db(self, host, file_type):
        find_tuple = {
            'environment': self.env,
            'host': host,
            'type': file_type
        }
        doc = self.config_db.find_one(find_tuple)
        if not doc:
            return {}
        doc.pop("_id", None)
        return self.decode_mongo_keys(doc)

    def write_config_to_db(self, host, config, file_type):
        find_tuple = {
            'environment': self.env,
            'host': host,
            'type': file_type
        }
        doc = copy.copy(find_tuple)
        doc['config'] = config
        doc = self.encode_mongo_keys(doc)
        if not doc:
            return {}
        self.config_db.update_one(find_tuple, {'$set': doc}, upsert=True)

    def merge_config(self, host, file_type, content):
        """
        merge current monitoring config of host
        with newer content.
        return the merged config
        """
        doc = self.get_config_from_db(host, file_type)
        config = remerge([doc['config'], content.get('config')]) if doc \
            else content.get('config', {})
        self.write_config_to_db(host, config, file_type)
        return config

    def write_config_file(self, file_name, sub_dir, host, content,
                          is_container=False, is_server=False):
        """
        apply environment definitions to the config,
        e.g. replace {server_ip} with the IP or host name for the server
        """
        # save the config to DB first, and while doing that
        # merge it with any existing config on same host
        content = self.merge_config(host, file_name, content)

        if self.provision == self.provision_levels['db']:
            self.log.debug('Monitoring setup kept only in DB')
            return
        # now dump the config to the file
        content_json = json.dumps(content.get('config', content),
                                  sort_keys=True, indent=4)
        content_json += '\n'
        # always write the file locally first
        local_dir = self.make_directory(os.path.join(self.get_config_dir(),
                                        sub_dir.strip(os.path.sep)))
        local_path = os.path.join(local_dir, file_name)
        self.write_to_local_host(local_path, content_json)
        self.track_setup_changes(host, is_container, file_name, local_path,
                                 sub_dir, is_server=is_server)

    def add_changes_for_all_clients(self):
        """
        to debug deployment, add simulated track changes entries.
        no need to add for server, as these are done by server_setup()
        """
        docs = self.config_db.find({'environment': self.env})
        for doc in docs:
            host = doc['host']
            sub_dir = os.path.join('host', host)
            file_name = doc['type']
            config_folder = self.env_monitoring_config['config_folder']
            local_path = os.path.join(config_folder, sub_dir, file_name)
            if host == self.env_monitoring_config['server_ip']:
                continue
            self.track_setup_changes(host, False, file_name, local_path,
                                     sub_dir)

    def get_ssh(self, host, is_container=False, for_sftp=False):
        ssh = SshConnection.get_ssh(host, for_sftp)
        if not ssh:
            conf = self.env_monitoring_config
            if is_container or host == conf['server_ip']:
                host = conf['server_ip']
                port = int(conf['ssh_port'])
                user = conf['ssh_user']
                pwd = conf['ssh_password']
                ssh = SshConnection(host, user, _pwd=pwd, _port=port,
                                    for_sftp=for_sftp)
            else:
                ssh = SshConn(host, for_sftp=for_sftp)
        return ssh

    def track_setup_changes(self, host=None, is_container=False, file_name=None,
                            local_path=None, sub_dir=None,
                            is_server=False,
                            target_mode=None,
                            target_path=PRODUCTION_CONFIG_DIR):
        if host not in self.pending_changes:
            self.pending_changes[host] = {}
        if file_name not in self.pending_changes[host]:
            self.pending_changes[host][file_name] = {
                "host": host,
                "is_container": is_container,
                "is_server": is_server,
                "file_name": file_name,
                "local_path": local_path,
                "sub_dir": sub_dir,
                "target_path": target_path,
                "target_mode": target_mode
            }

    def handle_pending_setup_changes(self):
        if self.provision < self.provision_levels['files']:
            if self.provision == self.provision_levels['db']:
                self.log.info('Monitoring config applied only in DB')
            return True
        self.log.info('applying monitoring setup')
        hosts = {}
        scripts_to_hosts = {}
        for host, host_changes in self.pending_changes.items():
            self.handle_pending_host_setup_changes(host_changes, hosts,
                                                   scripts_to_hosts)
        if self.provision < self.provision_levels['deploy']:
            return True
        if self.fetch_ssl_files:
            self.deploy_ssl_files(list(scripts_to_hosts.keys()))
        for host in scripts_to_hosts.values():
            self.deploy_scripts_to_host(host)
        for host in hosts.values():
            self.deploy_config_to_target(host)
        had_errors = ', with some error(s)' if self.had_errors else ''
        self.log.info('done applying monitoring setup{}'.format(had_errors))
        return not self.had_errors

    def handle_pending_host_setup_changes(self, host_changes, hosts,
                                          scripts_to_hosts):
        if self.provision < self.provision_levels['deploy']:
            self.log.info('Monitoring config not deployed to remote host')
        for file_type, changes in host_changes.items():
            host = changes['host']
            is_container = changes['is_container']
            is_server = changes['is_server']
            local_dir = changes['local_path']
            if local_dir == "scripts":
                scripts_to_hosts[host] = {'host': host, 'is_server': is_server}
                continue
            self.log.debug('applying monitoring setup changes ' +
                           'for host ' + host + ', file type: ' + file_type)
            is_local_host = host == self.local_host
            file_path = os.path.join(self.PRODUCTION_CONFIG_DIR, file_type)
            if not is_server and host not in hosts:
                hosts[host] = {
                    'host': host,
                    'local_dir': local_dir,
                    'is_local_host': is_local_host,
                    'is_container': is_container,
                    'is_server': is_server
                }
            if is_server:
                remote_path = self.PRODUCTION_CONFIG_DIR
                if os.path.isfile(local_dir):
                    remote_path += os.path.sep + os.path.basename(local_dir)
                try:
                    self.write_to_server(local_dir,
                                         remote_path=remote_path,
                                         is_container=is_container)
                except SshError:
                    self.had_errors = True
            elif is_local_host:
                    # write to production configuration directory on local host
                    self.make_directory(self.PRODUCTION_CONFIG_DIR)
                    shutil.copy(changes['local_path'], file_path)
            else:
                # write to remote host prepare dir - use sftp
                if self.provision < self.provision_levels['deploy']:
                    continue
                try:
                    self.write_to_remote_host(host, changes['local_path'])
                except SshError:
                    self.had_errors = True

    def prepare_scripts(self, host, is_server):
        if self.scripts_prepared_for_host.get(host, False):
            return
        gateway_host = SshConn.get_gateway_host(host)
        # copy scripts to host
        scripts_dir = os.path.join(self.env_monitoring_config['app_path'],
                                   self.APP_SCRIPTS_FOLDER)
        script_files = [f for f in os.listdir(scripts_dir)
                        if os.path.isfile(os.path.join(scripts_dir, f))]
        script_mode = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | \
            stat.S_IROTH | stat.S_IXOTH
        target_host = host if is_server else gateway_host
        self.make_remote_dir(target_host, self.REMOTE_SCRIPTS_FOLDER)
        for file_name in script_files:
            remote_path = os.path.join(self.REMOTE_SCRIPTS_FOLDER, file_name)
            local_path = os.path.join(scripts_dir, file_name)
            if not os.path.isfile(local_path):
                continue
            if is_server:
                ssh = self.get_ssh(target_host, for_sftp=True)
                ssh.copy_file(local_path, remote_path, mode=script_mode)
            else:
                self.copy_to_remote_host(target_host, local_path, remote_path,
                                         mode=script_mode,
                                         make_remote_dir=False)
        self.scripts_prepared_for_host[host] = True

    def deploy_ssl_files(self, hosts: list):
        try:
            monitoring_server = self.env_monitoring_config['server_ip']
            gateway_host = SshConn.get_gateway_host(hosts[0])
            temp_dir = tempfile.TemporaryDirectory()
            for file_path in self.fetch_ssl_files:
                # copy SSL files from the monitoring server
                file_name = os.path.basename(file_path)
                local_path = os.path.join(temp_dir.name, file_name)
                self.get_file(monitoring_server, file_path, local_path)
                #  first copy the files to the gateway
                self.write_to_remote_host(gateway_host, local_path,
                                          remote_path=file_path)
            ssl_path = os.path.commonprefix(self.fetch_ssl_files)
            for host in hosts:
                self.copy_from_gateway_to_host(host, ssl_path, ssl_path)
        except SshError:
            self.had_errors = True

    def deploy_scripts_to_host(self, host_details):
        try:
            host = host_details['host']
            is_server = host_details['is_server']
            self.prepare_scripts(host, is_server)
            remote_path = self.REMOTE_SCRIPTS_FOLDER
            local_path = remote_path + os.path.sep + '*.py'
            if is_server:
                return  # this was done earlier
            self.copy_from_gateway_to_host(host, local_path, remote_path)
        except SshError:
            self.had_errors = True

    def restart_service(self, host: str = None,
                        service: str = 'sensu-client',
                        is_server: bool = False,
                        msg: str =None):
        ssh = self.get_ssh(host)
        cmd = 'sudo /etc/init.d/{} restart'.format(service)
        log_msg = msg if msg else 'deploying config to host {}'.format(host)
        self.log.info(log_msg)
        try:
            if is_server:
                ssh.exec(cmd)
            else:
                self.run(cmd, ssh_to_host=host, ssh=ssh)
        except SshError:
            self.had_errors = True

    def deploy_config_to_target(self, host_details):
        try:
            host = host_details['host']
            is_local_host = host_details['is_local_host']
            is_container = host_details['is_container']
            is_server = host_details['is_server']
            local_dir = host_details['local_dir']
            if is_container or is_server or not is_local_host:
                local_dir = os.path.dirname(local_dir)
                if not is_server:
                    self.move_setup_files_to_remote_host(host, local_dir)
                # restart the Sensu client on the remote host,
                # so it takes the new setup
                self.restart_service(host)
        except SshError:
            self.had_errors = True

    def run_cmd_locally(self, cmd):
        try:
            subprocess.popen(cmd.split(),
                             shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print("Error running command: " + cmd +
                  ", output: " + self.binary2str(e.output) + "\n")

    def move_setup_files_to_remote_host(self, host, local_dir):
        if self.provision < self.provision_levels['deploy']:
            self.log.info('Monitoring config not written to remote host')
            return
        # need to scp the files from the gateway host to the target host
        remote_path = self.PRODUCTION_CONFIG_DIR
        self.copy_from_gateway_to_host(host, local_dir, remote_path)

    def copy_from_gateway_to_host(self, host, local_dir, remote_path):
        ssh = self.get_ssh(host)
        what_to_copy = local_dir if '*' in local_dir else local_dir + '/*'
        if ssh.is_gateway_host(host):
            # on gateway host, perform a simple copy
            # make sure the source and destination are not the same
            local_dir_base = local_dir[:local_dir.rindex('/*')] \
                if '/*' in local_dir else local_dir
            if local_dir_base.strip('/*') == remote_path.strip('/*'):
                return  # same directory - nothing to do
            cmd = 'cp {} {}'.format(what_to_copy, remote_path)
            self.run(cmd, ssh=ssh)
            return
        self.make_remote_dir(host, remote_path)
        remote_path = ssh.get_user() + '@' + host + ':' + \
            remote_path + os.sep
        self.run_on_gateway('scp {} {}'.format(what_to_copy, remote_path),
                            enable_cache=False,
                            use_sudo=None)

    def make_remote_dir_on_host(self, ssh, host, path, path_is_file=False):
        # make sure we have write permissions in target directories
        dir_path = path
        if path_is_file:
            dir_path = os.path.dirname(dir_path)
        cmd = 'sudo mkdir -p ' + dir_path
        try:
            self.run(cmd, ssh_to_host=host, ssh=ssh)
        except timeout:
            self.log.error('timed out trying to create directory {} on host {}'
                           .format(dir_path, host))
            return
        cmd = 'sudo chown -R ' + ssh.get_user() + ' ' + dir_path
        self.run(cmd, ssh_to_host=host, ssh=ssh)

    def make_remote_dir(self, host, path, path_is_file=False):
        ssh = self.get_ssh(host, for_sftp=True)
        self.make_remote_dir_on_host(ssh, host, path, path_is_file)

    def copy_to_remote_host(self, host, local_path, remote_path, mode=None,
                            make_remote_dir=True):
        # copy the local file to the preparation folder for the remote host
        # on the gateway host
        ssh = self.get_ssh(host)
        gateway_host = ssh.get_gateway_host(host)
        if make_remote_dir:
            self.make_remote_dir(gateway_host, remote_path, path_is_file=True)
        ftp_ssh = self.get_ssh(gateway_host, for_sftp=True)
        ftp_ssh.copy_file(local_path, remote_path, mode)

    def write_to_remote_host(self, host, local_path=None, remote_path=None):
        remote_path = remote_path if remote_path else local_path
        self.copy_to_remote_host(host, local_path, remote_path)

    def write_to_server(self, local_path, remote_path=None, is_container=False):
        host = self.env_monitoring_config['server_ip']
        ssh = self.get_ssh(host, is_container=is_container)
        remote_path = remote_path if remote_path else local_path
        self.make_remote_dir_on_host(ssh, host, remote_path, True)
        # copy to config dir first
        ftp_ssh = self.get_ssh(host, is_container=is_container, for_sftp=True)
        ftp_ssh.copy_file(local_path, remote_path)

    @staticmethod
    def write_to_local_host(file_path, content):
        f = open(file_path, "w")
        f.write(content)
        f.close()
        return file_path

    def get_file(self, host, remote_path, local_path):
        ftp_ssh = self.get_ssh(host, for_sftp=True)
        ftp_ssh.copy_file_from_remote(remote_path, local_path)

