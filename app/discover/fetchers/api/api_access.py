###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import calendar
import re
import requests
import time

from utils.api_access_base import ApiAccessBase
from utils.string_utils import jsonify


class ApiAccess(ApiAccessBase):

    ADMIN_PORT = "35357"

    subject_token = None
    initialized = False
    regions = {}

    tokens = {}
    admin_endpoint = ""
    admin_project = None
    auth_response = {}

    alternative_services = {
        "neutron": ["quantum"]
    }

    # identity API v2 version with admin token
    def __init__(self, config=None):
        super().__init__('OpenStack', config)
        self.base_url = "http://" + self.host + ":" + self.port
        if self.initialized:
            return
        ApiAccess.admin_project = self.api_config.get("admin_project", "admin")
        ApiAccess.admin_endpoint = "http://" + self.host + ":" + self.ADMIN_PORT

        token = self.v2_auth_pwd(ApiAccess.admin_project)
        if not token:
            raise ValueError("Authentication failed. Failed to obtain token")
        else:
            self.subject_token = token
            self.initialized = True

    @staticmethod
    def parse_time(time_str):
        try:
            time_struct = time.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            try:
                time_struct = time.strptime(time_str,
                                            "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                return None
        return time_struct

    # try to use existing token, if it did not expire
    def get_existing_token(self, project_id):
        try:
            token_details = ApiAccess.tokens[project_id]
        except KeyError:
            return None
        token_expiry = token_details["expires"]
        token_expiry_time_struct = self.parse_time(token_expiry)
        if not token_expiry_time_struct:
            return None
        token_expiry_time = token_details["token_expiry_time"]
        now = time.time()
        if now > token_expiry_time:
            # token has expired
            ApiAccess.tokens.pop(project_id)
            return None
        return token_details

    def v2_auth(self, project_id, headers, post_body):
        subject_token = self.get_existing_token(project_id)
        if subject_token:
            return subject_token
        req_url = self.base_url + "/v2.0/tokens"
        response = requests.post(req_url, json=post_body, headers=headers,
                                 timeout=self.CONNECT_TIMEOUT)
        response = response.json()
        ApiAccess.auth_response[project_id] = response
        if 'error' in response:
            e = response['error']
            self.log.error(str(e['code']) + ' ' + e['title'] + ': ' +
                           e['message'] + ", URL: " + req_url)
            return None
        try:
            token_details = response["access"]["token"]
        except KeyError:
            # assume authentication failed
            return None
        token_expiry = token_details["expires"]
        token_expiry_time_struct = self.parse_time(token_expiry)
        if not token_expiry_time_struct:
            return None
        token_expiry_time = calendar.timegm(token_expiry_time_struct)
        token_details["token_expiry_time"] = token_expiry_time
        ApiAccess.tokens[project_id] = token_details
        return token_details

    def v2_auth_pwd(self, project):
        user = self.api_config["user"]
        pwd = self.api_config["pwd"]
        post_body = {
            "auth": {
                "passwordCredentials": {
                    "username": user,
                    "password": pwd
                }
            }
        }
        if project is not None:
            post_body["auth"]["tenantName"] = project
            project_id = project
        else:
            project_id = ""
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8'
        }
        return self.v2_auth(project_id, headers, post_body)

    @staticmethod
    def get_auth_response(project_id):
        auth_response = ApiAccess.auth_response.get(project_id)
        if not auth_response:
            auth_response = ApiAccess.auth_response.get('admin', {})
        return auth_response

    def get_region_url(self, region_name, service):
        if region_name not in self.regions:
            return None
        region = self.regions[region_name]
        s = self.get_service_region_endpoints(region, service)
        if not s:
            return None
        orig_url = s["adminURL"]
        # replace host name with the host found in config
        url = re.sub(r"^([^/]+)//[^:]+", r"\1//" + self.host, orig_url)
        return url

    # like get_region_url(), but remove everything starting from the "/v2"
    def get_region_url_nover(self, region, service):
        full_url = self.get_region_url(region, service)
        if not full_url:
            self.log.error("could not find region URL for region: " + region)
            exit()
        url = re.sub(r":([0-9]+)/v[2-9].*", r":\1", full_url)
        return url

    def get_catalog(self, pretty):
        return jsonify(self.regions, pretty)

    # find the endpoints for a given service name,
    # considering also alternative service names
    def get_service_region_endpoints(self, region, service):
        alternatives = [service]
        endpoints = region["endpoints"]
        if service in self.alternative_services:
            alternatives.extend(self.alternative_services[service])
        for sname in alternatives:
            if sname in endpoints:
                return endpoints[sname]
        return None
