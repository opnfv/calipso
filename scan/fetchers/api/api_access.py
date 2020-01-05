###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re

from urllib3 import Retry

from base.utils.api_access_base import ApiAccessBase
from base.utils.exceptions import CredentialsError
from base.utils.origins import Origin
from base.utils.string_utils import jsonify
from scan.fetchers.api.clients.keystone import *
from requests import adapters

from scan.scan_error import ScanError


class ApiAccess(ApiAccessBase):

    ADMIN_PORT = "35357"
    KEYSTONE_CLIENTS = {
        "v2": KeystoneClientV2,
        "v3": KeystoneClientV3
    }
    alternative_services = {
        "neutron": ["quantum"]
    }
    regions = {}

    def __init__(self, config=None):
        super().__init__('OpenStack', config)
        self.base_url = None
        self.admin_project = None
        self.admin_endpoint = None
        self.keystone_client = None
        self.set_keystone_connection()

    def set_keystone_connection(self):
        self.base_url = "http://{}:{}".format(self.host, self.port)
        self.admin_project = self.api_config.get("admin_project", "admin")
        self.admin_endpoint = "http://{}:{}".format(self.host, self.ADMIN_PORT)
        self.keystone_client = self.get_keystone_client()

        token = self.keystone_client.auth()
        if not token:
            raise ScanError("ApiAccess: Authentication failed. "
                            "Failed to obtain token")

    def setup(self, env, origin: Origin = None):
        super().setup(env, origin)
        self.set_api_config('OpenStack')
        self.set_keystone_connection()

    @classmethod
    def reset(cls):
        cls.regions = {}
        KeystoneClient.tokens, KeystoneClient.auth_responses = {}, {}
        for keystone_client in cls.KEYSTONE_CLIENTS.values():
            keystone_client.tokens, keystone_client.auth_responses = {}, {}

    def get_keystone_client(self):
        session = requests.Session()
        session.mount(self.base_url, adapters.HTTPAdapter(max_retries=Retry(self.REQUEST_RETRIES)))
        # Intercept improper configuration errors
        try:
            response = session.get(self.base_url, timeout=(self.CONNECT_TIMEOUT, self.READ_TIMEOUT))
            response.raise_for_status()
        except Exception as e:
            raise ScanError("Failed to get keystone client. Error: {}".format(e))
        finally:
            session.close()

        versions = response.json()["versions"]["values"]
        for version in versions:
            if version.get("status") == "stable":
                version_id = version.get("id")
                if not version_id:
                    continue

                id_match = re.match("^(v\d+)\..*", version_id)
                if not id_match:
                    self.log.warning(
                        "ApiAccess: Failed to determine stable OpenStack auth version id. "
                        "Found id: {}".format(version.get("id"))
                    )
                    continue

                auth_class = self.KEYSTONE_CLIENTS.get(id_match.groups()[0])
                if not auth_class:
                    self.log.warning(
                        "ApiAccess: OpenStack auth version {} unsupported (no auth class found)"
                        .format(version.get("id"))
                    )
                    continue

                self.log.info("ApiAccess: Using keystone API version: '{}'".format(version_id))
                return auth_class(base_url=self.base_url, version=version_id,
                                  project=self.admin_project, api_config=self.api_config)
        raise ValueError("ApiAccess: Failed to determine stable OpenStack auth version")

    def get_auth_response(self, project_id):
        return self.keystone_client.get_auth_response(project_id)

    def auth(self, project=None):
        return self.keystone_client.auth(project)

    def get_region_url(self, region_name, service, force_http=True):
        if region_name not in self.regions:
            return None
        region = self.regions[region_name]
        s = self.get_service_region_endpoints(region, service)
        if not s:
            return None
        orig_url = self.keystone_client.get_region_url_from_service(s)
        # replace host name with the host found in config

        host_match = re.match(r"^[^/]+//(.+):[0-9]+", orig_url)
        url = orig_url.replace(host_match.group(1), self.host)

        if force_http and url.startswith("https"):
            url = url.replace("https", "http", 1)
        return url

    # like get_region_url_from_service(), but remove everything starting from the "/v*"
    def get_region_url_nover(self, region, service, force_http=True):
        full_url = self.get_region_url(region, service, force_http)
        if not full_url:
            self.log.error("could not find region URL for region: " + region)
            exit()
        url = re.sub(r":([0-9]+)/v[2-9].*", r":\1", full_url)
        return url

    def get_catalog(self, project_id=None):
        return self.keystone_client.get_catalog(project_id)

    def get_regions(self, pretty):
        return jsonify(self.regions, pretty)

    # find the endpoints for a given service name,
    # considering also alternative service names
    def get_service_region_endpoints(self, region, service):
        alternatives = [service]
        endpoints = region["endpoints"]
        if service in self.alternative_services:
            alternatives.extend(self.alternative_services[service])
        for sname in alternatives:
            for endpoint in endpoints:
                if endpoint['name'] == sname:
                    return endpoint
        return None
