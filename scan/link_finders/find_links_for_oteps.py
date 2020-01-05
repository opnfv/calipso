###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from scan.link_finders.find_links import FindLinks


class FindLinksForOteps(FindLinks):

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
        # link_type: "vedge-otep"
        vedge = self.inv.get_by_id(self.get_env(), otep["parent_id"])
        link_name = vedge["name"] + "-otep"
        self.link_items(vedge, otep, link_name=link_name)

    def add_otep_vconnector_link(self, otep):
        # link_type: "otep-vconnector"
        if "vconnector" not in otep:
            return
        vconnector = self.inv.find_items({
            "environment": self.get_env(),
            "type": "vconnector",
            "host": otep["host"],
            "name": otep["vconnector"]
        }, get_single=True)
        link_name = otep["name"] + "-" + otep["vconnector"]
        self.link_items(otep, vconnector, link_name=link_name)

    def add_otep_pnic_link(self, otep):
        # link_type: "otep-host_pnic"
        pnic = self.inv.find_items({
            "environment": self.get_env(),
            "type": "host_pnic",
            "host": otep["host"],
            "IP Address": otep["ip_address"]
        }, get_single=True)
        if not pnic:
            return
        link_name = '{}-pnic-{}'.format(otep["host"], pnic["name"])
        self.link_items(otep, pnic, link_name=link_name)
