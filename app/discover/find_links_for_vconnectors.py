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


class FindLinksForVconnectors(FindLinks):
    def __init__(self):
        super().__init__()

    def add_links(self):
        vconnectors = self.inv.find_items({
            "environment": self.get_env(),
            "type": "vconnector"
        })
        self.log.info("adding links of type: vnic-vconnector, vconnector-pnic")
        for vconnector in vconnectors:
            for interface in vconnector["interfaces_names"]:
                self.add_vnic_vconnector_link(vconnector, interface)
                self.add_vconnector_pnic_link(vconnector, interface)

    def add_vnic_vconnector_link(self, vconnector, interface_name):
        mechanism_drivers = self.configuration.environment['mechanism_drivers']
        is_ovs = mechanism_drivers and mechanism_drivers[0] == 'OVS'
        if is_ovs:
            # interface ID for OVS
            vnic = self.inv.get_by_id(self.get_env(), interface_name)
        else:
            # interface ID for VPP - match interface MAC address to vNIC MAC
            interface = vconnector['interfaces'][interface_name]
            if not interface or 'mac_address' not in interface:
                return
            vnic_mac = interface['mac_address']
            vnic = self.inv.get_by_field(self.get_env(), 'vnic',
                                         'mac_address', vnic_mac,
                                         get_single=True)
        if not vnic:
            return
        host = vnic["host"]
        source = vnic["_id"]
        source_id = vnic["id"]
        target = vconnector["_id"]
        target_id = vconnector["id"]
        link_type = "vnic-vconnector"
        link_name = vnic["mac_address"]
        state = "up"  # TBD
        link_weight = 0  # TBD
        attributes = {}
        if 'network' in vnic:
            attributes = {'network': vnic['network']}
            vconnector['network'] = vnic['network']
            self.inv.set(vconnector)
        self.create_link(self.get_env(),
                         source, source_id, target, target_id,
                         link_type, link_name, state, link_weight,
                         host=host,
                         extra_attributes=attributes)

    def add_vconnector_pnic_link(self, vconnector, interface):
        ifname = interface['name'] if isinstance(interface, dict) else interface
        if "." in ifname:
            ifname = ifname[:ifname.index(".")]
        host = vconnector["host"]
        pnic = self.inv.find_items({
            "environment": self.get_env(),
            "type": "pnic",
            "host": vconnector["host"],
            "name": ifname
        }, get_single=True)
        if not pnic:
            return
        source = vconnector["_id"]
        source_id = vconnector["id"]
        target = pnic["_id"]
        target_id = pnic["id"]
        link_type = "vconnector-pnic"
        link_name = pnic["name"]
        state = "up"  # TBD
        link_weight = 0  # TBD
        self.create_link(self.get_env(),
                         source, source_id,
                         target, target_id,
                         link_type, link_name, state, link_weight,
                         host=host)
