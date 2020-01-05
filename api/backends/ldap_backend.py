###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import ssl

from ldap3 import Server, Connection, Tls

from api.backends.auth_backend import AuthBackend
from base.utils.config_file import ConfigFile
from base.utils.logging.full_logger import FullLogger
from base.utils.util import read_environment_variables


class LDAPBackend(AuthBackend):

    default_config_file = "ldap.conf"
    TLS_REQUEST_CERTS = {
        "demand": ssl.CERT_REQUIRED,
        "allow": ssl.CERT_OPTIONAL,
        "never": ssl.CERT_NONE,
        "default": ssl.CERT_NONE
    }
    user_ssl = True

    REQUIRED_ENV_VARIABLES = {
        'user_tree_dn': 'CALIPSO_LDAP_SERVICE_USER_TREE_DN',
        'user_id_attribute': 'CALIPSO_LDAP_SERVICE_USER_ID_ATTRIBUTE',
    }
    OPTIONAL_ENV_VARIABLES = {
        'user': 'CALIPSO_LDAP_SERVICE_USER',
        'password': 'CALIPSO_LDAP_SERVICE_PWD',
        'url': 'CALIPSO_LDAP_SERVICE_URL',
        'user_pass_attribute': 'CALIPSO_LDAP_SERVICE_USER_PASS_ATTRIBUTE',
        'user_objectclass': 'CALIPSO_LDAP_SERVICE_USER_OBJECTCLASS',
        'query_scope': 'CALIPSO_LDAP_SERVICE_QUERY_SCOPE',
        'tls_req_cert': 'CALIPSO_LDAP_SERVICE_TLS_REQ_CERT',
        'tls_cacertfile': 'CALIPSO_LDAP_SERVICE_TLS_CACERTFILE',
        'group_member_attribute': 'CALIPSO_LDAP_SERVICE_GROUP_MEMBER_ATTRIBUTE'
    }

    def __init__(self, config_file_path=""):
        super().__init__()
        self.log = FullLogger()
        self._ldap_params = {
            "url": "ldap://localhost:389"
        }
        self._ldap_params.update(self._get_ldap_params(config_file_path))
        self._server = self._connect_ldap_server()

    # Try to read ldap config from environment variables
    def _read_config_from_env_vars(self):
        try:
            return read_environment_variables(
                required=self.REQUIRED_ENV_VARIABLES,
                optional=self.OPTIONAL_ENV_VARIABLES
            )
        except ValueError:
            return {}

    def _get_ldap_params(self, config_file_path):
        ldap_params = self._read_config_from_env_vars()
        if ldap_params:
            return ldap_params

        if not config_file_path:
            config_file_path = ConfigFile.get(self.default_config_file)
        if config_file_path:
            try:
                config_file = ConfigFile(config_file_path)
                params = config_file.read_config()
                ldap_params.update(params)
            except Exception as e:
                self.log.error(str(e))
                raise
        if "user_tree_dn" not in ldap_params:
            raise ValueError("user_tree_dn must be specified in " +
                             config_file_path)
        if "user_id_attribute" not in ldap_params:
            raise ValueError("user_id_attribute must be specified in " +
                             config_file_path)
        return ldap_params

    def _connect_ldap_server(self):
        ca_certificate_file = self._ldap_params.get('tls_cacertfile')
        req_cert = self._ldap_params.get('tls_req_cert')
        ldap_url = self._ldap_params.get('url')

        if ca_certificate_file:
            if not req_cert or req_cert not in self.TLS_REQUEST_CERTS.keys():
                req_cert = 'default'
            tls_req_cert = self.TLS_REQUEST_CERTS[req_cert]
            tls = Tls(local_certificate_file=ca_certificate_file,
                      validate=tls_req_cert)
            return Server(ldap_url, use_ssl=self.user_ssl, tls=tls)

        return Server(ldap_url, use_ssl=self.user_ssl)

    def authenticate_user(self, username, pwd):
        if not self._server:
            self._server = self._connect_ldap_server()

        user_dn = self._ldap_params['user_id_attribute'] + "=" + \
                  username + "," + self._ldap_params['user_tree_dn']
        connection = Connection(self._server, user=user_dn, password=pwd)
        # validate the user by binding
        # bound is true if binding succeed, otherwise false
        bound = False
        try:
            bound = connection.bind()
            connection.unbind()
        except Exception as e:
            self.log.error('Failed to bind the server for {0}'.format(str(e)))

        return bound
