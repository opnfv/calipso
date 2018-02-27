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


class ApiFetchNetwork(ApiAccess):
    def __init__(self):
        super(ApiFetchNetwork, self).__init__()
        self.inv = InventoryMgr()

    def get(self, project_id):
        # use project admin credentials, to be able to fetch all networks
        token = self.v2_auth_pwd(self.admin_project)
        if not token:
            return []
        ret = []
        for region in self.regions:
            # TODO: refactor legacy code
            # (Unresolved reference - self.get_for_region)
            ret.extend(self.get_for_region(region, token, project_id))
        return ret

    def get_network(self, region, token, subnet_id):
        endpoint = self.get_region_url_nover(region, "neutron")

        # get target network network document
        req_url = endpoint + "/v2.0/networks/" + subnet_id
        headers = {
            "X-Auth-Project-Id": self.admin_project,
            "X-Auth-Token": token["id"]
        }
        response = self.get_url(req_url, headers)
        if "network" not in response:
            return []
        network = response["network"]
        subnets = network['subnets']

        # get subnets documents.
        subnets_hash = {}
        cidrs = []
        subnet_ids = []
        for subnet_id in subnets:
            req_url = endpoint + "/v2.0/subnets/" + subnet_id
            response = self.get_url(req_url, headers)
            if "subnet" in response:
                # create a hash subnets, to allow easy locating of subnets
                subnet = response["subnet"]
                subnets_hash[subnet["name"]] = subnet
                cidrs.append(subnet["cidr"])
                subnet_ids.append(subnet["id"])

        network["subnets"] = subnets_hash
        network["cidrs"] = cidrs
        network["subnet_ids"] = subnet_ids

        self.set_folder_parent(network, object_type="network",
                               master_parent_type="project",
                               master_parent_id=network["tenant_id"])
        # set the 'network' attribute for network objects to the name of
        # network, to allow setting constraint on network when creating
        # network clique
        network['network'] = network["id"]
        # get the project name
        project = self.inv.get_by_id(self.get_env(), network["tenant_id"])
        if project:
            network["project"] = project["name"]

        return network
