###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from api.auth.token import Token
from api.backends.ldap_access import LDAPAccess
from utils.inventory_mgr import InventoryMgr
from utils.logging.full_logger import FullLogger


class Auth:

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()
        self.log = FullLogger()
        self.tokens_coll = self.inv.client['tokens']['api_tokens']
        self.ldap_access = LDAPAccess()

    def get_token(self, token):
        tokens = None
        try:
            tokens = list(self.tokens_coll.find({'token': token}))
        except Exception as e:
            self.log.error('Failed to get token for ', str(e))

        return tokens

    def write_token(self, token):
        error = None
        try:
            self.tokens_coll.insert_one(token)
        except Exception as e:
            self.log.error("Failed to write new token {0} to database for {1}"
                           .format(token[token], str(e)))
            error = 'Failed to create new token'

        return error

    def delete_token(self, token):
        error = None
        try:
            self.tokens_coll.delete_one({'token': token})
        except Exception as e:
            self.log.error('Failed to delete token {0} for {1}'.
                           format(token, str(e)))
            error = 'Failed to delete token {0}'.format(token)

        return error

    def validate_credentials(self, username, pwd):
        return self.ldap_access.authenticate_user(username, pwd)

    def validate_token(self, token):
        error = None
        tokens = self.get_token(token)
        if not tokens:
            error = "Token {0} doesn't exist".format(token)
        elif len(tokens) > 1:
            self.log.error('Multiple tokens found for {0}'.format(token))
            error = "Multiple tokens found"
        else:
            t = tokens[0]
            error = Token.validate_token(t)

        return error
