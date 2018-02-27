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
from utils.inventory_mgr import InventoryMgr


class ApiFetchPort(ApiAccess):
    def __init__(self):
        super(ApiFetchPort, self).__init__()
        self.inv = InventoryMgr()

    def get(self, project_id):
        if not project_id:
            self.log.info("Get method needs ID parameter")
            return []
        # use project admin credentials, to be able to fetch all ports
        token = self.v2_auth_pwd(self.admin_project)
        if not token:
            return []
        ret = []
        for region in self.regions:
            ret.append(self.get_port(region, token, project_id))
        if ret == []:
            self.log.info("ApiFetchPort: Port not found.")
        return ret

    def get_port(self, region, token, id):
        endpoint = self.get_region_url_nover(region, "neutron")
        req_url = endpoint + "/v2.0/ports/" + id
        headers = {
            "X-Auth-Project-Id": self.admin_project,
            "X-Auth-Token": token["id"]
        }
        response = self.get_url(req_url, headers)
        if not "port" in response:
            return []

        doc = response["port"]
        self.set_folder_parent(doc, object_type="port",
                               master_parent_type="network",
                               master_parent_id=doc["network_id"])
        # get the project name
        net = self.inv.get_by_id(self.get_env(), doc["network_id"])
        if net:
            doc["name"] = doc["mac_address"]
        else:
            doc["name"] = doc["id"]
        project = self.inv.get_by_id(self.get_env(), doc["tenant_id"])
        if project:
            doc["project"] = project["name"]
        return doc
