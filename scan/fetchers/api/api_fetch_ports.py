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

from base.utils.inventory_mgr import InventoryMgr
from scan.fetchers.api.api_access import ApiAccess


class ApiFetchPorts(ApiAccess):
    def __init__(self):
        super(ApiFetchPorts, self).__init__()
        self.inv = InventoryMgr()
        self.token = None
        self.auth_headers = None

    def setup(self, env, origin: Origin = None):
        super().setup(env, origin)
        self.token = None
        self.auth_headers = {}

    def get(self, project_id):
        # use project admin credentials, to be able to fetch all ports
        self.token = self.auth(self.admin_project)
        if not self.token:
            return []
        self.auth_headers = {
            "X-Auth-Project-Id": self.admin_project,
            "X-Auth-Token": self.token["id"]
        }

        ret = []
        for region in self.regions:
            ret.extend(self.get_ports_for_region(region))
        return ret

    def get_ports_for_region(self, region):
        endpoint = self.get_region_url_nover(region, "neutron", force_http=True)
        req_url = endpoint + "/v2.0/ports"
        response = self.get_url(req_url, self.auth_headers)
        if "ports" not in response:
            return []
        ports = response["ports"]
        for doc in ports:
            self.set_folder_parent(doc, object_type="port",
                                   master_parent_type="network",
                                   master_parent_id=doc["network_id"])
            # get the project name
            net = self.inv.get_by_id(self.get_env(), doc["network_id"])
            if net:
                doc["name"] = doc["mac_address"]
            else:
                doc["name"] = doc["id"]

            if "security_groups" in doc:
                doc["security_groups"] = [{"id": s} for s in doc["security_groups"]]

            project = self.inv.get_by_id(self.get_env(), doc["tenant_id"])
            if project:
                doc["project"] = project["name"]
        return ports
