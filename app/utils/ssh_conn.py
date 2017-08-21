###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import os

from discover.configuration import Configuration
from utils.inventory_mgr import InventoryMgr
from utils.ssh_connection import SshConnection


class SshConn(SshConnection):
    config = None
    ssh = None
    connections = {}

    max_call_count_per_con = 100
    timeout = 15  # timeout for exec in seconds

    def __init__(self, host_name, for_sftp=False):
        self.config = Configuration()
        self.env_config = self.config.get_env_config()
        self.env = self.env_config['name']
        self.conf = self.config.get('CLI')
        self.gateway = None
        self.host = None
        self.host_conf = self.get_host_conf(host_name)
        self.ssh = None
        self.ftp = None
        self.for_sftp = for_sftp
        self.key = None
        self.port = None
        self.user = None
        self.pwd = None
        self.check_definitions()
        super().__init__(host_name, self.user, _pwd=self.pwd, _key=self.key,
                         _port=self.port, for_sftp=for_sftp)
        self.inv = InventoryMgr()
        if host_name in self.connections and not self.ssh:
            self.ssh = self.connections[host_name]

    def get_host_conf(self, host_name):
        if 'hosts' in self.conf:
            if not host_name:
                raise ValueError('SshConn(): host must be specified ' +
                                 'if multi-host CLI config is used')
            if host_name not in self.conf['hosts']:
                raise ValueError('host details missing: ' + host_name)
            return self.conf['hosts'][host_name]
        else:
            return self.conf

    def check_definitions(self):
        try:
            self.host = self.host_conf['host']
            if self.host in self.connections:
                self.ssh = self.connections[self.host]
        except KeyError:
            raise ValueError('Missing definition of host for CLI access')
        try:
            self.user = self.host_conf['user']
        except KeyError:
            raise ValueError('Missing definition of user for CLI access')
        try:
            self.key = self.host_conf['key']
            if self.key and not os.path.exists(self.key):
                raise ValueError('Key file not found: ' + self.key)
        except KeyError:
            pass
        try:
            self.pwd = self.host_conf['pwd']
        except KeyError:
            self.pwd = None
        if not self.key and not self.pwd:
            raise ValueError('Must specify key or password for CLI access')

    gateway_hosts = {}

    @staticmethod
    def get_gateway_host(host):
        if not SshConn.gateway_hosts.get(host):
            ssh = SshConn(host)
            gateway = ssh.exec('uname -n')
            SshConn.gateway_hosts[host] = gateway.strip()
        return SshConn.gateway_hosts[host]

    def is_gateway_host(self, host):
        gateway_host = self.get_gateway_host(host)
        return host == gateway_host
