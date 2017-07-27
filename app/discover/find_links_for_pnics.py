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


class FindLinksForPnics(FindLinks):
    def __init__(self):
        super().__init__()

    def add_links(self):
        pnics = self.inv.find_items({
            "environment": self.get_env(),
            "type": "pnic",
            "pnic_type": {"$ne": "switch"}  # TODO: make a more educated guess
        })
        for pnic in pnics:
            self.add_pnic_network_links(pnic)

    def add_pnic_network_links(self, pnic):
        self.log.info("adding links of type: pnic-network")
        host = pnic["host"]
        # find ports for that host, and fetch just the network ID
        ports = self.inv.find_items({
            "environment": self.get_env(),
            "type": "port",
            "binding:host_id": host
        }, {"network_id": 1, "id": 1})
        networks = {}
        for port in ports:
            networks[port["network_id"]] = 1
        for network_id in networks.keys():
            network = self.inv.get_by_id(self.get_env(), network_id)
            if network == []:
                return
            source = pnic["_id"]
            source_id = pnic["id"]
            target = network["_id"]
            target_id = network["id"]
            link_type = "pnic-network"
            link_name = "Segment-" + str(network["provider:segmentation_id"]) \
                if "provider:segmentation_id" in network \
                else "Segment-None"
            state = "up" if pnic["Link detected"] == "yes" else "down"
            link_weight = 0  # TBD
            source_label = "port-" + pnic["port_id"] if "port_id" in pnic \
                else ""
            self.create_link(self.get_env(), host,
                             source, source_id, target, target_id,
                             link_type, link_name, state, link_weight,
                             source_label,
                             extra_attributes={"network": target_id})
