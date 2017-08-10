###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.find_links import FindLinks


class FindLinksForOteps(FindLinks):
    def __init__(self):
        super().__init__()

    def add_links(self):
        self.log.info("adding link types: " +
                      "vedge-otep, otep-vconnector, otep-host_pnic")
        oteps = self.inv.find_items({
            "environment": self.get_env(),
            "type": "otep"
        })
        for otep in oteps:
            self.add_vedge_otep_link(otep)
            self.add_otep_vconnector_link(otep)
            self.add_otep_pnic_link(otep)

    def add_vedge_otep_link(self, otep):
        vedge = self.inv.get_by_id(self.get_env(), otep["parent_id"])
        source = vedge["_id"]
        source_id = vedge["id"]
        target = otep["_id"]
        target_id = otep["id"]
        link_type = "vedge-otep"
        link_name = vedge["name"] + "-otep"
        state = "up"  # TBD
        link_weight = 0  # TBD
        self.create_link(self.get_env(),
                         source, source_id, target, target_id,
                         link_type, link_name, state, link_weight,
                         host=vedge["host"])

    def add_otep_vconnector_link(self, otep):
        if "vconnector" not in otep:
            return
        vconnector = self.inv.find_items({
            "environment": self.get_env(),
            "type": "vconnector",
            "host": otep["host"],
            "name": otep["vconnector"]
        }, get_single=True)
        if not vconnector:
            return
        source = otep["_id"]
        source_id = otep["id"]
        target = vconnector["_id"]
        target_id = vconnector["id"]
        link_type = "otep-vconnector"
        link_name = otep["name"] + "-" + otep["vconnector"]
        state = "up"  # TBD
        link_weight = 0  # TBD
        self.create_link(self.get_env(),
                         source, source_id, target, target_id,
                         link_type, link_name, state, link_weight,
                         host=otep["host"])

    def add_otep_pnic_link(self, otep):
        pnic = self.inv.find_items({
            "environment": self.get_env(),
            "type": "host_pnic",
            "host": otep["host"],
            "IP Address": otep["ip_address"]
        }, get_single=True)
        if not pnic:
            return
        source = otep["_id"]
        source_id = otep["id"]
        target = pnic["_id"]
        target_id = pnic["id"]
        link_type = "otep-host_pnic"
        link_name = otep["host"] + "pnic" + pnic["name"]
        state = "up"  # TBD
        link_weight = 0  # TBD
        self.create_link(self.get_env(),
                         source, source_id, target, target_id,
                         link_type, link_name, state, link_weight,
                         host=otep["host"])
