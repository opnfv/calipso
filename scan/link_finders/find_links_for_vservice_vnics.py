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


class FindLinksForVserviceVnics(FindLinks):

    def add_links(self, search=None):
        self.log.info("adding links of type: vservice-vnic")

        if search is None:
            search = {}

        search.update({"environment": self.get_env(),
                       "type": "vnic",
                       "vnic_type": "vservice_vnic"})

        vnics = self.inv.find_items(search)

        for v in vnics:
            self.add_link_for_vnic(v)

    def add_link_for_vnic(self, v):
        # link_type: "vservice-vnic"
        host = self.inv.get_by_id(self.get_env(), v["host"])
        if "Network" not in host["host_type"]:
            return
        vservice_id = v["parent_id"]
        vservice_id = vservice_id[:vservice_id.rindex('-')]
        vservice = self.inv.get_by_id(self.get_env(), vservice_id)
        extra_attributes = {'vedge_type': v['vedge_type']}
        link_name = None
        if "network" in v:
            network = self.inv.get_by_id(self.get_env(), v["network"])
            link_name = network["name"]
            extra_attributes['network'] = v['network']
        self.link_items(vservice, v, link_name=link_name, host=v["host"],
                        extra_attributes=extra_attributes)
