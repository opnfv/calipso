###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.api.api_access import ApiAccess


class ApiFetchProjects(ApiAccess):
    def __init__(self):
        super(ApiFetchProjects, self).__init__()

    def get(self, project_id):
        token = self.v2_auth_pwd(self.admin_project)
        if not token:
            return []
        if not self.regions:
            self.log.error('No regions found')
            return []
        ret = []
        for region in self.regions:
            ret.extend(self.get_for_region(region, token))
        projects_for_user = self.get_projects_for_api_user(region, token)
        return [p for p in ret if p['name'] in projects_for_user] \
            if projects_for_user else ret

    def get_projects_for_api_user(self, region, token):
        if not token:
            token = self.v2_auth_pwd(self.admin_project)
            if not token:
                return []
        endpoint = self.get_region_url_nover(region, "keystone")
        headers = {
            'X-Auth-Project-Id': self.admin_project,
            'X-Auth-Token': token['id']
        }
        # get the list of projects accessible by the admin user
        req_url = endpoint + '/v3/projects'
        response = self.get_url(req_url, headers)
        if not response or 'projects' not in response:
            return None
        response = [p['name'] for p in response['projects']]
        return response

    def get_for_region(self, region, token):
        endpoint = self.get_region_url_nover(region, "keystone")
        req_url = endpoint + "/v2.0/tenants"
        headers = {
            "X-Auth-Project-Id": self.admin_project,
            "X-Auth-Token": token["id"]
        }
        response = self.get_url(req_url, headers)
        if not isinstance(response, dict):
            self.log.error('invalid response to /tenants request: not dict')
            return []
        tenants_list = response.get("tenants", [])
        if not isinstance(tenants_list, list):
            self.log.error('invalid response to /tenants request: '
                           'tenants value is n ot a list')
            return []
        response = [t for t in tenants_list if t.get("name", "") != "services"]
        return response
