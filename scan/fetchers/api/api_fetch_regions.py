###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from scan.fetchers.api.api_access import ApiAccess


class ApiFetchRegions(ApiAccess):
    NULL_REGION = "No-Region"

    def get(self, regions_folder_id):
        token = self.auth(self.admin_project)
        if not token:
            return []

        project_id = regions_folder_id.replace('-regions', '')
        service_catalog = self.get_catalog(project_id)
        if not service_catalog:
            return []

        for service in service_catalog:
            for e in service["endpoints"]:
                if "region" in e:
                    region_name = e.pop("region")
                    region_name = region_name if region_name else self.NULL_REGION
                else:
                    region_name = self.NULL_REGION
                if region_name in self.regions.keys():
                    region = self.regions[region_name]
                else:
                    region = {
                        "id": "|".join(("region", region_name)),
                        "name": region_name,
                        "endpoints": []
                    }
                    ApiAccess.regions[region_name] = region
                region["parent_type"] = "regions_folder"
                region["parent_id"] = self.get_env() + "-regions"
                e["name"] = service["name"]
                e["service_type"] = service["type"]
                region["endpoints"].append(e)
        return list(ApiAccess.regions.values())
