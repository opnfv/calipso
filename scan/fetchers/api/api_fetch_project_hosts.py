###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json
import re
from requests import exceptions
from base.utils.inventory_mgr import InventoryMgr
from base.utils.origins import Origin
from scan.fetchers.api.api_access import ApiAccess
from scan.fetchers.cli.cli_fetch_host_details import CliFetchHostDetails
from scan.fetchers.db.db_access import DbAccess


class ApiFetchProjectHosts(ApiAccess, DbAccess, CliFetchHostDetails):

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()
        self.nova_endpoint = None
        self.ironic_endpoint = None
        self.token = None
        self.availability_zones = None

    def setup(self, env, origin: Origin = None):
        super().setup(env, origin)
        self.token = None
        self.nova_endpoint = self.base_url.replace(":5000", ":8774")
        self.ironic_endpoint = self.base_url.replace(":5000", ":6385")
        self.availability_zones = {}

    def get(self, project_id):
        if not self.availability_zones:
            self.availability_zones = {
                az["name"]: az for az in self.inv.find({"type": "availability_zone"})
            }

        if project_id != self.admin_project:
            # do not scan hosts except under project 'admin'
            return []
        self.token = self.auth(self.admin_project)
        if not self.token:
            return []
        ret = []
        for region in self.regions:
            ret.extend(self.get_for_region(region))
        return ret

    def get_for_region(self, region):
        endpoint = self.get_region_url(region, "nova")
        ret = []
        if not self.token:
            return []
        req_url = endpoint + "/os-availability-zone/detail"
        headers = {
            "X-Auth-Project-Id": self.admin_project,
            "X-Auth-Token": self.token["id"]
        }
        response = self.get_url(req_url, headers)
        if "status" in response and int(response["status"]) != 200:
            return []

        az_info = response["availabilityZoneInfo"]
        hosts = {}
        for doc in az_info:
            az_hosts = self.get_hosts_from_az(doc)
            for h in az_hosts:
                if "compute" in (ht.lower() for ht in h["host_type"]):
                    self.fetch_host_resources(h)

                if h["name"] in hosts:
                    # merge host_type data between AZs
                    existing_entry = hosts[h["name"]]
                    if 'flavor_resources' in h:
                        existing_entry['flavor_resources'] = h['flavor_resources']
                    for t in h["host_type"]:
                        self.add_host_type(existing_entry, t, doc['zoneName'])
                else:
                    hosts[h["name"]] = h
                    ret.append(h)

        # get os_id for hosts using the os-hypervisors API call
        req_url = endpoint + "/os-hypervisors"
        response = self.get_url(req_url, headers)
        if "status" in response and int(response["status"]) != 200:
            return ret
        if "hypervisors" not in response:
            return ret
        for h in response["hypervisors"]:
            hvname = h["hypervisor_hostname"]
            if '.' in hvname and hvname not in hosts:
                hostname = hvname[:hvname.index('.')]
            else:
                hostname = hvname
            try:
                doc = hosts[hostname]
            except KeyError:
                # TBD - add error output
                continue
            doc["os_id"] = str(h["id"])
            self.fetch_compute_node_ip_address(doc, hvname)
        # get more network nodes details
        self.fetch_network_node_details(ret)
        # temp solution to add ironic hosts/instances from ironic api
        ironic_instances = self.fetch_ironic_instances()
        for ironic in ironic_instances:
            ret.append(ironic)
        return ret

    def get_hosts_from_az(self, az):
        ret = []
        for h in az["hosts"]:
            doc = self.get_host_details(az, h)
            ret.append(doc)
        return ret

    def get_host_details(self, az, h):
        # for hosts we use the name
        services = az["hosts"][h]

        az_doc = self.availability_zones[az["zoneName"]]
        host_doc = {
            "id": h,
            "host": h,
            "name": h,
            "zone": az_doc["name"],
            "parent_type": "availability_zone",
            "parent_id": az_doc["id"],
            "services": services,
            "host_type": []
        }
        if "nova-conductor" in services:
            s = services["nova-conductor"]
            if s["available"] and s["active"]:
                self.add_host_type(host_doc, "Controller", az['zoneName'])
        if "nova-compute" in services:
            s = services["nova-compute"]
            if s["available"] and s["active"]:
                self.add_host_type(host_doc, "Compute", az['zoneName'])
        self.fetch_host_os_details(host_doc)
        return host_doc

    def fetch_host_resources(self, host):
        req_url = "{}/v2.1/os-hosts/{}".format(self.nova_endpoint, host["id"])
        response = self.get_url(req_url, {"X-Auth-Token": self.token["id"]})

        host["flavor_resources"] = []
        # For Ironic hosts/nodes nova_endpoint will respond with None
        if response is not None:
            if "host" in response:
                for resource in response["host"]:
                    resource = resource["resource"]
                    project_id = resource["project"]
                    if not re.match("^\(.*\)$", project_id):
                        project = self.inv.find_one({"id": project_id})
                        if project:
                            resource["project_name"] = project["name"]
                    if resource["project"] == '(total)':
                        resource['memory_mb_total'] = resource.pop('memory_mb')
                        resource['cpu_total'] = resource.pop('cpu')
                        resource['disk_gb_total'] = resource.pop('disk_gb')
                    elif resource["project"] == '(used_now)':
                        resource['memory_mb_used_now'] = resource.pop('memory_mb')
                        resource['cpu_used_now'] = resource.pop('cpu')
                        resource['disk_gb_used_now'] = resource.pop('disk_gb')
                    elif resource["project"] == '(used_max)':
                        resource['memory_mb_used_max'] = resource.pop('memory_mb')
                        resource['cpu_used_max'] = resource.pop('cpu')
                        resource['disk_gb_used_max'] = resource.pop('disk_gb')
                    host["flavor_resources"].append(resource)

    # fetch more details of network nodes from neutron DB agents table
    def fetch_network_node_details(self, docs):
        hosts = {}
        for doc in docs:
            hosts[doc["host"]] = doc
        query = """
          SELECT DISTINCT host, host AS id, configurations
          FROM {}.agents
          WHERE agent_type IN ('Metadata agent', 'DHCP agent', 'L3 agent')
        """.format(self.neutron_db)
        results = self.get_objects_list(query, "")
        for r in results:
            host = r["host"]
            if host not in hosts:
                self.log.error("host from agents table not in hosts list: {}"
                               .format(host))
                continue
            host = hosts[host]
            host["config"] = json.loads(r["configurations"])
            self.add_host_type(host, "Network", '')

    # fetch ip_address from nova.compute_nodes table if possible
    def fetch_compute_node_ip_address(self, doc, h):
        query = """
      SELECT host_ip AS ip_address
      FROM nova.compute_nodes
      WHERE hypervisor_hostname = %s
    """
        results = self.get_objects_list_for_id(query, "", h)
        for db_row in results:
            doc.update(db_row)

    def add_host_type(self, doc, host_type, zone):
        if host_type not in doc["host_type"]:
            doc["host_type"].append(host_type)
            if host_type.lower() == 'compute':
                az_doc = self.availability_zones.get(zone)
                if az_doc:
                    doc['zone'] = az_doc["name"]
                    doc['parent_id'] = az_doc["id"]

    def fetch_ironic_instances(self):
        # temp solution here , until we fully support ironic bare-metals
        # ironic instance is bare-metal host/node fully assigned to a tenant
        req_url = "{}/v1/nodes/detail".format(self.ironic_endpoint)
        try:
            response = self.get_url(req_url, {"X-Auth-Token": self.token["id"]})
        # Ironic is an optional API, we might have environment with no Ironic
        except (exceptions.ConnectionError, exceptions.ConnectTimeout):
            response = None
        ironic_instances = []
        if response is not None:
            nodes = response["nodes"]
            ports = []
            for node in nodes:
                ironic_instances.append(node)
                ports_url = "{}/v1/nodes/{}/ports".format(self.ironic_endpoint, node["uuid"])
                ports_resp = self.get_url(ports_url, {"X-Auth-Token": self.token["id"]})
                if ports_resp is not None:
                    ports = ports_resp["ports"]
            for ironic in ironic_instances:
                ironic.update({"id": ironic["uuid"], "ports": ports,
                               "name": "ironic-{}".format(ironic["uuid"]),
                               "host_type": ["Bare_metal"],
                               "host": "host-{}".format(ironic["uuid"]),
                               "zone": "ironic",
                               "services": {"ironic-compute": {"created_at": ironic["created_at"],
                                                               "updated_at": ironic["updated_at"]}},
                               "OS": {"name": "Red Hat Enterprise Linux Server"}
                               })
                for e in ["links", "uuid"]:
                    ironic.pop(e)
        return ironic_instances
