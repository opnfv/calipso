###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from flask import make_response, jsonify, request


class Responder:

    def __init__(self):
        self.request_type = ''
        self.request_data = dict()
        self.error = None

    @staticmethod
    def get_error_response(error: str = None, code: int = 200):
        return make_response(jsonify({'error': error}), code)

    @staticmethod
    def get_data_response(data):
        return make_response(jsonify({'data': data}))

    def reset_request_data(self):
        self.request_data = None

    def get_request_data(self):
        if self.request_data:
            return self.request_data
        self.request_type = request.environ['CONTENT_TYPE']
        # remove trailing ';..' from request type
        self.request_type = self.request_type.split(';', 1)[0]
        # json post data
        form_data_formats = [
            'multipart/form-data',
            'application/x-www-form-urlencoded'
        ]
        if request.method == "GET":
            self.request_data = request.args
        # the following is relevant only when method is 'POST':
        elif self.request_type == 'application/json':
            self.request_data = request.get_json()
        # form post data:
        elif self.request_type in form_data_formats:
            self.request_data = request.form
        else:
            self.error = 'get_request_data(): handling not implemented' + \
                'for request method {} and request type {}' \
                .format(request.method, self.request_type)
            return None
        return self.request_data

    def get_param(self, param: str, default_val = None) -> str:
        req_data = self.get_request_data()
        val = req_data.get(param, default_val)
        return val

    def get_request_param(self, param: str, default_val = None) -> bool:
        val = self.get_param(param, default_val=default_val)
        if val is None:
            return False
        setattr(self, param, val)
        return True
