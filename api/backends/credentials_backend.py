###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json

from api.backends.auth_backend import AuthBackend


class CredentialsBackend(AuthBackend):

    def __init__(self, config_file: str):
        with open(config_file) as f:
            file_contents = json.load(f)

        if isinstance(file_contents, dict):
            file_contents = [file_contents]

        # TODO: stronger requirements
        self.user_list = [
            {"username": user["username"], "password": user["password"]}
            for user in file_contents
        ]

    def authenticate_user(self, username, password):
        # TODO: hash password
        for user in self.user_list:
            if username == user['username'] and password == user['password']:
                return True
        return False
