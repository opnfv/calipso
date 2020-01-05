###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from scan.fetchers.kube.kube_fetch_containers import KubeFetchContainers
from scan.link_finders.find_links import FindLinks


class FindLinksForContainers(FindLinks):

    def add_links(self):
        containers = self.inv.find_items({
            'environment': self.get_env(),
            'type': 'container'
        })
        self.log.info('adding links of type: container-vnic, container-network')
        for container in containers:
            self.find_matching_vnic(container)
            self.find_matching_vedge(container)
            self.find_container_network_links(container)

    def find_matching_vnic(self, container):
        vnic_cond = {
            'environment': self.get_env(),
            'type': 'vnic',
            'host': container['host']
        }
        if 'VPP' in self.configuration.environment.get('mechanism_drivers'):
            vnic_cond['ip_address'] = container['ip_address']
        else:
            if 'vnic_index' not in container or not container['vnic_index']:
                return
            vnic_cond['index'] = container['vnic_index']
        vnic = self.inv.find_one(vnic_cond)
        if vnic:
            self.add_container_vnic_link(container, vnic)

    def add_container_vnic_link(self, container, vnic):
        # link_type: 'container-vnic'
        link_name = vnic['mac_address']
        attributes = dict(container_vnic=vnic['object_name'])
        if 'network' in container:
            vnic['network'] = container['network']
            self.inv.set(vnic)
            attributes['network'] = container['network']
        self.link_items(container, vnic, link_name=link_name,
                        extra_attributes=attributes)

    def find_matching_vedge(self, container):
        if container.get('container_app', '') != KubeFetchContainers.PROXY_ATTR:
            return
        vedge = self.inv.find_one({
            'environment': self.get_env(),
            'type': 'vedge',
            'host': container['host']
        })
        if not vedge:
            return
        self.add_container_vedge_link(container, vedge)

    def add_container_vedge_link(self, container, vedge):
        # link_type: 'container-vedge'
        mechanism = self.configuration.environment['mechanism_drivers'][0]
        link_name = '{}-{}-{}'.format(container['object_name'],
                                      vedge['parent_id'],
                                      mechanism)
        if 'network' in container:
            attributes = dict(network=container['network'])
        else:
            attributes = None
        self.link_items(source=container, target=vedge,
                        link_name=link_name,
                        extra_attributes=attributes)

    def find_container_network_links(self, container):
        # link_type = 'container-network'
        if container.get('network', ''):
            network = self.inv.get_by_id(self.get_env(),
                                         container['network'])
            if not network:
                self.log.error('unable to find network {} in container {}'
                               .format(container['network'],
                                       container['name']))
            link_name = '{}-{}'.format(container['object_name'],
                                       network['type'])
            self.link_items(source=container, target=network,
                            link_name=link_name)
