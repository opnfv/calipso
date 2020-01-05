###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.utils.origins import Origin
from scan.fetchers.api.api_access import ApiAccess


class ApiFetchProjects(ApiAccess):
    def __init__(self):
        super(ApiFetchProjects, self).__init__()
        self.token = None
        self.auth_headers = None
        self.nova_endpoint = None

    def setup(self, env, origin: Origin = None):
        super().setup(env, origin)
        self.token = None
        self.auth_headers = {}
        self.nova_endpoint = self.base_url.replace(":5000", ":8774")

    def get(self, project_id):
        self.token = self.auth(self.admin_project)
        if not self.token:
            return []
        self.auth_headers = {
            'X-Auth-Project-Id': self.admin_project,
            'X-Auth-Token': self.token['id']
        }

        if not self.regions:
            self.log.error('No regions found')
            return []

        ret = []
        for region in self.regions:
            projects = self.get_projects_for_api_user(region)
            if self.keystone_client.tenants_enabled:
                tenants = self.get_tenants_for_region(region)
                ret.extend(t for t in tenants if t['name'] in (p['name'] for p in projects))
            else:
                ret.extend(projects)
        return ret

    def get_quotas_for_project(self, region, project):
        req_url = "{}/v2/os-quota-sets/{}/detail".format(self.nova_endpoint, project['id'])
        response = self.get_url(req_url, self.auth_headers)
        if not response or 'quota_set' not in response:
            return
        project['quota_set'] = response['quota_set']

    def get_projects_for_api_user(self, region):
        endpoint = self.get_region_url_nover(region, "keystone")
        # get the list of projects accessible by the admin user
        req_url = endpoint + '/v3/projects'
        response = self.get_url(req_url, self.auth_headers)
        if not response or 'projects' not in response:
            return []

        projects = []
        for project in response['projects']:
            # 'services' project does not contain any networks or ports
            if project.get('name') == 'services':
                continue
            if 'parent_id' in project:
                project['parent_domain_id'] = project.pop('parent_id')
            self.get_quotas_for_project(region, project)
            projects.append(project)
        return projects

    def get_tenants_for_region(self, region):
        endpoint = self.get_region_url_nover(region, "keystone")
        req_url = endpoint + self.keystone_client.tenants_url
        response = self.get_url(req_url, self.auth_headers)
        if not isinstance(response, dict):
            self.log.error('invalid response to /tenants request: not dict')
            return []
        tenants_list = response.get("tenants", [])
        if not isinstance(tenants_list, list):
            self.log.error('invalid response to /tenants request: '
                           'tenants value is n ot a list')
            return []

        for tenant in tenants_list:
            self.get_quotas_for_project(region, tenant)

        return tenants_list
