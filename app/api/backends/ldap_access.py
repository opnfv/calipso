###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import ssl

from ldap3 import Server, Connection, Tls

from utils.config_file import ConfigFile
from utils.logging.full_logger import FullLogger
from utils.singleton import Singleton


class LDAPAccess(metaclass=Singleton):

    default_config_file = "ldap.conf"
    TLS_REQUEST_CERTS = {
        "demand": ssl.CERT_REQUIRED,
        "allow": ssl.CERT_OPTIONAL,
        "never": ssl.CERT_NONE,
        "default": ssl.CERT_NONE
    }
    user_ssl = True

    def __init__(self, config_file_path=""):
        super().__init__()
        self.log = FullLogger()
        self.ldap_params = self.get_ldap_params(config_file_path)
        self.server = self.connect_ldap_server()

    def get_ldap_params(self, config_file_path):
        ldap_params = {
            "url": "ldap://localhost:389"
        }
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

    def connect_ldap_server(self):
        ca_certificate_file = self.ldap_params.get('tls_cacertfile')
        req_cert = self.ldap_params.get('tls_req_cert')
        ldap_url = self.ldap_params.get('url')

        if ca_certificate_file:
            if not req_cert or req_cert not in self.TLS_REQUEST_CERTS.keys():
                req_cert = 'default'
            tls_req_cert = self.TLS_REQUEST_CERTS[req_cert]
            tls = Tls(local_certificate_file=ca_certificate_file,
                      validate=tls_req_cert)
            return Server(ldap_url, use_ssl=self.user_ssl, tls=tls)

        return Server(ldap_url, use_ssl=self.user_ssl)

    def authenticate_user(self, username, password):
        if not self.server:
            self.server = self.connect_ldap_server()

        user_dn = self.ldap_params['user_id_attribute'] + "=" + username + \
                  "," + self.ldap_params['user_tree_dn']
        connection = Connection(self.server, user=user_dn, password=password)
        # validate the user by binding
        # bound is true if binding succeed, otherwise false
        bound = False
        try:
            bound = connection.bind()
            connection.unbind()
        except Exception as e:
            self.log.error('Failed to bind the server for {0}'.format(str(e)))

        return bound
