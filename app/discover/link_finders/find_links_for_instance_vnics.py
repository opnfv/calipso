###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.link_finders.find_links import FindLinks


class FindLinksForInstanceVnics(FindLinks):
    def __init__(self):
        super().__init__()

    def add_links(self):
        self.log.info("adding links of type: instance-vnic")
        vnics = self.inv.find_items({
            "environment": self.get_env(),
            "type": "vnic",
            "vnic_type": "instance_vnic"
        })
        for v in vnics:
            self.add_link_for_vnic(v)

    def add_link_for_vnic(self, v):
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
        source = instance["_id"]
        source_id = instance["id"]
        target = v["_id"]
        target_id = v["id"]
        link_type = "instance-vnic"
        # find related network
        network_name = None
        network_id = None
        for net in instance["network_info"]:
            if "{}-{}".format(v["host"], net["devname"]) == v["id"]:
                network_name = net["network"]["label"]
                network_id = net['network']['id']
                v['network'] = network_id
                self.inv.set(v)
                if self.inv.monitoring_setup_manager:
                    self.inv.monitoring_setup_manager.create_setup(instance)
                break
        state = "up"  # TBD
        link_weight = 0  # TBD
        attributes = {} if not network_id else {'network': network_id}
        self.create_link(self.get_env(),
                         source, source_id, target, target_id,
                         link_type, network_name, state, link_weight,
                         host=host["name"],
                         extra_attributes=attributes)
