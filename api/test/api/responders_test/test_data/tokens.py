###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
URL = '/auth/tokens'

AUTH_OBJ_WITHOUT_AUTH = {

}

AUTH_OBJ_WITHOUT_METHODS = {
    'auth': {}
}

AUTH_OBJ_WITHOUT_CREDENTIALS = {
    'auth': {
        'methods': ['credentials']
    }
}

AUTH_OBJ_WITHOUT_TOKEN = {
    'auth': {
        'methods': ['token']
    }
}

AUTH_OBJ_WITH_WRONG_CREDENTIALS = {
    'auth': {
        'methods': ['credentials'],
        'credentials': {
            'username': 'wrong_user',
            'password': 'password'
        }
    }
}

AUTH_OBJ_WITH_WRONG_TOKEN = {
    'auth': {
        'methods': ['token'],
        'token': 'wrong_token'
    }
}

AUTH_OBJ_WITH_CORRECT_CREDENTIALS = {
    'auth': {
        'methods': ['credentials'],
        'credentials': {
            'username': 'wrong_user',
            'password': 'password'
        }
    }
}

AUTH_OBJ_WITH_CORRECT_TOKEN = {
    'auth': {
        'methods': ['token'],
        'token': '17dfa88789aa47f6bb8501865d905f13'
    }
}

HEADER_WITHOUT_TOKEN = {

}

HEADER_WITH_WRONG_TOKEN = {
    'X-Auth-Token': 'wrong token'
}

HEADER_WITH_CORRECT_TOKEN = {
    'X-Auth-Token': '17dfa88789aa47f6bb8501865d905f13'
}

AUTH_BASE_PATH = 'api.auth.auth.Auth'
AUTH_GET_TOKEN = AUTH_BASE_PATH + '.get_token'
AUTH_WRITE_TOKEN = AUTH_BASE_PATH + '.write_token'
AUTH_DELETE_TOKEN = AUTH_BASE_PATH + '.delete_token'
AUTH_VALIDATE_CREDENTIALS = AUTH_BASE_PATH + '.validate_credentials'
AUTH_VALIDATE_TOKEN = AUTH_BASE_PATH + '.validate_token'
