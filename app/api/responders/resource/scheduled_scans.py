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


class ScheduledScans(ResponderBase):
    def __init__(self):
        super().__init__()
        self.COLLECTION = "scheduled_scans"
        self.ID = "_id"
        self.PROJECTION = {
            self.ID: True,
            "environment": True,
            "scheduled_timestamp": True,
            "freq": True
        }
        self.SCAN_FREQ = [
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
            "environment": self.require(str, mandatory=True),
            "id": self.require(ObjectId, True),
            "freq": self.require(str, False,
                                 DataValidate.LIST, self.SCAN_FREQ),
            "page": self.require(int, True),
            "page_size": self.require(int, True)
        }

        self.validate_query_data(filters, filters_requirements)
        page, page_size = self.get_pagination(filters)

        query = self.build_query(filters)
        if self.ID in query:
            scheduled_scan = self.get_object_by_id(self.COLLECTION, query,
                                                   [ObjectId, datetime],
                                                   self.ID)
            self.set_successful_response(resp, scheduled_scan)
        else:
            scheduled_scan_ids = self.get_objects_list(self.COLLECTION, query,
                                                       page, page_size,
                                                       self.PROJECTION,
                                                       [datetime])
            self.set_successful_response(resp,
                                         {"scheduled_scans": scheduled_scan_ids})

    def on_post(self, req, resp):
        self.log.debug("Posting new scheduled scan")
        error, scheduled_scan = self.get_content_from_request(req)
        if error:
            self.bad_request(error)

        log_levels = self.get_constants_by_name("log_levels")
        scheduled_scan_requirements = {
            "environment": self.require(str, mandatory=True),
            "scan_only_links": self.require(bool, True),
            "scan_only_cliques": self.require(bool, True),
            "scan_only_inventory": self.require(bool, True),
            "freq": self.require(str, validate=DataValidate.LIST,
                                 requirement=self.SCAN_FREQ,
                                 mandatory=True),
            "log_level": self.require(str,
                                      validate=DataValidate.LIST,
                                      requirement=log_levels),
            "clear": self.require(bool, True),
            "submit_timestamp": self.require(str, mandatory=True)
        }
        self.validate_query_data(scheduled_scan, scheduled_scan_requirements)
        self.check_and_convert_datetime("submit_timestamp", scheduled_scan)
        scan_only_keys = [k for k in scheduled_scan if k.startswith("scan_only_")]
        if len(scan_only_keys) > 1:
            self.bad_request("multiple scan_only_* flags found: {0}. "
                             "only one of them can be set."
                             .format(", ".join(scan_only_keys)))

        env_name = scheduled_scan["environment"]
        if not self.check_environment_name(env_name):
            self.bad_request("unkown environment: " + env_name)

        self.write(scheduled_scan, self.COLLECTION)
        self.set_successful_response(resp,
                                     {"message": "created a new scheduled scan for "
                                                 "environment {0}"
                                     .format(env_name)},
                                     "201")

    def build_query(self, filters):
        query = {}
        filters_keys = ["freq", "environment"]
        self.update_query_with_filters(filters, filters_keys, query)

        _id = filters.get("id")
        if _id:
            query["_id"] = _id
        return query
