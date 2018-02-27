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


class ApiFetchNetworks(ApiAccess):
    def __init__(self):
        super(ApiFetchNetworks, self).__init__()
        self.inv = InventoryMgr()

    def get(self, project_id=None):
        # use project admin credentials, to be able to fetch all networks
        token = self.v2_auth_pwd(self.admin_project)
        if not token:
            return []
        ret = []
        for region in self.regions:
            ret.extend(self.get_networks(region, token))
        return ret

    def get_networks(self, region, token):
        endpoint = self.get_region_url_nover(region, "neutron")
        req_url = endpoint + "/v2.0/networks"
        headers = {
            "X-Auth-Project-Id": self.admin_project,
            "X-Auth-Token": token["id"]
        }
        response = self.get_url(req_url, headers)
        if "networks" not in response:
            return []
        networks = response["networks"]
        req_url = endpoint + "/v2.0/subnets"
        response = self.get_url(req_url, headers)
        subnets_hash = {}
        if "subnets" in response:
            # create a hash subnets, to allow easy locating of subnets
            subnets = response["subnets"]
            for s in subnets:
                subnets_hash[s["id"]] = s
        for doc in networks:
            project_id = doc["tenant_id"]
            if not project_id:
                # find project ID of admin project
                project = self.inv.get_by_field(self.get_env(),
                                                "project", "name",
                                                self.admin_project,
                                                get_single=True)
                if not project:
                    self.log.error("failed to find admin project in DB")
                project_id = project["id"]
            self.set_folder_parent(doc, object_type='network',
                                   master_parent_id=project_id,
                                   master_parent_type='project')
            # set the 'network' attribute for network objects to the name of
            # network, to allow setting constraint on network when creating
            # network clique
            doc['network'] = doc["id"]
            # get the project name
            project = self.inv.get_by_id(self.get_env(), project_id)
            if project:
                doc["project"] = project["name"]
            subnets_details = {}
            cidrs = []
            subnet_ids = []
            for s in doc["subnets"]:
                try:
                    subnet = subnets_hash[s]
                    cidrs.append(subnet["cidr"])
                    subnet_ids.append(subnet["id"])
                    subnets_details[subnet["name"]] = subnet
                except KeyError:
                    pass

            doc["subnets"] = subnets_details
            doc["cidrs"] = cidrs
            doc["subnet_ids"] = subnet_ids
        return networks
