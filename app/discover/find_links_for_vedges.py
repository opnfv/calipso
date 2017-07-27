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


class FindLinksForVedges(FindLinks):
    def __init__(self):
        super().__init__()

    def add_links(self):
        self.log.info("adding link types: " +
                      "vnic-vedge, vconnector-vedge, vedge-pnic")
        vedges = self.inv.find_items({
            "environment": self.get_env(),
            "type": "vedge"
        })
        for vedge in vedges:
            ports = vedge["ports"]
            for p in ports.values():
                self.add_link_for_vedge(vedge, p)

    def add_link_for_vedge(self, vedge, port):
        vnic = self.inv.get_by_id(self.get_env(),
                                  vedge['host'] + '-' + port["name"])
        if not vnic:
            self.find_matching_vconnector(vedge, port)
            self.find_matching_pnic(vedge, port)
            return
        source = vnic["_id"]
        source_id = vnic["id"]
        target = vedge["_id"]
        target_id = vedge["id"]
        link_type = "vnic-vedge"
        link_name = vnic["name"] + "-" + vedge["name"]
        if "tag" in port:
            link_name += "-" + port["tag"]
        state = "up"  # TBD
        link_weight = 0  # TBD
        source_label = vnic["mac_address"]
        target_label = port["id"]
        self.create_link(self.get_env(), vedge["host"],
                         source, source_id, target, target_id,
                         link_type, link_name, state, link_weight,
                         source_label, target_label)

    def find_matching_vconnector(self, vedge, port):
        if self.configuration.has_network_plugin('VPP'):
            vconnector_interface_name = port['name']
        else:
            if not port["name"].startswith("qv"):
                return
            base_id = port["name"][3:]
            vconnector_interface_name = "qvb" + base_id
        vconnector = self.inv.find_items({
            "environment": self.get_env(),
            "type": "vconnector",
            "host": vedge['host'],
            'interfaces_names': vconnector_interface_name},
            get_single=True)
        if not vconnector:
            return
        source = vconnector["_id"]
        source_id = vconnector["id"]
        target = vedge["_id"]
        target_id = vedge["id"]
        link_type = "vconnector-vedge"
        link_name = "port-" + port["id"]
        if "tag" in port:
            link_name += "-" + port["tag"]
        state = "up"  # TBD
        link_weight = 0  # TBD
        source_label = vconnector_interface_name
        target_label = port["name"]
        mac_address = "Unknown"
        attributes = {'mac_address': mac_address}
        for interface in vconnector['interfaces'].values():
            if vconnector_interface_name != interface['name']:
                continue
            if 'mac_address' not in interface:
                continue
            mac_address = interface['mac_address']
            attributes['mac_address'] = mac_address
            break
        if 'network' in vconnector:
            attributes['network'] = vconnector['network']
        self.create_link(self.get_env(), vedge["host"],
                         source, source_id, target, target_id,
                         link_type, link_name, state, link_weight,
                         source_label, target_label,
                         attributes)

    def find_matching_pnic(self, vedge, port):
        pname = port["name"]
        if "pnic" in vedge:
            if pname != vedge["pnic"]:
                return
        elif self.configuration.has_network_plugin('VPP'):
            pass
        pnic = self.inv.find_items({
            "environment": self.get_env(),
            "type": "pnic",
            "host": vedge["host"],
            "name": pname
        }, get_single=True)
        if not pnic:
            return
        source = vedge["_id"]
        source_id = vedge["id"]
        target = pnic["_id"]
        target_id = pnic["id"]
        link_type = "vedge-pnic"
        link_name = "Port-" + port["id"]
        state = "up" if pnic["Link detected"] == "yes" else "down"
        link_weight = 0  # TBD
        self.create_link(self.get_env(), vedge["host"],
                         source, source_id, target, target_id,
                         link_type, link_name, state, link_weight)
