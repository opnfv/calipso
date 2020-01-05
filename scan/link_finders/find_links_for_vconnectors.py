###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import functools

from base.utils.configuration import Configuration
from base.utils.origins import Origin
from scan.link_finders.find_links import FindLinks


class FindLinksForVconnectors(FindLinks):
    def __init__(self):
        super().__init__()
        self.environment_type = None
        self.mechanism_drivers = None

    def setup(self, env, origin: Origin = None):
        super().setup(env, origin)
        self.configuration = Configuration()
        self.environment_type = self.configuration.get_env_type()
        self.mechanism_drivers = self.configuration.get_env_config().get('mechanism_drivers', [])

    def add_links(self):
        if self.environment_type == self.ENV_TYPE_OPENSTACK:
            self.log.info('adding links of type: vnic-vconnector, '
                          'vconnector-host_pnic')
        if self.environment_type == self.ENV_TYPE_KUBERNETES:
            self.log.info('adding links of type: vconnector-vedge')
        vconnectors = self.inv.find_items({
            'environment': self.get_env(),
            'type': 'vconnector'
        })
        for vconnector in vconnectors:
            for interface in vconnector["interfaces_names"]:
                self.add_vnic_vconnector_link(vconnector, interface)
                if self.environment_type == self.ENV_TYPE_OPENSTACK:
                    self.add_vconnector_pnic_link(vconnector, interface)
            if self.environment_type == self.ENV_TYPE_KUBERNETES \
                    and 'Flannel' in self.mechanism_drivers:
                self.add_k8s_vconnector_vedge_link(vconnector)

    def add_vnic_vconnector_link(self, vconnector, interface_name):
        # link_type: "vnic-vconnector"
        mech_drivers = self.mechanism_drivers
        ovs_or_flannel = 'OVS' in mech_drivers or 'Flannel' in mech_drivers
        if ovs_or_flannel:
            # interface ID for OVS
            search_func = functools.partial(self.inv.get_by_field,
                                            self.get_env(), 'vnic',
                                            field_value=interface_name, get_single=True)
            vnic = search_func(field_name='name')
            if not vnic:
                vnic = search_func(field_name='target.@dev')
        else:
            # interface ID for VPP - match interface MAC address to vNIC MAC
            interface = next(i for i in vconnector['interfaces'] if i['name'] == interface_name)
            if not interface or 'mac_address' not in interface:
                return
            vconnector_if_mac = interface['mac_address']
            vnic = self.inv.find_one({
                'environment': self.get_env(),
                'type': 'vnic',
                'host': vconnector['host'],
                'mac_address': vconnector_if_mac})
        if not vnic:
            return
        link_name = vnic["mac_address"]
        attributes = {'vedge_type': vnic['vedge_type']} if 'vedge_type' in vnic else {}

        if 'network' in vnic:
            attributes['network'] = vnic['network']
            vconnector['network'] = vnic['network']
            self.inv.set(vconnector)
        self.link_items(vnic, vconnector, link_name=link_name,
                        extra_attributes=attributes)

    def add_vconnector_pnic_link(self, vconnector, interface):
        # link_type: "vconnector-host_pnic"
        ifname = interface['name'] if isinstance(interface, dict) else interface
        if "." in ifname:
            ifname = ifname[:ifname.index(".")]
        pnic = self.inv.find_items({
            "environment": self.get_env(),
            "type": "host_pnic",
            "host": vconnector["host"],
            "name": ifname
        }, get_single=True)
        if not pnic:
            return
        self.link_items(vconnector, pnic, link_name=pnic["name"])

    def add_k8s_vconnector_vedge_link(self, vconnector):
        # link_type: 'vconnector-vedge'
        host = vconnector['host']
        prefix = '{}-cni'.format(host)
        if not vconnector['id'].startswith(prefix):
            return
        vedge = self.inv.find_one({
            'environment': self.get_env(),
            'type': 'vedge',
            'host': host
        })
        if not vedge:
            return

        attributes = {'vedge_type': vedge['vedge_type']} if 'vedge_type' in vedge else {}
        self.link_items(vconnector, vedge, link_name=vedge['name'], extra_attributes=attributes)
