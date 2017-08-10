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

from discover.find_links import FindLinks


class FindLinksForPnics(FindLinks):
    def __init__(self):
        super().__init__()

    def add_links(self):
        pnics = self.inv.find_items({
            "environment": self.get_env(),
            "type": "pnic",
            "pnic_type": "host"
        })
        self.log.info("adding links of type: pnic-network, host-switch")
        for pnic in pnics:
            self.add_pnic_network_links(pnic)
            self.add_host_pnic_to_switch_pnic_link(pnic)
        pnics = self.inv.find_items({
            "environment": self.get_env(),
            "type": "pnic",
            "pnic_type": "switch",
            "role": "uplink"
        })
        self.log.info("adding links of type: switch-switch")
        for pnic in pnics:
            self.add_switch_to_switch_link(pnic)

    def add_pnic_network_links(self, pnic):
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
            if not network:
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
            attributes={"network": target_id}
            if "port_id" in pnic:
                attributes['source_label'] = "port-" + pnic["port_id"]
            self.create_link(self.get_env(),
                             source, source_id, target, target_id,
                             link_type, link_name, state, link_weight,
                             host=host,
                             extra_attributes=attributes)

    def add_host_pnic_to_switch_pnic_link(self, host_pnic):
        switch_pnic = self.inv.find_items({
            "environment": self.get_env(),
            "type": "pnic",
            "pnic_type": "switch",
            "mac_address": host_pnic["mac_address"]},
            get_single=True)
        if not switch_pnic:
            return
        source = host_pnic["_id"]
        source_id = host_pnic["id"]
        target = switch_pnic["_id"]
        target_id = switch_pnic["id"]
        link_type = "host-switch"
        link_name = "{}-{}".format(host_pnic['host'],
                                   switch_pnic['parent_id'])
        state = "up" if host_pnic["Link detected"] == "yes" else "down"
        link_weight = 0  # TBD
        self.create_link(self.get_env(),
                         source, source_id, target, target_id,
                         link_type, link_name, state, link_weight,
                         host=host_pnic['host'])

    def add_switch_to_switch_link(self, leaf_pnic):
        spine_pnic = self.inv.get_by_id(self.get_env(),
                                        leaf_pnic['connected_to'])
        if not spine_pnic:
            return
        source = leaf_pnic["_id"]
        source_id = leaf_pnic["id"]
        target = spine_pnic["_id"]
        target_id = spine_pnic["id"]
        link_type = "switch-switch"
        if_id_matches = re.search("(eth.*)$", source_id)
        link_name = if_id_matches.group(1).replace("__", "/")
        state = "up"  # TBD
        link_weight = 0  # TBD
        self.create_link(self.get_env(),
                         source, source_id, target, target_id,
                         link_type, link_name, state, link_weight,
                         switch=leaf_pnic['switch'])