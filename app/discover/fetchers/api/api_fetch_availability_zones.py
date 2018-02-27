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


class ApiFetchAvailabilityZones(ApiAccess):
    def __init__(self):
        super(ApiFetchAvailabilityZones, self).__init__()

    def get(self, project_id):
        token = self.v2_auth_pwd(project_id)
        if not token:
            return []
        ret = []
        for region in self.regions:
            ret.extend(self.get_for_region(project_id, region, token))
        return ret

    def get_for_region(self, project, region, token):
        # we use os-availability-zone/detail rather than os-availability-zone,
        # because the later does not inclde the "internal" zone in the results
        endpoint = self.get_region_url_nover(region, "nova")
        req_url = endpoint + "/v2/" + token["tenant"]["id"] + \
            "/os-availability-zone/detail"
        headers = {
            "X-Auth-Project-Id": project,
            "X-Auth-Token": token["id"]
        }
        response = self.get_url(req_url, headers)
        if "status" in response and int(response["status"]) != 200:
            return []
        ret = []
        if "availabilityZoneInfo" not in response:
            return []
        azs = response["availabilityZoneInfo"]
        if not azs:
            return []
        for doc in azs:
            doc["id"] = doc["zoneName"]
            doc["name"] = doc.pop("zoneName")
            self.set_folder_parent(doc, object_type="availability_zone",
                                   master_parent_type="region",
                                   master_parent_id=region,
                                   parent_text="Availability Zones")
            doc["available"] = doc["zoneState"]["available"]
            doc.pop("zoneState")
            ret.append(doc)
        return ret
