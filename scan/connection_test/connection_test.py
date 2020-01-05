###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

# This is a connection-test used for testing environment config targets
# it can be used for functional testing,
# as well as for environment testing sent from the UI or API
import socket

import amqp
import paramiko
import requests
import argparse
import datetime

import urllib3
from kombu import Connection
import time
import pymongo
from functools import partial

from kubernetes.client.rest import ApiException as KubeApiException
from scan.fetchers.aci.aci_access import AciAccess
from scan.fetchers.api.api_access import ApiAccess
from scan.fetchers.db.db_access import DbAccess
from scan.fetchers.kube.kube_access import KubeAccess
from scan.manager import Manager
from base.utils.constants import ConnectionTestStatus, ConnectionTestType
from base.utils.exceptions import HostAddressError, CredentialsError, SshKeyError
from base.utils.logging.file_logger import FileLogger
from base.utils.mongo_access import MongoAccess
from base.utils.ssh_connection import SshConnection


def test_openstack(config, test_request):
    try:
        ApiAccess.reset()
        ApiAccess(config)
        ConnectionTest.report_success(test_request,
                                      ConnectionTestType.OPENSTACK.value)
    except requests.ConnectionError:
        raise HostAddressError()


def test_mysql(config, test_request):
    DbAccess.close_connection()
    db_access = DbAccess(config, force_connect=True)
    ConnectionTest.report_success(test_request, ConnectionTestType.MYSQL.value)
    if db_access:
        pass


def test_ssh_connect(config) -> bool:
    SshConnection.disconnect_all()
    ssh = SshConnection(config.get('host', ''),
                        config.get('user', ''),
                        _pwd=config.get('pwd'),
                        _key=config.get('key'),
                        _port=int(config.get('port',
                                             SshConnection.DEFAULT_PORT)))
    try:
        ret = ssh.connect()
    except socket.timeout:
        raise HostAddressError()
    except paramiko.ssh_exception.SSHException:
        raise SshKeyError()
    # TODO: SshConnection class should raise an exception
    if not ret:
        raise CredentialsError()

    return ret


def test_cli(config, test_request):
    ret = test_ssh_connect(config)
    ConnectionTest.set_test_result(test_request,
                                   ConnectionTestType.CLI.value,
                                   ret)


def test_amqp_connect(config):
    connect_url = 'amqp://{user}:{pwd}@{host}:{port}//' \
        .format(user=config.get("user", ''),
                pwd=config.get('pwd', ''),
                host=config.get('host', ''),
                port=int(config.get('port', 5671)))

    conn = Connection(connect_url)
    try:
        conn.connect()
    except socket.timeout:
        raise HostAddressError()
    except amqp.exceptions.AccessRefused:
        raise CredentialsError()


def test_amqp(config, test_request):
    test_amqp_connect(config)
    ConnectionTest.report_success(test_request, ConnectionTestType.AMQP.value)


def test_monitoring(config, test_request):
    # for monitoring configuration test, need to test:
    # 1. SSH access
    # 2. RabbitMQ access
    ssh_config = {
        'host': config.get('server_ip'),
        'user': config.get('ssh_user'),
        'pwd': config.get('ssh_password'),
        'port': int(config.get('ssh_port', 0))
    }
    if not test_ssh_connect(ssh_config):
        return
    ConnectionTest.report_success(test_request, ConnectionTestType.MONITORING.value)


def test_aci(config, test_request):
    aci_access = AciAccess(config)
    try:
        aci_access.login()
    except requests.ConnectTimeout:
        raise HostAddressError()
    except requests.HTTPError as e:
        if e.response.status_code == requests.codes.UNAUTHORIZED:
            raise CredentialsError()
        else:
            raise e
    ConnectionTest.report_success(test_request, ConnectionTestType.ACI.value)


def test_kubernetes(config, test_request):
    kube_access = KubeAccess(config)
    try:
        kube_access.api.list_namespace(watch=False, _request_timeout=3)
    except urllib3.exceptions.MaxRetryError:
        raise HostAddressError()
    except KubeApiException as e:
        if e.status == requests.codes.UNAUTHORIZED:
            raise CredentialsError()
        else:
            raise e
    ConnectionTest.report_success(test_request,
                                  ConnectionTestType.KUBERNETES.value)


TEST_HANDLERS = {
    ConnectionTestType.OPENSTACK.value: test_openstack,
    ConnectionTestType.MYSQL.value: test_mysql,
    ConnectionTestType.CLI.value: test_cli,
    ConnectionTestType.AMQP.value: test_amqp,
    ConnectionTestType.ACI.value: test_aci,
    ConnectionTestType.MONITORING.value: test_monitoring,
    ConnectionTestType.KUBERNETES.value: test_kubernetes
}


class ConnectionTest(Manager):

    DEFAULTS = {
        'mongo_config': '',
        'connection_tests': 'connection_tests',
        'environments': 'environments_config',
        'interval': 1,
        'loglevel': 'WARNING'
    }

    def __init__(self):
        self.args = self.get_args()
        super().__init__(log_directory=self.args.log_directory,
                         mongo_config_file=self.args.mongo_config)
        self.db_client = None
        self.connection_tests_collection = None
        self.environments_collection = None

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('-m', '--mongo_config', nargs='?', type=str,
                            default=ConnectionTest.DEFAULTS['mongo_config'],
                            help='Name of config file ' +
                                 'with MongoDB server access details')
        parser.add_argument('-c', '--connection_tests_collection', nargs='?',
                            type=str,
                            default=ConnectionTest.DEFAULTS['connection_tests'],
                            help='connection_tests collection to read from')
        parser.add_argument('-e', '--environments_collection', nargs='?',
                            type=str,
                            default=ConnectionTest.DEFAULTS['environments'],
                            help='Environments collection to update '
                                 'after tests')
        parser.add_argument('-i', '--interval', nargs='?', type=float,
                            default=ConnectionTest.DEFAULTS['interval'],
                            help='Interval between collection polls'
                                 '(must be more than {} seconds)'
                                 .format(ConnectionTest.MIN_INTERVAL))
        parser.add_argument('-l', '--loglevel', nargs='?', type=str,
                            default=ConnectionTest.DEFAULTS['loglevel'],
                            help='Logging level \n(default: {})'
                                 .format(ConnectionTest.DEFAULTS['loglevel']))
        parser.add_argument('-d', '--log_directory', nargs='?', type=str,
                            default=FileLogger.LOG_DIRECTORY,
                            help='File logger directory \n(default: {})'
                                 .format(FileLogger.LOG_DIRECTORY))
        args = parser.parse_args()
        return args

    def configure(self):
        self.db_client = MongoAccess()
        self.connection_tests_collection = \
            self.db_client.db[self.args.connection_tests_collection]
        self.environments_collection = \
            self.db_client.db[self.args.environments_collection]
        self._update_document = \
            partial(MongoAccess.update_document,
                    self.connection_tests_collection)
        self.interval = max(self.MIN_INTERVAL, self.args.interval)
        self.log.set_loglevel(self.args.loglevel)

        self.log.info('Started ConnectionTest with following configuration:\n'
                      '{1}\n'
                      'connection_tests collection: '
                      '{0.connection_tests_collection.name}\n'
                      'Polling interval: {0.interval} second(s)'
                      .format(self, MongoAccess.get_source_text()))

    def _build_test_args(self, test_request: dict):
        args = {
            'mongo_config': self.args.mongo_config
        }

        def set_arg(name_from: str, name_to: str = None):
            if name_to is None:
                name_to = name_from
            val = test_request.get(name_from)
            if val:
                args[name_to] = val

        set_arg('object_id', 'id')
        set_arg('log_level', 'loglevel')
        set_arg('environment', 'env')
        set_arg('scan_only_inventory', 'inventory_only')
        set_arg('scan_only_links', 'links_only')
        set_arg('scan_only_cliques', 'cliques_only')
        set_arg('inventory')
        set_arg('clear')
        set_arg('clear_all')

        return args

    def _finalize_test(self, test_request: dict):
        # update the status and timestamps.
        self.log.info('Request {} has been tested.'
                      .format(test_request['_id']))
        start_time = test_request['submit_timestamp']
        if isinstance(start_time, str):
            start_time = datetime.datetime. \
                strptime(start_time, '%Y-%m-%dT%H:%M:%S%z')
        end_time = datetime.datetime.utcnow()
        test_request['response_timestamp'] = end_time
        test_request['response_time'] = \
            str(end_time - start_time.replace(tzinfo=None))
        test_request['status'] = ConnectionTestStatus.RESPONSE.value
        self._update_document(test_request)

    @staticmethod
    def set_test_result(test_request, target, result):
        test_request.get('test_results', {})[target] = result

    @staticmethod
    def report_success(test_request, target):
        ConnectionTest.set_test_result(test_request, target, True)

    @staticmethod
    def handle_test_target(target, test_request):
        targets_config = test_request.get('targets_configuration', [])
        try:
            config = next(t for t in targets_config if t['name'] == target)
        except StopIteration:
            raise ValueError('failed to find {} in targets_configuration'
                             .format(target))
        handler = TEST_HANDLERS.get(target)
        if not handler:
            raise ValueError('unknown test target: {}'.format(target))
        handler(config, test_request)

    def do_test(self, test_request):
        targets = [t for t in test_request.get('test_targets', [])]
        test_request['test_results'] = {t: False for t in targets}
        test_request['errors'] = {}
        for test_target in test_request.get('test_targets', []):
            self.log.info('testing connection to: {}'.format(test_target))
            try:
                self.handle_test_target(test_target, test_request)
            except Exception as e:
                self.log.exception(e)
                test_request['errors'][test_target] = str(e)
                self.log.error('Test of target {} failed (id: {}):\n{}'
                               .format(test_target,
                                       test_request['_id'],
                                       str(e)))
        self._finalize_test(test_request)
        self._set_env_operational(test_request['environment'])

    # if environment_config document for this specific environment exists,
    # update the value of the 'operational' field to 'running'
    def _set_env_operational(self, env):
        self.environments_collection. \
            update_one({'name': env}, {'$set': {'operational': 'running'}})

    def do_action(self):
        while True:
            # Find a pending request that is waiting the longest time
            results = self.connection_tests_collection \
                .find({'status': ConnectionTestStatus.REQUEST.value,
                       'submit_timestamp': {'$ne': None}}) \
                .sort('submit_timestamp', pymongo.ASCENDING) \
                .limit(1)

            # If no connection tests are pending, sleep for some time
            if results.count() == 0:
                time.sleep(self.interval)
            else:
                self.do_test(results[0])


if __name__ == '__main__':
    ConnectionTest().run()
