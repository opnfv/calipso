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

from discover.link_finders.find_links import FindLinks
from utils.util import decode_aci_dn


class FindLinksForPnics(FindLinks):
    def __init__(self):
        super().__init__()

    def add_links(self):
        self.log.info("adding links of type: pnic-network, "
                      "host_pnic-switch_pnic, switch-host_pnic")
        pnics = self.inv.find_items({
            "environment": self.get_env(),
            "type": "host_pnic"
        })
        for pnic in pnics:
            self.add_pnic_network_links(pnic)
            self.add_host_pnic_to_switch_pnic_link(pnic)

        self.log.info("adding links of type: switch_pnic-switch_pnic, "
                      "switch-switch_pnic")
        pnics = self.inv.find_items({
            "environment": self.get_env(),
            "type": "switch_pnic",
        })
        for pnic in pnics:
            self.add_switch_to_pnic_link(pnic)
            if pnic["role"] == "uplink":
                self.add_switch_pnic_to_switch_pnic_link(pnic)

    def add_pnic_network_links(self, pnic):
        host = pnic["host"]
        if self.configuration.get_env_config()['type_drivers'] == "vlan":
            # take this pnic only if we can find matching vedge-pnic links
            matches = self.inv.find({
                "environment": self.get_env(),
                "link_type": "vedge-host_pnic",
                "host": host,
                "target_id": pnic["id"]},
                projection={"_id": 1},
                collection="links",
                get_single=True)
            if not matches:
                return
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
            link_type = "host_pnic-network"
            link_name = "Segment-" + str(network["provider:segmentation_id"]) \
                if "provider:segmentation_id" in network \
                else "Segment-None"
            state = "up" if pnic["Link detected"] == "yes" else "down"
            link_weight = 0  # TBD
            attributes = {"network": target_id}
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
            "type": "switch_pnic",
            "mac_address": host_pnic["mac_address"]},
            get_single=True)
        if not switch_pnic:
            return
        source = host_pnic["_id"]
        source_id = host_pnic["id"]
        target = switch_pnic["_id"]
        target_id = switch_pnic["id"]
        link_type = "host_pnic-switch_pnic"
        link_name = "{}-{}".format(host_pnic['host'],
                                   switch_pnic['parent_id'])
        state = "up" if host_pnic["Link detected"] == "yes" else "down"
        link_weight = 0  # TBD
        self.create_link(self.get_env(),
                         source, source_id, target, target_id,
                         link_type, link_name, state, link_weight,
                         host=host_pnic['host'])

    def add_switch_pnic_to_switch_pnic_link(self, leaf_pnic):
        spine_pnic = self.inv.get_by_id(self.get_env(),
                                        leaf_pnic['connected_to'])
        if not spine_pnic:
            return
        source = leaf_pnic["_id"]
        source_id = leaf_pnic["id"]
        target = spine_pnic["_id"]
        target_id = spine_pnic["id"]
        link_type = "switch_pnic-switch_pnic"
        if_id_matches = re.search("(eth.*)$", source_id)
        link_name = decode_aci_dn(if_id_matches.group(1))
        state = "up"  # TBD
        link_weight = 0  # TBD
        self.create_link(self.get_env(),
                         source, source_id, target, target_id,
                         link_type, link_name, state, link_weight,
                         switch=leaf_pnic['switch'])

    def add_switch_to_pnic_link(self, pnic):
        switch = self.inv.get_by_id(self.get_env(), pnic['parent_id'])
        if not switch:
            return
        source = switch["_id"]
        source_id = switch["id"]
        target = pnic["_id"]
        target_id = pnic["id"]
        link_type = "switch-{}".format(pnic['type'])
        link_name = "{}={}".format(switch["object_name"], pnic["object_name"])
        state = "up"  # TBD
        link_weight = 0  # TBD
        self.create_link(self.get_env(),
                         source, source_id, target, target_id,
                         link_type, link_name, state, link_weight,
                         switch=switch['id'])
