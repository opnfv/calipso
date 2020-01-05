###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from datetime import datetime

from bson.objectid import ObjectId

from api.responders.responder_base import ResponderBase
from api.validation.data_validate import DataValidate


class Scans(ResponderBase):

    DEFAULT_STATUS = "pending"
    COLLECTION = "scans"
    ID = "_id"
    PROJECTION = {
        ID: True,
        "environment": True,
        "status": True
    }

    def on_get(self, req, resp):
        self.log.debug("Getting scans")
        filters = self.parse_query_params(req)

        scan_statuses = self.get_constants_by_name("scans_statuses")
        filters_requirements = {
            "env_name": self.require(str, mandatory=True),
            "id": self.require(ObjectId, convert_to_type=True),
            "base_object": self.require(str),
            "status": self.require(str,
                                   validate=DataValidate.LIST,
                                   requirement=scan_statuses),
            "page": self.require(int, convert_to_type=True),
            "page_size": self.require(int, convert_to_type=True)
        }

        self.validate_query_data(filters, filters_requirements)
        page, page_size = self.get_pagination(filters)

        query = self.build_query(filters)
        if "_id" in query:
            scan = self.get_object_by_id(self.COLLECTION, query,
                                         [ObjectId, datetime], self.ID)
            self.set_ok_response(resp, scan)
        else:
            scans_ids = self.get_objects_list(self.COLLECTION, query,
                                              page, page_size, self.PROJECTION)
            self.set_ok_response(resp, {"scans": scans_ids})

    def on_post(self, req, resp):
        self.log.debug("Posting new scan")
        error, scan = self.get_content_from_request(req)
        if error:
            self.bad_request(error)

        log_levels = self.get_constants_by_name("log_levels")

        scan_requirements = {
            "log_level": self.require(str,
                                      validate=DataValidate.LIST,
                                      requirement=log_levels),
            "clear": self.require(bool, convert_to_type=True),
            "scan_only_inventory": self.require(bool, convert_to_type=True, default=False),
            "scan_only_links": self.require(bool, convert_to_type=True, default=False),
            "scan_only_cliques": self.require(bool, convert_to_type=True, default=False),
            "env_name": self.require(str, mandatory=True),
            "inventory": self.require(str),
            "object_id": self.require(str),
            "es_index": self.require(bool, convert_to_type=True, default=False)
        }
        self.validate_query_data(scan, scan_requirements)
        scan_only_keys = [k for k in scan if k.startswith("scan_only_") and scan[k] is True]
        if len(scan_only_keys) > 1:
            self.bad_request("multiple scan_only_* flags are set to true: {0}. "
                             "only one of them can be set to true."
                             .format(", ".join(scan_only_keys)))

        env_name = scan.pop("env_name")
        scan["environment"] = env_name
        if not self.check_environment_name(env_name):
            self.bad_request("unknown environment: {}".format(env_name))

        scan.update({
            "status": self.DEFAULT_STATUS,
            "submit_timestamp": datetime.now()
        })

        result = self.write(scan, self.COLLECTION)
        response_body = {
            "message": "created a new scan for environment {}".format(env_name),
            "id": str(result.inserted_id)
        }
        self.set_created_response(resp, response_body)

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
