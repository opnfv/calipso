###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import calendar
import time

import requests
from abc import abstractmethod, ABCMeta


from base.utils.logging.full_logger import FullLogger


class KeystoneClient(metaclass=ABCMeta):
    CONNECT_TIMEOUT = 5

    auth_path = None
    tenants_url = None

    tokens = {}
    auth_responses = {}

    def __init__(self, base_url, version, project, api_config):
        self.auth_url = "/".join((base_url.rstrip("/"), self.auth_path.lstrip("/")))
        self.version = version
        self.project = project
        self.api_config = api_config
        self.log = FullLogger()

    @property
    def tenants_enabled(self):
        return True if self.tenants_url else False

    @abstractmethod
    def get_post_body(self):
        return None

    @abstractmethod
    def get_token(self, auth_response):
        return None

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
    @classmethod
    def get_existing_token(cls, project_id):
        try:
            token_details = cls.tokens[project_id]
        except KeyError:
            return None

        token_expiry_time = token_details.get("token_expiry_time")
        if not token_expiry_time:
            return token_details  # Token doesn't have expiration time
        now = time.time()
        if now > token_expiry_time:
            # token has expired
            cls.tokens.pop(project_id)
            return None
        return token_details

    def get_auth_response(self, project_id):
        return self.auth_responses.get(project_id, self.auth_responses.get(self.project))

    @abstractmethod
    def get_catalog(self, project_id=None):
        return []

    @staticmethod
    @abstractmethod
    def get_region_url_from_service(service):
        return None

    def auth(self, project=None):
        if not project:
            project = self.project

        post_body = self.get_post_body()

        if self.project is not None:
            post_body["auth"]["tenantName"] = project
            project_id = project
        else:
            project_id = ""

        subject_token = self.get_existing_token(project_id)
        if subject_token:
            return subject_token

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8'
        }

        response = requests.post(self.auth_url, json=post_body, headers=headers,
                                 timeout=self.CONNECT_TIMEOUT)
        self.auth_responses[project_id] = response

        token = self.get_token(response)
        if token:
            self.tokens[project_id] = token
        return token


class KeystoneClientV2(KeystoneClient):
    auth_path = "/v2.0/tokens"
    tenants_url = "/v2.0/tenants"

    def get_post_body(self):
        return {
            "auth": {
                "passwordCredentials": {
                    "username": self.api_config["user"],
                    "password": self.api_config["pwd"]
                }
            }
        }

    def get_token(self, auth_response):
        if 'error' in auth_response:
            self.log.error("{e['code']} {e['title']}: {e['message']}, URL: {url}".format(
                e=auth_response['error'], url=self.auth_url)
            )
            return None
        try:
            token_details = auth_response.json()["access"]["token"]
        except KeyError:
            # assume authentication failed
            return None
        token_expiry = token_details["expires"]
        token_expiry_time_struct = self.parse_time(token_expiry)
        if not token_expiry_time_struct:
            return None
        token_expiry_time = calendar.timegm(token_expiry_time_struct)
        token_details["token_expiry_time"] = token_expiry_time
        return token_details

    def get_catalog(self, project_id=None):
        if not project_id:
            project_id = self.project

        auth_response = self.auth_responses.get(project_id, self.auth_responses.get(self.project))
        if not auth_response:
            self.log.error("No auth response found for project '{}'".format(project_id))
            return []

        return auth_response.json()["access"]["serviceCatalog"]

    @staticmethod
    def get_region_url_from_service(service):
        return service["adminURL"]


class KeystoneClientV3(KeystoneClient):
    auth_path = "/v3/auth/tokens"

    def get_post_body(self):
        return {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": self.api_config["user"],
                            "password": self.api_config["pwd"],
                            "domain": {"id": "default"}
                        }
                    }
                },
                "scope": {
                    "project": {
                        "name": self.project,
                        "domain": {"id": "default"}
                    }
                }
            }
        }

    def get_token(self, auth_response):
        if 'error' in auth_response:
            self.log.error("{e['code']} {e['title']}: {e['message']}, URL: {url}".format(
                e=auth_response['error'], url=self.auth_url)
            )
            return None
        try:
            token_details = auth_response.json()["token"]
        except KeyError:
            # assume authentication failed
            return None

        token_details["id"] = auth_response.headers["X-Subject-Token"]
        token_details["tenant"] = token_details.pop("project")

        token_expiry = token_details.pop("expires_at", None)  # A null value indicates that the token never expires
        token_details["token_expiry_time"] = None
        if token_expiry:
            token_details["expires"] = token_expiry
            token_expiry_time_struct = self.parse_time(token_expiry)
            if not token_expiry_time_struct:
                self.log.warning("Failed to parse Keystone token expiry time from string: {}".format(token_expiry))
                return token_details
            token_expiry_time = calendar.timegm(token_expiry_time_struct)
            token_details["token_expiry_time"] = token_expiry_time
        return token_details

    def get_catalog(self, project_id=None):
        if not project_id:
            project_id = self.project

        token = self.tokens.get(project_id, self.tokens.get(self.project))
        if not token:
            self.log.error("Project '{}' doesn't have active tokens".format(project_id))
            return []

        return token["catalog"]

    @staticmethod
    def get_region_url_from_service(service):
        return service["url"]
