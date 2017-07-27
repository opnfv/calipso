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

import requests

from discover.configuration import Configuration
from discover.fetcher import Fetcher


def aci_config_required(default=None):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if not self.aci_enabled:
                return default
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


class AciAccess(Fetcher):

    RESPONSE_FORMAT = "json"
    cookie_token = None

    def __init__(self):
        super().__init__()
        self.configuration = Configuration()
        self.aci_enabled = self.configuration.get_env_config() \
            .get('aci_enabled', False)
        self.aci_configuration = None
        self.host = None
        if self.aci_enabled:
            self.aci_configuration = self.configuration.get("ACI")
            self.host = self.aci_configuration["host"]

    def get_base_url(self):
        return "https://{}/api".format(self.host)

    # Unwrap ACI response payload
    # and return an array of desired fields' values.
    #
    # Parameters
    # ----------
    #
    # payload: dict
    #       Full json response payload returned by ACI
    # *field_names: Tuple[str]
    #       Enumeration of fields that are used to traverse ACI "imdata" array
    #       (order is important)
    #
    # Returns
    # ----------
    # list
    #       List of unwrapped dictionaries (or primitives)
    #
    # Example
    # ----------
    # Given payload:
    #
    #   {
    #       "totalCount": "2",
    #       "imdata": [
    #           {
    #               "aaa": {
    #                   "bbb": {
    #                       "ccc": "value1"
    #                   }
    #               }
    #           },
    #           {
    #               "aaa": {
    #                   "bbb": {
    #                       "ccc": "value2"
    #                   }
    #               }
    #           }
    #       ]
    #   }
    #
    #   Executing get_objects_by_field_names(payload, "aaa", "bbb")
    #   will yield the following result:
    #
    #   >>> [{"ccc": "value1"}, {"ccc": "value2"}]
    #
    #   Executing get_objects_by_field_names(payload, "aaa", "bbb", "ccc")
    #   will yield the following result:
    #
    #   >>> ["value1", "value2"]
    #
    @staticmethod
    def get_objects_by_field_names(payload, *field_names):
        results = payload.get("imdata", [])
        if not results:
            return []

        for field in field_names:
            results = [entry[field] for entry in results]
        return results

    # Set auth tokens in request headers and cookies
    @staticmethod
    def _insert_token_into_request(cookies):
        return dict(cookies, **AciAccess.cookie_token) \
            if cookies \
            else AciAccess.cookie_token

    @staticmethod
    def _set_token(response):
        tokens = AciAccess.get_objects_by_field_names(response.json(), "aaaLogin", "attributes", "token")
        token = tokens[0]

        AciAccess.cookie_token = {"APIC-Cookie": token}

    @aci_config_required()
    def login(self):
        url = "/".join((self.get_base_url(), "aaaLogin.json"))
        payload = {
            "aaaUser": {
                "attributes": {
                    "name": self.aci_configuration["user"],
                    "pwd": self.aci_configuration["pwd"]
                }
            }
        }

        response = requests.post(url, json=payload, verify=False)
        response.raise_for_status()

        AciAccess._set_token(response)

    # Refresh token or login if token has expired
    @aci_config_required()
    def refresh_token(self):
        # First time login
        if not AciAccess.cookie_token:
            self.login()
            return

        url = "/".join((self.get_base_url(), "aaaRefresh.json"))

        response = requests.get(url, verify=False)

        # Login again if the token has expired
        if response.status_code == requests.codes.forbidden:
            self.login()
            return
        # Propagate any other error
        elif response.status_code != requests.codes.ok:
            response.raise_for_status()

        AciAccess._set_token(response)

    @aci_config_required(default={})
    def send_get(self, url, params, headers, cookies):
        self.refresh_token()

        cookies = self._insert_token_into_request(cookies)

        response = requests.get(url, params=params, headers=headers,
                                cookies=cookies, verify=False)
        # Let client handle HTTP errors
        response.raise_for_status()

        return response.json()

    # Search ACI for Managed Objects (MOs) of a specific class
    @aci_config_required(default=[])
    def fetch_objects_by_class(self,
                               class_name: str,
                               params: dict = None,
                               headers: dict = None,
                               cookies: dict = None,
                               response_format: str = RESPONSE_FORMAT):
        url = "/".join((self.get_base_url(),
                        "class", "{cn}.{f}".format(cn=class_name, f=response_format)))

        response_json = self.send_get(url, params, headers, cookies)
        return self.get_objects_by_field_names(response_json, class_name)

    # Fetch data for a specific Managed Object (MO)
    @aci_config_required(default=[])
    def fetch_mo_data(self,
                      dn: str,
                      params: dict = None,
                      headers: dict = None,
                      cookies: dict = None,
                      response_format: str = RESPONSE_FORMAT):
        url = "/".join((self.get_base_url(), "mo", "topology",
                        "{dn}.{f}".format(dn=dn, f=response_format)))

        response_json = self.send_get(url, params, headers, cookies)
        return response_json
