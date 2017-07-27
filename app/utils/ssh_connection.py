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

import paramiko

from utils.binary_converter import BinaryConverter


class SshConnection(BinaryConverter):
    config = None
    ssh = None
    connections = {}
    cli_connections = {}
    sftp_connections = {}

    max_call_count_per_con = 100
    timeout = 15  # timeout for exec in seconds

    DEFAULT_PORT = 22

    def __init__(self, _host: str, _user: str, _pwd: str=None, _key: str = None,
                 _port: int = None,  _call_count_limit: int=None,
                 for_sftp: bool = False):
        super().__init__()
        self.host = _host
        self.ssh = None
        self.ftp = None
        self.for_sftp = for_sftp
        self.key = _key
        self.port = _port
        self.user = _user
        self.pwd = _pwd
        self.check_definitions()
        self.fetched_host_details = False
        self.call_count = 0
        self.call_count_limit = 0 if for_sftp \
            else (SshConnection.max_call_count_per_con
                  if _call_count_limit is None else _call_count_limit)
        if for_sftp:
            self.sftp_connections[_host] = self
        else:
            self.cli_connections[_host] = self

    def check_definitions(self):
        if not self.host:
            raise ValueError('Missing definition of host for CLI access')
        if not self.user:
            raise ValueError('Missing definition of user ' +
                             'for CLI access to host {}'.format(self.host))
        if self.key and not os.path.exists(self.key):
            raise ValueError('Key file not found: ' + self.key)
        if not self.key and not self.pwd:
            raise ValueError('Must specify key or password ' +
                             'for CLI access to host {}'.format(self.host))

    @staticmethod
    def get_ssh(host, for_sftp=False):
        if for_sftp:
            return SshConnection.cli_connections.get(host)
        return SshConnection.sftp_connections.get(host)

    @staticmethod
    def get_connection(host, for_sftp=False):
        key = ('sftp-' if for_sftp else '') + host
        return SshConnection.connections.get(key)

    def disconnect(self):
        if self.ssh:
            self.ssh.close()

    @staticmethod
    def disconnect_all():
        for ssh in SshConnection.cli_connections.values():
            ssh.disconnect()
        SshConnection.cli_connections = {}
        for ssh in SshConnection.sftp_connections.values():
            ssh.disconnect()
        SshConnection.sftp_connections = {}

    def get_host(self):
        return self.host

    def get_user(self):
        return self.user

    def set_call_limit(self, _limit: int):
        self.call_count_limit = _limit

    def connect(self, reconnect=False) -> bool:
        connection = self.get_connection(self.host, self.for_sftp)
        if connection:
            self.ssh = connection
            if reconnect:
                self.log.info("SshConnection: " +
                              "****** forcing reconnect: %s ******",
                              self.host)
            elif self.call_count >= self.call_count_limit > 0:
                self.log.info("SshConnection: ****** reconnecting: %s, " +
                              "due to call count: %s ******",
                              self.host, self.call_count)
            else:
                return True
            connection.close()
            self.ssh = None
        self.ssh = paramiko.SSHClient()
        connection_key = ('sftp-' if self.for_sftp else '') + self.host
        SshConnection.connections[connection_key] = self.ssh
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.key:
            k = paramiko.RSAKey.from_private_key_file(self.key)
            self.ssh.connect(hostname=self.host, username=self.user, pkey=k,
                             port=self.port if self.port is not None
                             else self.DEFAULT_PORT,
                             password=self.pwd, timeout=30)
        else:
            try:
                port = self.port if self.port is not None else self.DEFAULT_PORT
                self.ssh.connect(self.host,
                                 username=self.user,
                                 password=self.pwd,
                                 port=port,
                                 timeout=30)
            except paramiko.ssh_exception.AuthenticationException:
                self.log.error('Failed SSH connect to host {}, port={}'
                               .format(self.host, port))
                self.ssh = None
        self.call_count = 0
        return self.ssh is not None

    def exec(self, cmd):
        if not self.connect():
            return ''
        self.call_count += 1
        self.log.debug("call count: %s, running call:\n%s\n",
                       str(self.call_count), cmd)
        stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=self.timeout)
        stdin.close()
        err = self.binary2str(stderr.read())
        if err:
            # ignore messages about loading plugin
            err_lines = [l for l in err.splitlines()
                         if 'Loaded plugin: ' not in l]
            if err_lines:
                self.log.error("CLI access: \n" +
                               "Host: {}\nCommand: {}\nError: {}\n".
                               format(self.host, cmd, err))
                stderr.close()
                stdout.close()
                return ""
        ret = self.binary2str(stdout.read())
        stderr.close()
        stdout.close()
        return ret

    def copy_file(self, local_path, remote_path, mode=None):
        if not self.connect():
            return
        if not self.ftp:
            self.ftp = self.ssh.open_sftp()
        try:
            self.ftp.put(local_path, remote_path)
        except IOError as e:
            self.log.error('SFTP copy_file failed to copy file: ' +
                           'local: ' + local_path +
                           ', remote host: ' + self.host +
                           ', error: ' + str(e))
            return str(e)
        try:
            remote_file = self.ftp.file(remote_path, 'a+')
        except IOError as e:
            self.log.error('SFTP copy_file failed to open file after put(): ' +
                           'local: ' + local_path +
                           ', remote host: ' + self.host +
                           ', error: ' + str(e))
            return str(e)
        try:
            if mode:
                remote_file.chmod(mode)
        except IOError as e:
            self.log.error('SFTP copy_file failed to chmod file: ' +
                           'local: ' + local_path +
                           ', remote host: ' + self.host +
                           ', port: ' + self.port +
                           ', error: ' + str(e))
            return str(e)
        self.log.info('SFTP copy_file success: '
                      'host={},port={},{} -> {}'.format(
            str(self.host), str(self.port), str(local_path), str(remote_path)))
        return ''

    def copy_file_from_remote(self, remote_path, local_path):
        if not self.connect():
            return
        if not self.ftp:
            self.ftp = self.ssh.open_sftp()
        try:
            self.ftp.get(remote_path, local_path)
        except IOError as e:
            self.log.error('SFTP copy_file_from_remote failed to copy file: '
                           'remote host: {}, '
                           'remote_path: {}, local: {}, error: {}'
                           .format(self.host, remote_path, local_path, str(e)))
            return str(e)
        self.log.info('SFTP copy_file_from_remote success: host={},{} -> {}'.
                      format(self.host, remote_path, local_path))
        return ''

    def is_gateway_host(self, host):
        return True
