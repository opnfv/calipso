###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from flask import request

from werkzeug.security import safe_str_cmp
from api.ldap_api.ldap_access import LDAPAccess
from api.ldap_api.responder import Responder


class Users(Responder):

    class User(object):
        def __init__(self, user_id, username, password):
            self.id = user_id
            self.username = username
            self.password = password

        def __str__(self):
            return "User(id='{}')".format(self.id)

    def __init__(self, conf_file_path):
        super().__init__()
        # table used for token generation per administrator
        api_users = [
            Users.User(1, 'admin', 'password')
        ]
        self.username_table = {u.username: u for u in api_users}
        self.user_id_table = {u.id: u for u in api_users}
        self.ldap = LDAPAccess(config_file_path=conf_file_path)

    def get_user_data(self, user_cn: str):
        user_data = self.ldap.get_user(user_cn)
        return user_data

    def get_user(self):
        user_cn = self.get_param('cn')
        if not user_cn:
            return self.get_error_response(error='cn missing')
        user_data = self.get_user_data(user_cn)
        if not user_data:
            return self.get_error_response(error='user not found')
        return self.get_data_response(user_data)

    def del_user(self):
        req_data = request.get_json()
        user_deleted = self.ldap.del_user(req_data)
        if not user_deleted:
            msg = "Invalid details or user not found"
            return self.get_error_response(error=msg)
        return self.get_data_response(user_deleted)

    def add_user(self):
        req_data = request.get_json()
        user_added = self.ldap.add_user(req_data)
        if not user_added:
            msg = "Invalid details or user already exists"
            return self.get_error_response(error=msg)
        return self.get_data_response(user_added)

    def authenticate(self, username, password):
        # security check: validate username and password,
        # use safe encoding and not some embedded code
        user = self.username_table.get(username, None)
        print(user)
        if user and safe_str_cmp(user.password.encode('utf-8'),
                                 password.encode('utf-8')):
            return user

    def identity(self, payload):
        user_id = payload['identity']
        return self.user_id_table.get(user_id, None)

    def check_login(self, login_type=LDAPAccess.CUSTOMER):
        req_data = request.get_json()
        username = req_data.get('username')
        password = req_data.get('password')
        if not username or not password:
            return self.get_error_response("error in request")
        authenticated = self.ldap.auth_user(username, password,
                                            login_type=login_type)
        if not authenticated:
            return self.get_error_response(error="Invalid credentials")
        return self.get_data_response(authenticated)
