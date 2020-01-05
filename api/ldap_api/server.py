###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import argparse
import ssl
from datetime import timedelta

from flask import Flask
from flask_jwt import JWT, jwt_required
from api.ldap_api.ldap_access import LDAPAccess
from api.ldap_api.users import Users


default_home_dir = '/local_dir'
default_ldap_conf_file = '{}/ldap_access.conf'.format(config_dir)

DEFAULT_APP_PORT = "5000"
REPO_NAME = "calipso"
APP_DOMAIN = "calipso.cisco.com"
PROJECT_NAME = "Calipso"
app_dir = '{}/{}'.format(default_home_dir, REPO_NAME)
default_bind_address = '{}:{}'.format(APP_DOMAIN, DEFAULT_APP_PORT)


def get_args():
    parser_desc = "Parameters for {} API".format(PROJECT_NAME)
    parser = argparse.ArgumentParser(description=parser_desc)
    parser.add_argument("-l", "--ldap_config", nargs="?", type=str,
                        default=default_ldap_conf_file,
                        help="name of the config file with ldap server "
                             "config details")
    parser.add_argument("-b", "--bind", nargs="?", type=str,
                        default=default_bind_address,
                        help="binding address of the API server\n"
                             "(default calipso.cisco.com:5000)")
    # note: we should change this to 127.0.0.1:5000 once development is done
    parser.add_argument("-t", "--tokenlife", nargs="?", type=int,
                        default=900,
                        help="lifetime of the token")
    program_args = parser.parse_args()
    return program_args


args = get_args()

settings = {'SERVER_NAME': args.bind}
app = Flask(__name__)
app.config.update(settings)
app.config['SECRET_KEY'] = 'string-to-create-token-hash'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=args.tokenlife)

user_access = Users(args.ldap_config)
jwt = JWT(app, user_access.authenticate, user_access.identity)
translations_responder = Translations()

# security in flask


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('{}/calipso_api.crt'.format(config_dir),
                        '{}/calipso_api.key'.format(config_dir))

# users section


@app.route('/login', methods=['POST'])
@jwt_required()
def login():
    user_access.reset_request_data()
    return user_access.check_login(login_type=LDAPAccess.CUSTOMER)


@app.route('/admin_login', methods=['POST'])
@jwt_required()
def admin_login():
    user_access.reset_request_data()
    return user_access.check_login(login_type=LDAPAccess.EMPLOYEE)


@app.route('/add_user', methods=['POST'])
@jwt_required()
def add_user():
    user_access.reset_request_data()
    return user_access.add_user()


@app.route('/del_user', methods=['POST'])
@jwt_required()
def del_user():
    user_access.reset_request_data()
    return user_access.del_user()


@app.route('/get_user', methods=['GET'])
@jwt_required()
def get_user():
    user_access.reset_request_data()
    return user_access.get_user()


if __name__ == "__main__":
    app.run(ssl_context=context)
