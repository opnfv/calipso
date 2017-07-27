###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
# fetch the end points for a given project (tenant)
# return list of regions, to allow further recursive scanning

from discover.fetchers.api.api_access import ApiAccess


class ApiFetchEndPoints(ApiAccess):

    def get(self, project_id):
        if project_id != "admin":
            return []  # XXX currently having problems authenticating to other tenants
        self.v2_auth_pwd(project_id)

        environment = ApiAccess.config.get_env_name()
        regions = []
        services = ApiAccess.auth_response['access']['serviceCatalog']
        endpoints = []
        for s in services:
            if s["type"] != "identity":
                continue
            e = s["endpoints"][0]
            e["environment"] = environment
            e["project"] = project_id
            e["type"] = "endpoint"
            endpoints.append(e)
        return endpoints
