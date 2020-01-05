###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re

from base.utils.configuration import Configuration
from base.utils.origins import Origin
from base.utils.util import decode_aci_dn
from scan.link_finders.find_links import FindLinks


class FindLinksForPnics(FindLinks):
    def __init__(self):
        super().__init__()
        self.environment_type = None

    def setup(self, env, origin: Origin = None):
        super().setup(env, origin)
        self.configuration = Configuration()
        self.environment_type = self.configuration.get_env_type()

    def add_links(self):
        self.log.info("adding links of type: pnic-network, "
                      "host_pnic-switch_pnic, switch-switch_pnic")
        pnics = self.inv.find_items({
            "environment": self.get_env(),
            "type": "host_pnic"
        })
        aci_enabled = self.configuration.environment.get('aci_enabled')
        for pnic in pnics:
            self.add_pnic_network_links(pnic)
            if aci_enabled is True:
                self.add_host_pnic_to_switch_pnic_link(pnic)

        if aci_enabled is True:
            self.log.info("adding links of type: switch_pnic-switch_pnic, "
                          "switch-switch_pnic")
            pnics = self.inv.find_items({
                "environment": self.get_env(),
                "type": "switch_pnic",
            })
            for pnic in pnics:
                self.add_switch_to_pnic_link(pnic)
                if pnic.get('role', '') == 'uplink':
                    self.add_switch_pnic_to_switch_pnic_link(pnic)

    def add_pnic_network_links(self, pnic):
        if self.environment_type == self.ENV_TYPE_OPENSTACK:
            self.add_openstack_pnic_network_links(pnic)
        if self.environment_type == self.ENV_TYPE_KUBERNETES:
            self.add_kubernetes_pnic_network_links(pnic)

    def add_openstack_pnic_network_links(self, pnic):
        # link_type: "host_pnic-network"
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
            link_name = "Segment-" + str(network["provider:segmentation_id"]) \
                if "provider:segmentation_id" in network \
                else "Segment-None"
            state = "up" if pnic["Link detected"] == "yes" else "down"
            attributes = {"network": network['id']}
            if "port_id" in pnic:
                attributes['source_label'] = "port-" + pnic["port_id"]
            self.link_items(pnic, network, link_name=link_name, state=state,
                            extra_attributes=attributes)

    def add_kubernetes_pnic_network_links(self, pnic):
        networks = self.inv.find_items({
            'environment': self.get_env(),
            'type': 'network'
        })
        for network in networks:
            self.add_kubernetes_pnic_network_link(pnic, network)

    def add_kubernetes_pnic_network_link(self, pnic, network):
        # link_type: 'host_pnic-network'
        link_name = '{}-{}'.format(pnic['object_name'], network['object_name'])
        attributes = {'network': network['id']}
        if 'port_id' in pnic:
            attributes['source_label'] = 'port-' + pnic['port_id']
        self.link_items(pnic, network, link_name=link_name,
                        extra_attributes=attributes)

    def add_host_pnic_to_switch_pnic_link(self, host_pnic):
        # link_type: "host_pnic-switch_pnic"
        mac_address = host_pnic.get("mac_address")
        if not mac_address:
            return

        switch_pnic = self.inv.find_items({
            "environment": self.get_env(),
            "type": "switch_pnic",
            "mac_address": host_pnic["mac_address"]},
            get_single=True)
        if not switch_pnic:
            return
        link_name = "{}-{}".format(host_pnic['host'],
                                   switch_pnic['parent_id'])
        state = "up" if host_pnic["Link detected"] == "yes" else "down"
        self.link_items(host_pnic, switch_pnic, host=host_pnic['host'],
                        state=state, link_name=link_name)

    def add_switch_pnic_to_switch_pnic_link(self, leaf_pnic):
        # link_type: "switch_pnic-switch_pnic"
        spine_pnic = self.inv.get_by_id(self.get_env(),
                                        leaf_pnic['connected_to'])
        if not spine_pnic:
            return
        if_id_matches = re.search("(eth.*)$", leaf_pnic['id'])
        link_name = decode_aci_dn(if_id_matches.group(1))
        self.link_items(leaf_pnic, spine_pnic, link_name=link_name)

    def add_switch_to_pnic_link(self, pnic):
        # link_type: switch-host_pnic, switch-switch_pnic
        switch = self.inv.get_by_id(self.get_env(), pnic['parent_id'])
        if not switch:
            return
        self.link_items(switch, pnic, switch=switch['id'])
