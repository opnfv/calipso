###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re

from base.utils.inventory_mgr import InventoryMgr
from scan.fetchers.cli.cli_fetcher import CliFetcher
from scan.fetchers.db.db_access import DbAccess


class DbFetchOteps(DbAccess, CliFetcher):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()
        self.port_re = re.compile("^\s*port (\d+): ([^(]+)( \(internal\))?$")

    def get(self, id):
        vedge = self.inv.get_by_id(self.get_env(), id)
        tunnel_type = None
        if "configurations" not in vedge:
            return []
        if "tunnel_types" not in vedge["configurations"]:
            return []
        if not vedge["configurations"]["tunnel_types"]:
            return []
        tunnel_type = vedge["configurations"]["tunnel_types"][0]
        host_id = vedge["host"]
        table_name = "{}.ml2_{}_endpoints".format(self.neutron_db, tunnel_type)
        env_config = self.config.get_env_config()
        distribution = env_config["distribution"]
        distribution_version = env_config["distribution_version"]
        dist_ver = "{}-{}".format(distribution, distribution_version)
        if dist_ver == "Canonical-icehouse":
            # for Icehouse, we only get IP address from the DB, so take the
            # host IP address and from the host data in Mongo
            host = self.inv.get_by_id(self.get_env(), host_id)
            results = [{"host": host_id, "ip_address": host["ip_address"]}]
        else:
            results = self.get_objects_list_for_id(
                """
                SELECT *
                FROM {}
                WHERE host = %s
                """.format(table_name),
                "vedge", host_id)
        for doc in results:
            doc["id"] = host_id + "-otep"
            doc["name"] = doc["id"]
            doc["host"] = host_id
            doc["overlay_type"] = tunnel_type
            doc["ports"] = vedge["tunnel_ports"] if "tunnel_ports" in vedge else []
            if "udp_port" not in doc:
                doc["udp_port"] = "67"
            self.get_vconnector(doc, host_id, vedge)

        return results

    # find matching vConnector by tunneling_ip of vEdge
    # look for that IP address in 'ip address show' output for the host
    def get_vconnector(self, doc, host_id, vedge):
        tunneling_ip = vedge["configurations"]["tunneling_ip"]
        output_lines = self.run_fetch_lines("ip address show", host_id)
        interface = None
        ip_string = "    inet {}/".format(tunneling_ip)
        vconnector = None
        for l in output_lines:
            if l.startswith(" "):
                if interface and l.startswith(ip_string):
                    vconnector = interface
                    break
            else:
                if " " in l:
                    # line format is like this:
                    # <interface number>: <interface name>: ....
                    interface = l.split(":")[1].strip()

        if vconnector:
            doc["vconnector"] = '{}-{}'.format(host_id, vconnector)
