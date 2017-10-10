###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json
import re
from urllib import parse

from dateutil import parser
from pymongo import errors

from api.exceptions import exceptions
from api.validation.data_validate import DataValidate
from utils.dict_naming_converter import DictNamingConverter
from utils.inventory_mgr import InventoryMgr
from utils.logging.full_logger import FullLogger
from utils.string_utils import jsonify, stringify_object_values_by_types


class ResponderBase(DataValidate, DictNamingConverter):
    UNCHANGED_COLLECTIONS = ["monitoring_config_templates",
                             "environments_config",
                             "messages",
                             "scheduled_scans"]

    def __init__(self):
        super().__init__()
        self.log = FullLogger()
        self.inv = InventoryMgr()

    def set_successful_response(self, resp, body="", status="200"):
        if not isinstance(body, str):
            try:
                body = jsonify(body)
            except Exception as e:
                self.log.exception(e)
                raise ValueError("The response body should be a string")
        resp.status = status
        resp.body = body

    def set_error_response(self, title="", code="", message="", body=""):
        if body:
            raise exceptions.CalipsoApiException(code, body, message)
        body = {
            "error": {
                "message": message,
                "code": code,
                "title": title
            }
        }
        body = jsonify(body)
        raise exceptions.CalipsoApiException(code, body, message)

    def not_found(self, message="Requested resource not found"):
        self.set_error_response("Not Found", "404", message)

    def conflict(self,
                 message="The posted data conflicts with the existing data"):
        self.set_error_response("Conflict", "409", message)

    def bad_request(self, message="Invalid request content"):
        self.set_error_response("Bad Request", "400", message)

    def unauthorized(self, message="Request requires authorization"):
        self.set_error_response("Unauthorized", "401", message)

    def validate_query_data(self, data, data_requirements,
                            additional_key_reg=None,
                            can_be_empty_keys=[]):
        error_message = self.validate_data(data, data_requirements,
                                           additional_key_reg,
                                           can_be_empty_keys)
        if error_message:
            self.bad_request(error_message)

    def check_and_convert_datetime(self, time_key, data):
        time = data.get(time_key)

        if time:
            time = time.replace(' ', '+')
            try:
                data[time_key] = parser.parse(time)
            except Exception:
                self.bad_request("{0} must follow ISO 8610 date and time format,"
                                 "YYYY-MM-DDThh:mm:ss.sss+hhmm".format(time_key))

    def check_environment_name(self, env_name):
        query = {"name": env_name}
        objects = self.read("environments_config", query)
        if not objects:
            return False
        return True

    def get_object_by_id(self, collection, query, stringify_types, id):
        objs = self.read(collection, query)
        if not objs:
            env_name = query.get("environment")
            if env_name and \
                    not self.check_environment_name(env_name):
                self.bad_request("unknown environment: " + env_name)
            self.not_found()
        obj = objs[0]
        stringify_object_values_by_types(obj, stringify_types)
        if id == "_id":
            obj['id'] = obj.get('_id')
        return obj

    def get_objects_list(self, collection, query, page=0, page_size=1000,
                         projection=None, stringify_types=None):
        objects = self.read(collection, query, projection, page, page_size)
        if not objects:
            env_name = query.get("environment")
            if env_name and \
                    not self.check_environment_name(env_name):
                self.bad_request("unknown environment: " + env_name)
            self.not_found()
        for obj in objects:
            if "id" not in obj and "_id" in obj:
                obj["id"] = str(obj["_id"])
            if "_id" in obj:
                del obj["_id"]
        if stringify_types:
            stringify_object_values_by_types(objects, stringify_types)

        return objects

    def parse_query_params(self, req):
        query_string = req.query_string
        if not query_string:
            return {}
        try:
            query_params = dict((k, v if len(v) > 1 else v[0])
                                for k, v in
                                parse.parse_qs(query_string,
                                               keep_blank_values=True,
                                               strict_parsing=True).items())
            return query_params
        except ValueError as e:
            self.bad_request(str("Invalid query string: {0}".format(str(e))))

    def replace_colon_with_dot(self, s):
        return s.replace(':', '.')

    def get_pagination(self, filters):
        page_size = filters.get('page_size', 1000)
        page = filters.get('page', 0)
        return page, page_size

    def update_query_with_filters(self, filters, filters_keys, query):
        for filter_key in filters_keys:
            filter = filters.get(filter_key)
            if filter is not None:
                query.update({filter_key: filter})

    def get_content_from_request(self, req):
        error = ""
        content = ""
        if not req.content_length:
            error = "No data found in the request body"
            return error, content

        data = req.stream.read()
        content_string = data.decode()
        try:
            content = json.loads(content_string)
            if not isinstance(content, dict):
                error = "The data in the request body must be an object"
        except Exception:
            error = "The request can not be fulfilled due to bad syntax"

        return error, content

    def get_collection_by_name(self, name):
        if name in self.UNCHANGED_COLLECTIONS:
            return self.inv.db[name]
        return self.inv.collections[name]

    def get_constants_by_name(self, name):
        constants = self.get_collection_by_name("constants").\
            find_one({"name": name})
        # consts = [d['value'] for d in constants['data']]
        consts = []
        if not constants:
            self.log.error('constant type: ' + name +
                           'no constants exists')
            return consts
        for d in constants['data']:
            try:
                consts.append(d['value'])
            except KeyError:
                self.log.error('constant type: ' + name +
                               ': no "value" key for data: ' + str(d))
        return consts

    def read(self, collection, matches={}, projection=None, skip=0, limit=1000):
        collection = self.get_collection_by_name(collection)
        skip *= limit
        query = collection.find(matches, projection).skip(skip).limit(limit)
        return list(query)

    def write(self, document, collection="inventory"):
        try:
            return self.get_collection_by_name(collection)\
                       .insert_one(document)
        except errors.DuplicateKeyError as e:
            self.conflict("The key value ({0}) already exists".
                          format(', '.
                                 join(self.get_duplicate_key_values(e.details['errmsg']))))
        except errors.WriteError as e:
            self.bad_request('Failed to create resource for {0}'.format(str(e)))

    def get_duplicate_key_values(self, err_msg):
        return ["'{0}'".format(key) for key in re.findall(r'"([^",]+)"', err_msg)]

    def aggregate(self, pipeline, collection):
        collection = self.get_collection_by_name(collection)
        data = collection.aggregate(pipeline)
        return list(data)
