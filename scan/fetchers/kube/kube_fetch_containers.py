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
try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

from kubernetes.client.models import V1Container

from scan.fetchers.cli.cli_fetcher import CliFetcher
from scan.fetchers.kube.kube_access import KubeAccess
from base.utils.exceptions import CredentialsError, HostAddressError
from base.utils.ssh_connection import SshError


class KubeFetchContainers(KubeAccess, CliFetcher):

    PROXY_ATTR = 'kube-proxy'
    SANDBOX_ID_ATTR = 'io.kubernetes.sandbox.id'

    def get(self, parent_id) -> list:
        pod_id = parent_id.replace('-containers', '')
        pod_obj = self.inv.get_by_id(self.get_env(), pod_id)
        if not pod_obj:
            self.log.error('inventory has no pod with uid={}'.format(pod_id))
            return []

        # TODO: temporary
        if pod_obj.get('labels', {}).get('calipso-rancher-pod-for-kube-proxy'):
            return [self.get_rancher_proxy_container(pod_obj)]

        host = pod_obj['host']
        pod_filter = 'spec.nodeName={}'.format(host)
        pods = self.api.list_pod_for_all_namespaces(field_selector=pod_filter)
        ret = []
        if not pods or len(pods.items) == 0:
            self.log.error('failed to find pod with nodeName={}'.format(host))
            return []
        pod = next((pod for pod in pods.items if pod.metadata.uid == pod_id),
                   None)
        if not pod:
            self.log.error('failed to find pod with uid={}'.format(pod_id))
            return []
        for container in pod.spec.containers:
            ret.append(self.get_container(container, pod, pod_obj))
        return ret

    def get_rancher_proxy_container(self, pod_obj):
        doc = {
            'type': 'container',
            'namespace': pod_obj['namespace'],
            'host': pod_obj['host'],
            'pod': {'id': pod_obj['id'], 'name': pod_obj['object_name']},
            'id': '{}-kube-proxy'.format(pod_obj['id']),
            'name': 'kube-proxy',
            'container_id': 'kube-proxy'
        }
        self.get_container_config(doc, pod_obj)
        self.get_interface_link(doc, pod_obj)
        self.get_proxy_container_info(doc, pod_obj)
        return doc

    def get_container(self, container, pod, pod_obj):
        doc = {'type': 'container', 'environment': self.get_env(), 'namespace': pod.metadata.namespace}
        self.get_container_data(doc, container)
        self.fetch_container_status_data(doc, pod_obj)
        doc['host'] = pod_obj['host']
        doc['pod'] = dict(id=pod_obj['id'], name=pod_obj['object_name'])
        doc['ip_address'] = pod_obj.get('pod_status', {}).get('pod_ip', '')
        doc['id'] = '{}-{}'.format(pod_obj['id'], doc['name'])
        if doc.get('image'):
            doc['image'] = {"name": doc['image']}
        self.get_container_config(doc, pod_obj)
        self.get_interface_link(doc, pod_obj)
        self.get_proxy_container_info(doc, pod_obj)
        return doc

    @staticmethod
    def _get_state_from_container_status(container_status):
        for status_key in ('waiting', 'running', 'terminated'):
            if container_status.get('state', {}).get(status_key):
                return status_key

    def fetch_container_status_data(self, doc, pod_obj):
        container_statuses = pod_obj['pod_status']['container_statuses']
        container_status = next(s for s in container_statuses
                                if s['name'] == doc['name'])
        if not container_status:
            self.log.error('failed to find container_status record '
                           'for container {} in pod {}'
                           .format(doc['name'], pod_obj['name']))
            return
        container_id = container_status['container_id']
        if container_id is None:
            doc['container_type'] = container_status['name']
            doc['container_id'] = container_status['image']
        else:
            id_parts = container_id.split('://')
            doc['container_type'] = id_parts[0]
            doc['container_id'] = id_parts[1]
        doc['container_status'] = container_status
        doc['state'] = self._get_state_from_container_status(container_status)

    @staticmethod
    def get_container_data(doc: dict, container: V1Container):
        for k in dir(container):
            if k.startswith('_'):
                continue
            try:
                # TBD a lot of attributes from V1Container fail the saving to DB
                if k in ['to_dict', 'to_str', 'attribute_map', 'swagger_types',
                         'resources',
                         'liveness_probe',
                         'readiness_probe',
                         'security_context']:
                    continue
                val = getattr(container, k)
                if isinstance(val, classmethod):
                    continue
                if isinstance(val, staticmethod):
                    continue
                if val is not None:
                    doc[k] = val
            except AttributeError:
                pass

    def get_container_config(self, doc, pod_obj):
        if doc.get('state') == 'waiting':
            return

        cmd = 'docker inspect {}'.format(doc['container_id'])
        try:
            output = self.run(cmd, pod_obj['host'])
            data = json.loads(output)
        except SshError as e:
            self.log.warning('"docker inspect" cmd failed for container {}.\n'
                             'Error: {}'.format(doc['container_id'], e))
            return
        except JSONDecodeError as e:
            self.log.error('error reading output of cmd: {}, {}'
                           .format(cmd, str(e)))
            return
        if not data:
            return

        data = data[0]
        if 'State' in data:
            doc['container_state'] = data['State']
            doc['state'] = data['State']['Status']  # Prefer actual state to the one fetched from container_status
        if 'Config' in data:
            doc['config'] = data['Config']
            self.get_container_sandbox(doc, pod_obj)

    def get_container_sandbox(self, doc, pod_obj):
        sandbox_id = doc['config'].get('Labels').get(self.SANDBOX_ID_ATTR)
        if not sandbox_id:
            return

        cmd = 'docker inspect {}'.format(sandbox_id)
        output = self.run(cmd, pod_obj['host'])
        try:
            data = json.loads(output)
        except JSONDecodeError as e:
            self.log.error('error reading output of cmd: {}, {}'
                           .format(cmd, str(e)))
            return
        if not data:
            return

        doc['sandbox'] = data[0]
        self.find_network(doc)

    def get_interface_link(self, doc, pod_obj):
        if doc.get('state') != 'running' or doc['namespace'] == 'cattle-system' or doc['name'] == 'kubernetes-dashboard':
            doc['vnic_index'] = ''
            return

        interface_name = 'vpp1' if 'VPP' in self.configuration.environment['mechanism_drivers'] else 'eth0'
        file_name = "/sys/class/net/{}/iflink".format(interface_name)
        cmd = 'docker exec {0} sh -c "test -f {1} && cat {1} || exit 0"'.format(doc['container_id'], file_name)
        try:
            output = self.run(cmd, pod_obj['host'])
            doc['vnic_index'] = output.strip()
            self.add_container_to_vnic(doc, pod_obj)
        except (SshError, CredentialsError, HostAddressError):
            doc['vnic_index'] = ''

    # find network matching the one sandbox, and keep its name
    def find_network(self, doc):
        networks = doc['sandbox']['NetworkSettings']['Networks']
        if not networks:
            return
        if isinstance(networks, dict):
            network_names = list(networks.keys())
            network = network_names[0]
            network = networks[network]
        else:
            network = networks[0]
        network_id = network['NetworkID']
        network_obj = self.inv.get_by_id(self.get_env(), network_id)
        if not network_obj:
            return
        doc['network'] = network_id

    def add_container_to_vnic(self, container, pod_obj):
        condition = {
            'environment': self.get_env(),
            'type': 'vnic',
            'host': pod_obj['host'],
        }
        if 'VPP' in self.configuration.environment['mechanism_drivers']:
            condition['ip_address'] = container['ip_address']
        else:
            condition['index'] = container['vnic_index']
        vnic = self.inv.find_one(condition)
        if not vnic:
            return

        # TODO: figure out this logic
        # re-calc new ID and name path for vNIC and vNICs folder
        # self.set_folder_parent(vnic, object_type='vnic',
        #                        master_parent_id=container['id'],
        #                        master_parent_type='container')
        vnic_containers = vnic.get('containers', [])
        vnic_container = {'id': container['container_id'], 'name': container['name']}
        vnic['containers'] = vnic_containers.append(vnic_container) if vnic_containers else [vnic_container]
        self.inv.set(vnic)

        # self.inv.save_inventory_object(vnic,
        #                                parent=container,
        #                                environment=self.get_env())

    def get_proxy_container_info(self, container, pod_obj):
        if container['name'] != self.PROXY_ATTR:
            return
        container['container_app'] = self.PROXY_ATTR
        self.get_proxy_container_config(container)
        self.get_proxy_nat_tables(container)
        container['vservices'] = self.get_proxy_container_vservices(pod_obj)
        self.add_proxy_container_to_vservices(container)

    def get_proxy_container_config(self, container):
        command = container.get('command')
        if not command or not isinstance(command, list) or len(command) < 2:
            self.log.error('unable to find {} command file '
                           'for container {}'
                           .format(self.PROXY_ATTR, container['id']))
            return
        conf_line = command[1]
        if not isinstance(conf_line, str) \
                or not conf_line.startswith('--config='):
            self.log.error('unable to find {} command config file '
                           'for container {}'
                           .format(self.PROXY_ATTR, container['id']))
            return
        conf_file = conf_line[len('--config='):]
        cmd = 'docker exec {} cat  {}'.format(container['container_id'],
                                              conf_file)
        conf_file_contents = self.run(cmd=cmd, ssh_to_host=container['host'])
        container['kube_proxy_config'] = conf_file_contents

    def get_proxy_nat_tables(self, container):
        cmd = 'docker exec {} iptables -t nat -n -L' \
            .format(container['container_id'])
        nat_tables = self.run(cmd=cmd, ssh_to_host=container['host'])
        container['nat_tables'] = nat_tables

    def get_proxy_container_vservices(self, pod_obj: dict) -> list:
        pods = self.inv.find_items({
            'environment': self.get_env(),
            'type': 'pod',
            'host': pod_obj['host'],
            'vservices': {'$exists': 1}
        })
        vservices = []
        for pod in pods:
            vservices.extend(pod['vservices'])
        return vservices

    def add_proxy_container_to_vservices(self, container: dict):
        for vservice in list(container.get('vservices', [])):
            self.add_proxy_container_to_vservice(container, vservice)

    def add_proxy_container_to_vservice(self, container: dict, vservice: dict):
        vservice_obj = self.inv.get_by_id(self.get_env(), vservice['id'])
        if not vservice_obj:
            self.log.error('failed to find vservice object with id {} '
                           'in container {} (id: {})'
                           .format(vservice['id'],
                                   container['object_name'],
                                   container['id']))
        if self.PROXY_ATTR not in vservice_obj:
            vservice_obj[self.PROXY_ATTR] = []
        matches = [p for p in vservice_obj[self.PROXY_ATTR]
                   if p['id'] == container['id']]
        if not matches:
            proxy_data = dict(id=container['id'], name=container['name'],
                              host=container['host'])
            vservice_obj[self.PROXY_ATTR].append(proxy_data)
            self.inv.set(vservice_obj)
