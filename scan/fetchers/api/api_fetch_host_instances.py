###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.utils.inventory_mgr import InventoryMgr
from base.utils.origins import Origin
from scan.fetchers.api.api_access import ApiAccess
from scan.fetchers.db.db_fetch_instances import DbFetchInstances


class ApiFetchHostInstances(ApiAccess):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()
        self.token = None
        self.nova_endpoint = None
        self.neutron_endpoint = None
        self.projects = None
        self.db_fetcher = None

        self.flavors = None
        self.images = None
        self.security_groups = None

    def setup(self, env, origin: Origin = None):
        super().setup(env, origin)
        self.token = None
        self.nova_endpoint = self.base_url.replace(":5000", ":8774")
        self.neutron_endpoint = self.base_url.replace(":5000", ":9696")
        self.db_fetcher = DbFetchInstances()

        self.flavors = {}
        self.images = {}
        self.security_groups = {}

    def get_projects(self):
        if not self.projects:
            projects_list = self.inv.get(self.get_env(), "project", None)
            self.projects = [{"name": p["name"], "id": p["id"], "domain_id": p["domain_id"]} for p in projects_list]

    def get(self, id):
        self.get_projects()
        host_id = id[:id.rindex("-")]
        host = self.inv.get_by_id(self.get_env(), host_id)
        if not host or "Compute" not in host.get("host_type", ""):
            return []
        instances_found = self.get_instances_from_api(host_id)
        self.db_fetcher.get_instance_data(instances_found)
        return instances_found

    def get_instances_from_api(self, host_name):
        self.token = self.auth(self.admin_project)
        if not self.token:
            return []
        tenant_id = self.token["tenant"]["id"]
        req_url = "{}/v2/{}/os-hypervisors/{}/servers".format(self.nova_endpoint, tenant_id, host_name)
        response = self.get_url(req_url, {"X-Auth-Token": self.token["id"]})
        ret = []
        # Ironic hosts/nodes will not have instances, not 'hypevisors'
        if response is not None:
            if "hypervisors" not in response:
                return []
            if "servers" not in response["hypervisors"][0]:
                return []
            for doc in response["hypervisors"][0]["servers"]:
                doc["id"] = doc["uuid"]
                doc["host"] = host_name
                doc["local_name"] = doc.pop("name")
                self.get_additional_instance_data(doc)
                ret.append(doc)
        self.log.info("found %s instances for host: %s", str(len(ret)), host_name)
        return ret

    @staticmethod
    def set_server_info(doc, server):
        for field in ("key_name", "user_id", "tenant_id", "metadata",
                      "accessIPv4", "accessIPv6", "progress", "config_drive"):
            if field in server:
                doc[field] = server[field]

        if "addresses" in server:
            doc["addresses"] = [
                {"network": network_name, "addresses": addresses}
                for network_name, addresses in server["addresses"].items()
            ]

        for field in ("OS-SRV-USG:launched_at", "OS-EXT-STS:task_state", "OS-EXT-STS:vm_state",
                      "OS-SRV-USG:terminated_at", "OS-EXT-AZ:availability_zone", "OS-EXT-STS:power_state",
                      "OS-DCF:diskConfig", "os-extended-volumes:volumes_attached"):
            if field in server:
                doc[field.split(":")[-1]] = server[field]

        doc["created_at"] = server.get("created")

    def get_additional_instance_data(self, doc):
        req_url = "{}/v2/servers/{}".format(self.nova_endpoint, doc['id'])
        response = self.get_url(req_url, {"X-Auth-Token": self.token["id"]})
        server = response["server"]

        self.set_server_info(doc, server)
        # find the specific instance's project/tenant based on tenant_id and add more project details
        instance_project = next(
            (pi for pi in self.projects if pi["id"] == doc["tenant_id"]),
            {"name": "unknown", "domain_id": "unknown", "id": "unknown"}
        )

        doc.update({
            "project_name": instance_project["name"],
            "project_domain": instance_project["domain_id"],
            "flavor": self.get_flavor_data(server["flavor"]["id"]) if isinstance(server.get('flavor'), dict) else None,
            "image": self.get_image_data(server["image"]["id"]) if isinstance(server.get('image'), dict) else None,
            "security_groups": self.get_security_groups(server)
        })

    def get_flavor_data(self, flavor_id):
        if flavor_id in self.flavors:
            return self.flavors[flavor_id]

        req_url = "{}/v2/flavors/{}".format(self.nova_endpoint, flavor_id)
        response = self.get_url(req_url, {"X-Auth-Token": self.token["id"]})
        flavor = None
        if response and "flavor" in response:
            flavor = response["flavor"]
            flavor.pop("links", None)
            for field in flavor:
                flavor[field.split(":")[-1]] = flavor.pop(field)
            self.flavors[flavor_id] = flavor
        return flavor

    def get_image_data(self, image_id):
        if image_id in self.images:
            return self.images[image_id]

        req_url = "{}/v2/images/{}".format(self.nova_endpoint, image_id)
        response = self.get_url(req_url, {"X-Auth-Token": self.token["id"]})
        image = None
        if response and "image" in response:
            image = response["image"]
            image.pop("links", None)
            self.images[image_id] = image
        return image

    def get_security_groups(self, server):
        server_sec_groups = server.get('security_groups')
        if not server_sec_groups:
            return {}

        if not self.security_groups:
            req_url = "{}/v2.0/security-groups".format(self.neutron_endpoint)
            response = self.get_url(req_url, {"X-Auth-Token": self.token["id"]})
            self.security_groups = {"{}:{}".format(sg["tenant_id"], sg["name"]): sg for sg in response["security_groups"]}

        security_groups = []
        for security_group in server_sec_groups:
            sg_key = "{}:{}".format(server["tenant_id"], security_group["name"])
            security_groups.append(self.security_groups.get(sg_key))

        return security_groups
