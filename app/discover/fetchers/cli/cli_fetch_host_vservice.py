###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re

from discover.fetchers.cli.cli_access import CliAccess
from discover.fetchers.db.db_access import DbAccess
from discover.network_agents_list import NetworkAgentsList
from utils.inventory_mgr import InventoryMgr


class CliFetchHostVservice(CliAccess, DbAccess):
    def __init__(self):
        super(CliFetchHostVservice, self).__init__()
        # match only DHCP agent and router (L3 agent)
        self.type_re = re.compile("^q(dhcp|router)-")
        self.inv = InventoryMgr()
        self.agents_list = NetworkAgentsList()

    def get_vservice(self, host_id, name_space):
        result = {"local_service_id": name_space}
        self.set_details(host_id, result)
        return result

    def set_details(self, host_id, r):
        # keep the index without prefix
        id_full = r["local_service_id"].strip()
        prefix, id_clean = re.match("([A-Za-z]+)-([0-9A-Za-z\-]+)",
                                    id_full).groups()
        r["service_type"] = prefix
        name = self.get_router_name(r, id_clean) if prefix[1:] == "router" \
            else self.get_network_name(id_clean)
        r["name"] = prefix + "-" + name
        r["host"] = host_id
        r["id"] = id_full
        self.set_agent_type(r)

    def get_network_name(self, id):
        query = """
                SELECT name
                FROM {}.networks
                WHERE id = %s
                """.format(self.neutron_db)
        results = self.get_objects_list_for_id(query, "router", id)
        if not list(results):
            return id
        for db_row in results:
            return db_row["name"]

    def get_router_name(self, r, id):
        query = """
                SELECT *
                FROM {}.routers
                WHERE id = %s
                """.format(self.neutron_db)
        results = self.get_objects_list_for_id(query, "router", id.strip())
        for db_row in results:
            r.update(db_row)
        return r["name"]

    # dynamically create sub-folder for vService by type
    def set_agent_type(self, o):
        o["master_parent_id"] = o["host"] + "-vservices"
        o["master_parent_type"] = "vservices_folder"
        atype = o["service_type"]
        agent = self.agents_list.get_type(atype)
        try:
            o["parent_id"] = o["master_parent_id"] + "-" + agent["type"] + "s"
            o["parent_type"] = "vservice_" + agent["type"] + "s_folder"
            o["parent_text"] = agent["folder_text"]
        except KeyError:
            o["parent_id"] = o["master_parent_id"] + "-" + "miscellenaous"
            o["parent_type"] = "vservice_miscellenaous_folder"
            o["parent_text"] = "Misc. services"
