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


class FindLinksForInstanceVnics(FindLinks):

    def add_links(self):
        self.log.info("adding links of type: instance-vnic")
        vnics = self.inv.find_items({
            "environment": self.get_env(),
            "type": "vnic",
            "vnic_type": "instance_vnic"
        })
        for v in vnics:
            self.add_link_for_vnic(v)

    @staticmethod
    def match_vnic_and_network(vnic, network):
        return (
            "{}|{}".format(vnic["host"], network["devname"]) == vnic["id"]
            or
            vnic["mac_address"] == network["address"]
        )

    def add_link_for_vnic(self, v):
        # link_type: "instance-vnic"
        instance = self.inv.get_by_id(self.get_env(), v["instance_id"])
        if "network_info" not in instance:
            self.log.warn("add_link_for_vnic: " +
                          "network_info missing in instance: %s ",
                          instance["id"])
            return
        host = self.inv.get_by_id(self.get_env(), instance["host"])
        host_types = host["host_type"]
        if "Network" not in host_types and "Compute" not in host_types:
            return []
        # find related network
        network_name = None
        network_id = None
        for net in instance["network_info"]:
            if self.match_vnic_and_network(v, net):
                network_name = net["network"]["label"]
                network_id = net['network']['id']
                v['network'] = network_id
                self.inv.set(v)
                if self.inv.monitoring_setup_manager:
                    self.inv.monitoring_setup_manager.create_setup(instance)
                break
        attributes = {'vedge_type': v.get('vedge_type')}
        if network_id:
            attributes['network'] = network_id
        self.link_items(instance, v, link_name=network_name,
                        host=host["name"],
                        extra_attributes=attributes)
