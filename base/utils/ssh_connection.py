###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import socket

import os
import paramiko
import paramiko.buffered_pipe

from base.utils.binary_converter import BinaryConverter
from base.utils.exceptions import CredentialsError, HostAddressError


class SshError(Exception):
    pass


class SshConnection(BinaryConverter):
    connections = {}

    max_call_count_per_con = 100
    timeout = 15  # timeout for exec in seconds
    CONNECT_TIMEOUT = 5

    DEFAULT_PORT = 22

    def __init__(self, _host: str, _user: str, _pwd: str=None, _key: str = None,
                 _port: int = None,  _call_count_limit: int=None,
                 for_sftp: bool = False):
        super().__init__()
        self.host = _host
        self.ssh_client = None
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
        self.connections[self.get_connection_key(_host, for_sftp)] = self

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
    def get_ssh(host, _for_sftp=False):
        return SshConnection.get_connection(host, for_sftp=_for_sftp)

    @staticmethod
    def get_connection_key(host, for_sftp=False):
        key = ('sftp-' if for_sftp else '') + host
        return key

    @staticmethod
    def get_connection(host, for_sftp=False):
        key = SshConnection.get_connection_key(host, for_sftp)
        return SshConnection.connections.get(key)

    def disconnect(self):
        if self.ssh_client:
            self.ssh_client.close()

    @staticmethod
    def disconnect_all():
        for ssh in SshConnection.connections.values():
            ssh.disconnect()
        SshConnection.connections = {}

    def get_host(self):
        return self.host

    def get_user(self):
        return self.user

    def set_call_limit(self, _limit: int):
        self.call_count_limit = _limit

    def connect(self, reconnect=False) -> bool:
        connection = self.get_connection(self.host, self.for_sftp)
        if connection and connection.ssh_client:
            self.ssh_client = connection.ssh_client
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
            self.ssh_client = None
        self.ssh_client = paramiko.SSHClient()
        connection_key = SshConnection.get_connection_key(self.host,
                                                          self.for_sftp)
        SshConnection.connections[connection_key] = self
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        port = self.port if self.port is not None else self.DEFAULT_PORT
        try:
            if self.key:
                k = paramiko.RSAKey.from_private_key_file(self.key)
                self.ssh_client.connect(hostname=self.host,
                                        username=self.user,
                                        pkey=k,
                                        port=port,
                                        password=self.pwd,
                                        timeout=self.CONNECT_TIMEOUT)
            else:
                self.ssh_client.connect(self.host,
                                        username=self.user,
                                        password=self.pwd,
                                        port=port,
                                        timeout=self.CONNECT_TIMEOUT)
        except paramiko.ssh_exception.AuthenticationException:
            msg = 'Failed authentication on SSH connect ' \
                  'to host {}, port={}' \
                .format(self.host, port)
            self.log.error(msg)
            raise CredentialsError(msg)
        except (paramiko.ssh_exception.SSHException, TimeoutError,
                paramiko.buffered_pipe.PipeTimeout):
            msg = 'Timeout creating SSH connection to host {}, port={}' \
                .format(self.host, port)
            self.log.error(msg)
            raise HostAddressError(msg)
        except Exception as e:
            msg = 'Error creating SSH connection to host {}, port={}: {}' \
                .format(self.host, port, str(e))
            self.log.error(msg)
            if str(e) == 'timed out':
                raise HostAddressError(msg)
            else:
                raise SshError(msg)
        self.call_count = 0
        return self.ssh_client is not None

    def exec(self, cmd):
        if not self.connect():
            return ''
        self.call_count += 1
        self.log.debug("call count: %s, running call:\n%s\n",
                       str(self.call_count), cmd)
        try:
            stdin, stdout, stderr = \
                self.ssh_client.exec_command(cmd, timeout=self.timeout)
        except (AttributeError, paramiko.buffered_pipe.PipeTimeout,
                socket.timeout) as e:
            msg = 'Error when executing command: {}, error: {}' \
                .format(cmd, str(e))
            self.log.error(msg)
            raise SshError(msg)
        stdin.close()

        try:
            err = self.binary2str(stderr.read())
        except (paramiko.buffered_pipe.PipeTimeout, socket.timeout) \
                as timeout_error:
            msg = 'Timeout when reading stderr from host {}, cmd={}: {}'\
                .format(self.host, cmd, str(timeout_error))
            self.log.error(msg)
            raise SshError(msg)
        if stdout.channel.recv_exit_status() != 0 and err:
            if err.splitlines():
                msg = "CLI access: \nHost: {}\nCommand: {}\nError: {}\n"
                msg = msg.format(self.host, cmd, err)
                self.log.error(msg)
                stderr.close()
                stdout.close()
                raise SshError(msg)

        try:
            ret = self.binary2str(stdout.read())
        except (paramiko.buffered_pipe.PipeTimeout, socket.timeout) \
                as timeout_error:
            msg = 'Timeout when reading stdout from host {}, cmd={}: {}' \
                .format(self.host, cmd, str(timeout_error))
            self.log.error(msg)
            raise SshError(msg)
        stderr.close()
        stdout.close()
        return ret

    def copy_file(self, local_path: str, remote_path: str, mode=None):
        if not self.connect():
            return
        if not self.ftp:
            self.ftp = self.ssh_client.open_sftp()
        try:
            self.ftp.put(local_path, remote_path)
        except IOError as e:
            msg = 'SFTP copy_file failed to copy file: ' \
                  'local: {}, remote host: {}, error: {}' \
                .format(local_path, self.host, str(e))
            self.log.error(msg)
            raise SshError(msg)
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
                           ', port: ' + str(self.port) +
                           ', error: ' + str(e))
            return str(e)
        self.log.info('SFTP copy_file success: '
                      'host={},port={},{} -> {}'
                      .format(self.host, str(self.port), local_path,
                              remote_path))
        return ''

    def copy_file_from_remote(self, remote_path, local_path):
        if not self.connect():
            return
        if not self.ftp:
            self.ftp = self.ssh_client.open_sftp()
        try:
            self.ftp.get(remote_path, local_path)
        except IOError as e:
            msg = 'SFTP copy_file_from_remote failed to copy file: ' \
                  'remote host: {}, remote_path: {}, local: {}, error: {}'
            msg = msg.format(self.host, remote_path, local_path, str(e))
            self.log.error(msg)
            raise SshError(msg)
        self.log.info('SFTP copy_file_from_remote success: host={},{} -> {}'.
                      format(self.host, remote_path, local_path))
        return ''

    def is_gateway_host(self, host):
        return True
