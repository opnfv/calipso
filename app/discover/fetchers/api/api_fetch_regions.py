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


class ApiFetchRegions(ApiAccess):
    def __init__(self):
        super(ApiFetchRegions, self).__init__()
        self.endpoint = ApiAccess.base_url

    def get(self, project_id):
        token = self.v2_auth_pwd(self.admin_project)
        if not token:
            return []
        # the returned authentication response contains the list of end points
        # and regions
        service_catalog = ApiAccess.auth_response.get('access', {}).get('serviceCatalog')
        if not service_catalog:
            return []
        env = self.get_env()
        ret = []
        NULL_REGION = "No-Region"
        for service in service_catalog:
            for e in service["endpoints"]:
                if "region" in e:
                    region_name = e.pop("region")
                    region_name = region_name if region_name else NULL_REGION
                else:
                    region_name = NULL_REGION
                if region_name in self.regions.keys():
                    region = self.regions[region_name]
                else:
                    region = {
                        "id": region_name,
                        "name": region_name,
                        "endpoints": {}
                    }
                    ApiAccess.regions[region_name] = region
                region["parent_type"] = "regions_folder"
                region["parent_id"] = env + "-regions"
                e["service_type"] = service["type"]
                region["endpoints"][service["name"]] = e
        ret.extend(list(ApiAccess.regions.values()))
        return ret
