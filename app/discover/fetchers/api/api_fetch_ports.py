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


class ApiFetchPorts(ApiAccess):
    def __init__(self):
        super(ApiFetchPorts, self).__init__()
        self.inv = InventoryMgr()

    def get(self, project_id):
        # use project admin credentials, to be able to fetch all ports
        token = self.v2_auth_pwd(self.admin_project)
        if not token:
            return []
        ret = []
        for region in self.regions:
            ret.extend(self.get_ports_for_region(region, token))
        return ret

    def get_ports_for_region(self, region, token):
        endpoint = self.get_region_url_nover(region, "neutron")
        req_url = endpoint + "/v2.0/ports"
        headers = {
            "X-Auth-Project-Id": self.admin_project,
            "X-Auth-Token": token["id"]
        }
        response = self.get_url(req_url, headers)
        if not "ports" in response:
            return []
        ports = response["ports"]
        for doc in ports:
            doc["master_parent_type"] = "network"
            doc["master_parent_id"] = doc["network_id"]
            doc["parent_type"] = "ports_folder"
            doc["parent_id"] = doc["network_id"] + "-ports"
            doc["parent_text"] = "Ports"
            # get the project name
            net = self.inv.get_by_id(self.get_env(), doc["network_id"])
            if net:
                doc["name"] = doc["mac_address"]
            else:
                doc["name"] = doc["id"]
            project = self.inv.get_by_id(self.get_env(), doc["tenant_id"])
            if project:
                doc["project"] = project["name"]
        return ports
