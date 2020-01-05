###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import os.path
from pkg_resources import parse_version

from base.utils.cli_access import CliAccess
from base.utils.exceptions import CredentialsError, HostAddressError
from base.utils.inventory_mgr import InventoryMgr
from base.utils.ssh_connection import SshError
from monitoring.setup.monitoring_handler import MonitoringHandler


class SensuClientInstaller(MonitoringHandler):

    UBUNTU = 'ubuntu'
    CENTOS = 'centos'

    INSTALL_CMD = {
        UBUNTU: 'dpkg -i {}',
        CENTOS: 'rpm -i {}'
    }
    PERMISSIONS_CMD = {
        UBUNTU: '',
        CENTOS: 'usermod -aG wheel sensu'
    }
    SUDOERS_FILE = '/etc/sudoers'

    available_downloads = {}

    def __init__(self, env: str, host_id: str):
        super().__init__(env)
        self.cli_ssh = CliAccess()
        self.inv = InventoryMgr()
        self.host_id = host_id
        self.host = self.inv.get_by_id(env, host_id)
        self.server = self.env_monitoring_config.get('server_ip')
        self.server_cli_ssh = self.get_ssh(self.server)
        self.ubuntu_dist = None
        self.required_package = None

    def install(self):
        pkg_to_install = self.get_pkg_to_install()
        if not pkg_to_install:
            return
        try:
            self.fetch_package(pkg_to_install)
            self.install_package(pkg_to_install)
            self.set_permissions()
        except (SystemError, SshError, CredentialsError, HostAddressError) as e:
            self.log.error('Sensu install on host {} failed: {}'
                           .format(self.host, str(e)))
            return

    @staticmethod
    def get_attr_from_output(output_lines: list, attr: str) -> str:
        matches = [l for l in output_lines if l.startswith(attr)]
        if not matches:
            return ''
        line = matches[0]
        return SensuClientInstaller.get_attr_from_output_line(line)

    @staticmethod
    def get_attr_from_output_line(output_line: str):
        val = output_line[output_line.index(':')+1:].strip()
        return val

    INSTALLED = 'Installed: '
    CANDIDATE = 'Candidate: '
    SENSU_DIR = '/opt/sensu'
    SENSU_PKG_DIR = '/etc/sensu/pkg'
    SENSU_PKG_DIR_LOCAL = '/tmp/sensu_pkg'
    SENSU_VERSION_FILE = '/opt/sensu/version-manifest.txt'

    def find_available_downloads(self):
        ls_output = self.server_cli_ssh.exec('ls -R {}'
                                             .format(self.SENSU_PKG_DIR))
        ls_lines = ls_output.splitlines()
        last_target_dir = None
        for line in ls_lines:
            if line[-4:] in ['/32:', '/64:']:
                last_target_dir = line.replace(self.SENSU_PKG_DIR, '')
                continue
            elif last_target_dir:
                target_dir = last_target_dir.strip(os.path.sep).strip(':')
                self.available_downloads[target_dir] = line
                last_target_dir = None
            else:
                last_target_dir = None

    def find_available_package(self, os_details: dict):
        if not self.available_downloads:
            self.find_available_downloads()
        distribution = os_details['ID']
        version = os_details['version'].split()[-2].lower()
        arch = os_details['architecure'][-2:]
        download_dir = os.path.join(distribution, version, arch)
        download_file = self.available_downloads.get(download_dir)
        full_path = '' if not download_file \
            else os.path.join(self.SENSU_PKG_DIR, download_dir, download_file)
        return download_file, full_path

    @staticmethod
    def find_available_version(download_file: str) -> str:
        ver = download_file.replace('sensu', '').strip('-_')
        ver = ver[:ver.index('-')]
        return ver

    def get_pkg_to_install(self) -> str:
        if self.provision == self.provision_levels['none']:
            return ''
        if not self.host:
            return ''
        supported_os = [self.UBUNTU, self.CENTOS]
        distribution = self.host['OS']['ID']
        if distribution not in [self.UBUNTU, self.CENTOS]:
            self.log.error('Sensu client auto-install only supported for: {}'
                           .format(', '.join(supported_os)))
            return ''
        cmd = '[ -d {} ] && head -1 {} | sed "s/sensu //"' \
            .format(self.SENSU_DIR, self.SENSU_VERSION_FILE)
        installed_version = self.run_cmd(cmd, use_sudo=False)
        os_details = self.host['OS']
        available_pkg, pkg_path = self.find_available_package(os_details)
        available_version = self.find_available_version(available_pkg)
        if parse_version(available_version) <= parse_version(installed_version):
            return ''
        return pkg_path

    def run_cmd(self, cmd, use_sudo=True) -> str:
        ret = self.cli_ssh.run(cmd, ssh_to_host=self.host_id, use_sudo=use_sudo)
        return ret.strip()

    def get_local_path(self, pkg_to_install: str):
        return os.path.join(self.SENSU_PKG_DIR_LOCAL,
                            os.path.basename(pkg_to_install))

    def fetch_package(self, pkg_to_install: str):
        self.make_directory(self.SENSU_PKG_DIR_LOCAL)
        self.get_file(self.server, pkg_to_install,
                      self.get_local_path(pkg_to_install))
        local_path = self.get_local_path(pkg_to_install)
        self.copy_to_remote_host(self.host_id,
                                 local_path=local_path,
                                 remote_path=local_path)
        if not self.is_gateway_host(self.host_id):
            self.copy_from_gateway_to_host(self.host_id,
                                           self.SENSU_PKG_DIR_LOCAL,
                                           self.SENSU_PKG_DIR_LOCAL)

    def install_package(self, pkg_to_install):
        local_path = self.get_local_path(pkg_to_install)
        install_cmd = self.INSTALL_CMD[self.host['OS']['ID']]
        try:
            self.run_cmd(install_cmd.format(local_path))
        except (SshError, CredentialsError, HostAddressError) as e:
            key_warn = 'warning: {}: Header V4 RSA/SHA1 Signature, key ID ' \
                .format(local_path)
            error_string = str(e)
            if key_warn not in error_string:
                raise e

    def set_permissions(self):
        cmd = self.PERMISSIONS_CMD[self.host['OS']['ID']]
        if cmd:
            self.run_cmd(cmd)
        # add to sudoers file
        sudoer_permission = 'sensu        ALL=(ALL)       NOPASSWD: ALL'
        sudoer_cmd = 'grep --silent -w sensu {} || echo "{}" >> {}'\
            .format(self.SUDOERS_FILE, sudoer_permission, self.SUDOERS_FILE)
        self.run_cmd(sudoer_cmd, use_sudo=False)
