###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from api.validation.data_validate import DataValidate
from api.responders.responder_base import ResponderBase
from bson.objectid import ObjectId
from datetime import datetime


class Scans(ResponderBase):
    def __init__(self):
        super().__init__()
        self.COLLECTION = "scans"
        self.ID = "_id"
        self.PROJECTION = {
            self.ID: True,
            "environment": True,
            "status": True,
            "scan_completed": True
        }

    def on_get(self, req, resp):
        self.log.debug("Getting scans")
        filters = self.parse_query_params(req)

        scan_statuses = self.get_constants_by_name("scan_statuses")
        filters_requirements = {
            "env_name": self.require(str, mandatory=True),
            "id": self.require(ObjectId, True),
            "base_object": self.require(str),
            "status": self.require(str, False, DataValidate.LIST, scan_statuses),
            "page": self.require(int, True),
            "page_size": self.require(int, True)
        }

        self.validate_query_data(filters, filters_requirements)
        page, page_size = self.get_pagination(filters)

        query = self.build_query(filters)
        if "_id" in query:
            scan = self.get_object_by_id(self.COLLECTION, query,
                                         [ObjectId, datetime], self.ID)
            self.set_successful_response(resp, scan)
        else:
            scans_ids = self.get_objects_list(self.COLLECTION, query,
                                              page, page_size, self.PROJECTION)
            self.set_successful_response(resp, {"scans": scans_ids})

    def on_post(self, req, resp):
        self.log.debug("Posting new scan")
        error, scan = self.get_content_from_request(req)
        if error:
            self.bad_request(error)

        scan_statuses = self.get_constants_by_name("scan_statuses")
        log_levels = self.get_constants_by_name("log_levels")

        scan_requirements = {
            "status": self.require(str,
                                   validate=DataValidate.LIST,
                                   requirement=scan_statuses,
                                   mandatory=True),
            "log_level": self.require(str,
                                      validate=DataValidate.LIST,
                                      requirement=log_levels),
            "clear": self.require(bool, True),
            "scan_only_inventory": self.require(bool, True),
            "scan_only_links": self.require(bool, True),
            "scan_only_cliques": self.require(bool, True),
            "environment": self.require(str, mandatory=True),
            "inventory": self.require(str),
            "object_id": self.require(str)
        }
        self.validate_query_data(scan, scan_requirements)
        scan_only_keys = [k for k in scan if k.startswith("scan_only_")]
        if len(scan_only_keys) > 1:
            self.bad_request("multiple scan_only_* flags found: {0}. "
                             "only one of them can be set."
                             .format(", ".join(scan_only_keys)))

        env_name = scan["environment"]
        if not self.check_environment_name(env_name):
            self.bad_request("unkown environment: " + env_name)

        scan["scan_completed"] = False
        scan["submit_timestamp"] = datetime.now()
        self.write(scan, self.COLLECTION)
        self.set_successful_response(resp,
                                     {"message": "created a new scan for "
                                                 "environment {0}"
                                                 .format(env_name)},
                                     "201")

    def build_query(self, filters):
        query = {}
        filters_keys = ["status"]
        self.update_query_with_filters(filters, filters_keys, query)
        base_object = filters.get("base_object")
        if base_object:
            query['object_id'] = base_object
        _id = filters.get("id")
        if _id:
            query['_id'] = _id
        query['environment'] = filters['env_name']
        return query
