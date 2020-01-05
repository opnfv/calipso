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
from ldap3.core.exceptions import LDAPException

from api.ldap_api.config_file import ConfigFile
from api.ldap_api.console_logger import ConsoleLogger
from api.ldap_api.singleton import Singleton


class LDAPAccess(metaclass=Singleton):

    EMPLOYEE = 'employee'
    CUSTOMER = 'customer'

    config_file_path = None

    TLS_REQUEST_CERTS = {
        "demand": ssl.CERT_REQUIRED,
        "allow": ssl.CERT_OPTIONAL,
        "never": ssl.CERT_NONE,
        "default": ssl.CERT_NONE
    }
    user_ssl = True

    def __init__(self, config_file_path: str):
        super().__init__()
        if not config_file_path:
            raise ValueError('LDAPAccess: config file path must be provided')
        self.log = ConsoleLogger()
        self.ldap_params = self.get_ldap_params(config_file_path)
        self.server = self.connect_ldap_server()

    @staticmethod
    def set_config_file(config_file: str = None):
        if config_file:
            LDAPAccess.config_file_path = config_file

    def get_ldap_params(self, config_file_path):
        ldap_params = {}
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

    def connect_to_server(self):
        if not self.server:
            self.server = self.connect_ldap_server()
        id_attribute = self.ldap_params['user_id_attribute']
        user_tree_dn = self.ldap_params['user_tree_dn']
        admin_tree_dn = self.ldap_params.get('admin_tree_dn', user_tree_dn)
        adminuser = self.ldap_params['user']
        adminpass = self.ldap_params['password']
        admin_dn = '{}={},{}'.format(id_attribute, adminuser, admin_tree_dn)
        try:
            connection = Connection(self.server, user=admin_dn,
                                    password=adminpass, auto_bind=True)
        except LDAPException as e:
            self.log.error('Failed to connect to the LDAP server: {}'
                           .format(str(e)))
            return None
        return connection

    def get_user_dn(self, cn: str):
        user_tree_dn = self.ldap_params['user_tree_dn']
        user_dn = 'cn={},{}'.format(cn, user_tree_dn)
        return user_dn

    def auth_user(self, username, pwd, login_type=CUSTOMER) -> bool:
        if not self.server:
            self.server = self.connect_ldap_server()
        id_attribute = self.ldap_params['user_id_attribute']
        user_tree_dn = self.ldap_params['user_tree_dn']
        user_dn = '{}={},OU=engineering,{}' \
            .format(id_attribute, username, user_tree_dn) \
            if login_type == self.EMPLOYEE \
            else '{}={},{}'.format(id_attribute, username, user_tree_dn)
        connection = Connection(self.server, user=user_dn, password=pwd)
        # validate the user by binding
        # bound is true if binding succeed, otherwise false
        try:
            auth_result = connection.bind()
            connection.unbind()
        except Exception as e:
            self.log.error('Failed to bind the server for {0}'.format(str(e)))
            return False
        return auth_result

    def add_user(self, req_data):
        try:
            cn = req_data["cn"]
            uid = req_data["uid"]
            name = req_data["name"]
            sn = req_data["sn"]
            password = req_data["password"]
            department = req_data["department"]
            telephone = req_data["telephone"]
        except KeyError:
            return False
        connection = self.connect_to_server()
        if not connection:
            return False
        # add the user to ldap after binding as admin
        # bound is true if user add was succeed, otherwise false
        try:
            user_dn = self.get_user_dn(cn)
            attribute_map = {
                'uid': uid,
                'givenName': name,
                'sn': sn,
                'userpassword': password,
                'departmentNumber': department,
                'telephoneNumber': telephone
            }
            user_objectclass = self.ldap_params['user_objectclass']
            added = connection.add(user_dn, user_objectclass, attribute_map)
            connection.unbind()
        except Exception as e:
            self.log.error('Failed to bind the server for {0}'.format(str(e)))
            added = False
        return added

    def del_user(self, req_data) -> bool:
        try:
            cn = req_data["cn"]
        except KeyError:
            return False
        if not self.server:
            self.server = self.connect_ldap_server()
        connection = self.connect_to_server()
        if not connection:
            return False
        # delete the user from ldap after binding as admin
        # bound is true if user add was succeed, otherwise false
        try:
            user_dn = self.get_user_dn(cn)
            user_deleted = connection.delete(user_dn)
            connection.unbind()
        except Exception as e:
            self.log.error('Failed to bind the server for {0}'.format(str(e)))
            return False
        return user_deleted

    def get_user(self, cn):
        if not self.connect_ldap_server():
            return None
        if not self.server:
            self.server = self.connect_ldap_server()
        connection = self.connect_to_server()
        # get the user from ldap after binding as admin
        # found is true if user details were found, otherwise false
        try:
            user_tree_dn = self.ldap_params['user_tree_dn']
            attributes_to_fetch = ['cn', 'sn', 'uid', 'givenName',
                                   'departmentNumber', 'telephoneNumber',
                                   'objectclass']
            search_query = '(&(objectclass=person)(cn={}))'.format(cn)
            found = connection.search(user_tree_dn, search_query,
                                      attributes=attributes_to_fetch)
            if found:
                entry = connection.entries[0]
                entry_dict = entry.entry_attributes_as_dict
                connection.unbind()
                return entry_dict
            else:
                connection.unbind()
                return None
        except Exception as e:
            self.log.error('Failed to bind the server for {0}'.format(str(e)))
