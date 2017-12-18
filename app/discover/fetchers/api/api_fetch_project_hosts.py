###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json

from discover.fetchers.api.api_access import ApiAccess
from discover.fetchers.db.db_access import DbAccess
from discover.fetchers.cli.cli_access import CliAccess
from utils.ssh_connection import SshError


class ApiFetchProjectHosts(ApiAccess, DbAccess, CliAccess):
    def __init__(self):
        super(ApiFetchProjectHosts, self).__init__()

    def get(self, project_id):
        if project_id != self.admin_project:
            # do not scan hosts except under project 'admin'
            return []
        token = self.v2_auth_pwd(self.admin_project)
        if not token:
            return []
        ret = []
        for region in self.regions:
            ret.extend(self.get_for_region(region, token))
        return ret

    def get_for_region(self, region, token):
        endpoint = self.get_region_url(region, "nova")
        ret = []
        if not token:
            return []
        req_url = endpoint + "/os-availability-zone/detail"
        headers = {
            "X-Auth-Project-Id": self.admin_project,
            "X-Auth-Token": token["id"]
        }
        response = self.get_url(req_url, headers)
        if "status" in response and int(response["status"]) != 200:
            return []
        az_info = response["availabilityZoneInfo"]
        hosts = {}
        for doc in az_info:
            az_hosts = self.get_hosts_from_az(doc)
            for h in az_hosts:
                if h["name"] in hosts:
                    # merge host_type data between AZs
                    existing_entry = hosts[h["name"]]
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
        doc = {
            "id": h,
            "host": h,
            "name": h,
            "zone": az["zoneName"],
            "parent_type": "availability_zone",
            "parent_id": az["zoneName"],
            "services": services,
            "host_type": []
        }
        if "nova-conductor" in services:
            s = services["nova-conductor"]
            if s["available"] and s["active"]:
                self.add_host_type(doc, "Controller", az['zoneName'])
        if "nova-compute" in services:
            s = services["nova-compute"]
            if s["available"] and s["active"]:
                self.add_host_type(doc, "Compute", az['zoneName'])
        self.fetch_host_os_details(doc)
        return doc

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

    @staticmethod
    def add_host_type(doc, host_type, zone):
        if host_type not in doc["host_type"]:
            doc["host_type"].append(host_type)
            if host_type == 'Compute':
                doc['zone'] = zone
                doc['parent_id'] = zone

    def fetch_host_os_details(self, doc):
        cmd = 'cat /etc/os-release && echo "ARCHITECURE=`arch`"'
        try:
            lines = self.run_fetch_lines(cmd, ssh_to_host=doc['host'])
        except SshError as e:
            self.log.error('{}: {}', cmd, str(e))
        os_attributes = {}
        attributes_to_fetch = {
            'NAME': 'name',
            'VERSION': 'version',
            'ID': 'ID',
            'ID_LIKE': 'ID_LIKE',
            'ARCHITECURE': 'architecure'
        }
        for attr in attributes_to_fetch:
            matches = [l for l in lines if l.startswith(attr + '=')]
            if matches:
                line = matches[0]
                attr_name = attributes_to_fetch[attr]
                os_attributes[attr_name] = line[line.index('=')+1:].strip('"')
        if os_attributes:
            doc['OS'] = os_attributes
