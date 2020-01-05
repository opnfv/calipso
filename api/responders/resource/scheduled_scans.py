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


class ScheduledScans(ResponderBase):

    COLLECTION = "scheduled_scans"
    ID = "_id"
    PROJECTION = {
        ID: True,
        "environment": True,
        "scheduled_timestamp": True,
        "freq": True
    }
    SCAN_FREQ = [
        "YEARLY",
        "MONTHLY",
        "WEEKLY",
        "DAILY",
        "HOURLY"
    ]

    def on_get(self, req, resp):
        self.log.debug("Getting scheduled scans")
        filters = self.parse_query_params(req)

        filters_requirements = {
            "env_name": self.require(str, mandatory=True),
            "id": self.require(ObjectId, convert_to_type=True),
            "freq": self.require(str,
                                 validate=DataValidate.LIST,
                                 requirement=self.SCAN_FREQ),
            "page": self.require(int, convert_to_type=True),
            "page_size": self.require(int, convert_to_type=True)
        }

        self.validate_query_data(filters, filters_requirements)
        page, page_size = self.get_pagination(filters)

        query = self.build_query(filters)
        if self.ID in query:
            scheduled_scan = self.get_object_by_id(self.COLLECTION, query,
                                                   [ObjectId, datetime],
                                                   self.ID)
            self.set_ok_response(resp, scheduled_scan)
        else:
            scheduled_scan_ids = self.get_objects_list(self.COLLECTION, query,
                                                       page, page_size,
                                                       self.PROJECTION,
                                                       [datetime])
            self.set_ok_response(resp, {"scheduled_scans": scheduled_scan_ids})

    def on_post(self, req, resp):
        self.log.debug("Posting new scheduled scan")
        error, scheduled_scan = self.get_content_from_request(req)
        if error:
            self.bad_request(error)

        log_levels = self.get_constants_by_name("log_levels")
        scheduled_scan_requirements = {
            "env_name": self.require(str, mandatory=True),
            "scan_only_links": self.require(bool, convert_to_type=True, default=False),
            "scan_only_cliques": self.require(bool, convert_to_type=True, default=False),
            "scan_only_inventory": self.require(bool, convert_to_type=True, default=False),
            "freq": self.require(str,
                                 mandatory=True,
                                 validate=DataValidate.LIST,
                                 requirement=self.SCAN_FREQ),
            "log_level": self.require(str,
                                      validate=DataValidate.LIST,
                                      requirement=log_levels),
            "clear": self.require(bool, convert_to_type=True),
            "submit_timestamp": self.require(str, mandatory=True),
            "es_index": self.require(bool, convert_to_type=True, default=False)
        }
        self.validate_query_data(scheduled_scan, scheduled_scan_requirements)
        self.check_and_convert_datetime("submit_timestamp", scheduled_scan)

        scan_only_keys = [
            k for k in scheduled_scan if k.startswith("scan_only_") and scheduled_scan[k] is True
        ]
        if len(scan_only_keys) > 1:
            self.bad_request("multiple scan_only_* flags found: {0}. "
                             "only one of them can be set."
                             .format(", ".join(scan_only_keys)))

        env_name = scheduled_scan.pop("env_name")
        scheduled_scan["environment"] = env_name
        if not self.check_environment_name(env_name):
            self.bad_request("unknown environment: {}".format(env_name))

        result = self.write(scheduled_scan, self.COLLECTION)
        response_body = {
            "message": "created a new scheduled scan for environment {}".format(env_name),
            "id": str(result.inserted_id)
        }
        self.set_created_response(resp, response_body)

    def build_query(self, filters):
        query = {}
        filters_keys = ["freq"]
        self.update_query_with_filters(filters, filters_keys, query)

        _id = filters.get("id")
        if _id:
            query["_id"] = _id
        query['environment'] = filters['env_name']
        return query
