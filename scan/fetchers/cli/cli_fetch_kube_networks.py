###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json
from json import JSONDecodeError

from base.utils.inventory_mgr import InventoryMgr
from scan.fetchers.cli.cli_fetcher import CliFetcher


class CliFetchKubeNetworks(CliFetcher):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def get(self, host_id: str) -> list:
        host = self.inv.get_by_id(self.get_env(), host_id)
        if not host:
            self.log.error('Failed to find host with ID: {}', host_id)
            return []
        lines = self.run_fetch_lines('docker network ls', host_id)
        ret = []
        headers = [
            'NETWORK ID',
            'NAME',
            'DRIVER',
            'SCOPE'
        ]
        networks = self.parse_cmd_result_with_whitespace(lines, headers, True)
        for network in networks:
            new_network = self.get_network(host, network)
            if new_network:
                ret.append(new_network)
        return ret

    def get_network(self, host, network_data) -> dict:
        host_id = host['host']
        name = network_data['NAME']
        network = {
            'hosts': [{"name": host_id}],
            'local_name': name,
            'name': name,
            'driver': {'type': network_data['DRIVER']},
            'scope': network_data['SCOPE']
        }
        self.get_network_data(network, host_id)
        network_id = network['id']
        existing_network = self.inv.get_by_id(self.get_env(), network_id)
        if existing_network:
            self.add_host_to_network(existing_network, host_id)
            return {}
        self.set_folder_parent(network, 'network',
                               master_parent_type='environment',
                               master_parent_id=self.get_env())
        return network

    def get_network_data(self, network, host_id):
        cmd = 'docker network inspect {}'.format(network['local_name'])
        output = self.run(cmd, host_id)
        try:
            network_data = json.loads(output)
        except JSONDecodeError as e:
            self.log.error('error reading network data for {}: {}'
                           .format(network['id'], str(e)))
            return
        network_data = network_data[0]
        containers_list = []
        for container_id, container_doc in network_data.get('Containers', {}).items():
            container_doc['ContainerID'] = container_id
            containers_list.append(container_doc)
        network_data['Containers'] = containers_list

        # until we find why long network ID is shared between hosts, we'll call
        # it 'network_id' and use the name as the ID for the networks
        network_data['id'] = network_data.pop('Id')
        # add 'network' attribute to network itself to allow putting
        # a constraint on cliques with network as focal point
        network_data['network'] = network_data['id']
        network_data.pop('Name')
        network_data.pop('Driver')
        network_data.pop('Scope')
        network.update(network_data)

    def add_host_to_network(self, existing_network, host_id):
        hosts_list = existing_network['hosts']
        if host_id in (h["name"] for h in existing_network['hosts']):
            return
        hosts_list.append({"name": host_id})
        existing_network['hosts'] = hosts_list
        old_name = existing_network['name']
        new_name = existing_network['local_name']
        if new_name == old_name:
            return
        old_name_path = existing_network['name_path']
        old_name_part = '/Networks/{}'.format(old_name)
        new_name_part = '/Networks/{}'.format(new_name)
        existing_network['name'] = new_name
        existing_network['name_path'] = old_name_path.replace(old_name_part,
                                                              new_name_part)
        self.inv.set(existing_network)
