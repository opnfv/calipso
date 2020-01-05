###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

import time

import requests
import urllib3

from base.utils.api_access_base import ApiAccessBase
from base.utils.configuration import Configuration

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def aci_config_required(default=None):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if not self.aci_enabled:
                return default
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


class AciAccess(ApiAccessBase):

    RESPONSE_FORMAT = "json"
    MAX_LOGIN_ATTEMPTS = 5
    cookie_token = None
    session = None

    def __init__(self, config=None):
        self.aci_enabled = (
            True
            if config
            else Configuration().get_env_config().get('aci_enabled', False)
        )

        super().__init__("ACI", config=config, enabled=self.aci_enabled)

        self.aci_configuration = (
            self.config.get("ACI") if self.aci_enabled else None
        )

    @classmethod
    def reset_token(cls):
        cls.cookie_token = None

    @staticmethod
    def login_backoff(attempt):
        return attempt + 1

    def get_base_url(self):
        return "https://{}/api".format(self.host)

    # Debug method
    def send_request(self, method, url, *args, **kwargs):
        if not AciAccess.session:
            self.log.error("Session not initialized")
            return None

        method = method.upper()
        # self.log.info("Sending a {} request to ACI url: {}. Headers: {}".format(method, url, kwargs.get('headers')))
        if method == "GET":
            return AciAccess.session.get(url, *args, **kwargs)
        elif method == "POST":
            return AciAccess.session.post(url, *args, **kwargs)
        else:
            self.log.error("Unknown method")
            return None

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
        tokens = AciAccess.get_objects_by_field_names(response.json(), "aaaLogin", "attributes", "urlToken")
        token = tokens[0]

        if token:  # Refresh sends empty url tokens
            AciAccess.cookie_token = {"APIC-Challenge": token}

    @aci_config_required()
    def login(self):
        if AciAccess.session:
            self.logout(ignore_errors=True)
            AciAccess.session.close()
            AciAccess.session = None

        url = "/".join((self.get_base_url(), "aaaLogin.json?gui-token-request=yes"))
        payload = {
            "aaaUser": {
                "attributes": {
                    "name": self.aci_configuration["user"],
                    "pwd": self.aci_configuration["pwd"]
                }
            }
        }

        AciAccess.session = requests.Session()
        response = self.send_request("POST", url, json=payload, verify=False, timeout=self.CONNECT_TIMEOUT)

        response.raise_for_status()

        AciAccess._set_token(response)

    # Refresh token or login if token has expired
    @aci_config_required()
    def refresh_token(self):
        # First time login
        if not AciAccess.cookie_token:
            self.log.info("ACI token is empty. Logging in")
            self.login()
            return

        url = "/".join((self.get_base_url(), "aaaRefresh.json"))

        response = self.send_request("GET", url, headers=self.cookie_token, verify=False)

        # Login again if the token has expired
        if response.status_code == requests.codes.forbidden:
            self.log.info("ACI token refresh failed. Response: {}".format(response.text))
            self.login()
            return
        # Propagate any other error
        elif response.status_code != requests.codes.ok:
            response.raise_for_status()

        AciAccess._set_token(response)

    @aci_config_required()
    def logout(self, ignore_errors=False):
        if not AciAccess.cookie_token or not AciAccess.session:
            return

        url = "/".join((self.get_base_url(), "aaaLogout.json"))
        payload = {
            "aaaUser": {
                "attributes": {
                    "name": self.aci_configuration["user"]
                }
            }
        }

        response = self.send_request("POST", url, headers=self.cookie_token, json=payload,
                                     verify=False, timeout=self.CONNECT_TIMEOUT)

        if not ignore_errors:
            response.raise_for_status()

        self.reset_token()

    def get_token(self, attempt=1):
        try:
            self.refresh_token()
        except Exception as e:
            # ACI sometimes returns HTTP 503 (Service Temporarily Unavailable)
            # on excessively frequent client requests,
            # so a reasonable backoff is required.
            if attempt <= self.MAX_LOGIN_ATTEMPTS:
                time.sleep(self.login_backoff(attempt))
                return self.get_token(attempt=attempt+1)
            raise e

    @aci_config_required(default={})
    def send_get(self, url, params, headers, cookies):
        self.get_token()

        headers = self._insert_token_into_request(headers)

        response = self.send_request("GET", url,
                                     params=params, headers=headers,
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
