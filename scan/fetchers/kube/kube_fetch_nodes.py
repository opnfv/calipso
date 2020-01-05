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
from kubernetes.client.models import V1Node, V1ObjectMeta, V1NodeSpec, \
    V1NodeStatus

from base.utils.origins import Origin
from base.utils.ssh_connection import SshError
from scan.fetchers.cli.cli_fetch_host_details import CliFetchHostDetails
from scan.fetchers.cli.cli_fetch_interface_details \
    import CliFetchInterfaceDetails
from scan.fetchers.kube.kube_access import KubeAccess
from scan.scan_error import ScanError


class KubeFetchNodes(KubeAccess, CliFetchHostDetails):

    def __init__(self, config=None):
        super().__init__(config)
        self.details_fetcher = None

    def setup(self, env, origin: Origin = None):
        self.details_fetcher = CliFetchInterfaceDetails()
        super().setup(env, origin)

    def set_env(self, env):
        super().set_env(env)
        self.details_fetcher.set_env(env)

    def get(self, object_id):
        nodes = self.api.list_node()
        ret = []
        for node in nodes.items:
            try:
                ret.append(self.get_node_details(node))
            except SshError as e:
                ret.append(e)

        self.update_resource_version(
            method='list_node',
            resource_version=nodes.metadata.resource_version
        )

        return ret

    def get_node_details(self, node: V1Node):
        doc = {'type': 'host'}
        try:
            self.get_node_metadata(doc, node.metadata)
            doc['host'] = doc.get('name', '')
        except AttributeError:
            pass
        try:
            self.get_node_data_from_spec(doc, node.spec)
            self.get_node_data_from_status(doc, node.status)
        except AttributeError:
            pass
        doc['interfaces'] = self.get_host_interfaces(doc)
        self.fetch_host_os_details(doc)
        return doc

    @staticmethod
    def get_node_metadata(doc: dict, metadata: V1ObjectMeta):
        attrs = ['uid', 'name', 'cluster_name', 'annotations', 'labels']
        for attr in attrs:
            try:
                doc[attr] = getattr(metadata, attr)
            except AttributeError:
                pass
        doc['id'] = doc['name']
        doc['host_type'] = ['Network', 'Compute']

    @staticmethod
    def get_node_data_from_spec(doc: dict, spec: V1NodeSpec):
        if 'node-role.kubernetes.io/master' in doc['labels']:
            doc['host_type'].append('Kube-master')
        attrs = ['pod_cidr', 'provider_id', 'taints', 'unschedulable']
        for attr in attrs:
            try:
                doc[attr] = getattr(spec, attr)
            except AttributeError:
                pass

    @staticmethod
    def class_to_dict(data_object, exclude: list=None) -> dict:
        ret = dict()
        if exclude is None:
            exclude = []
        exclude.extend(['attribute_map', 'swagger_types'])
        attrs = [attr for attr in dir(data_object)
                 if not attr.startswith('_')
                 and attr not in exclude]
        for attr in attrs:
            try:
                v = getattr(data_object, attr)
                if not callable(v):
                    ret[attr] = v
            except AttributeError:
                pass
        return ret

    @staticmethod
    def get_node_data_from_status(doc: dict, status: V1NodeStatus):
        doc.update(KubeFetchNodes.class_to_dict(status,
                                                exclude=['daemon_endpoints']))
        addresses = doc['addresses']
        ip_address = next(addr.address for addr in addresses
                          if addr.type == 'InternalIP')
        doc['ip_address'] = ip_address
        node_info = KubeFetchNodes.class_to_dict(doc['node_info'])
        doc['node_info'] = node_info

    def get_interface_data(self, interface_name, interface_lines, host_id):
        ethtool_cmd = 'ethtool {}'.format(interface_name)
        ethtool_lines = self.run_fetch_lines(ethtool_cmd, host_id)
        return self.details_fetcher.get_interface_details(host_id=host_id,
                                                          interface_name=interface_name,
                                                          ip_lines=interface_lines,
                                                          ethtool_lines=ethtool_lines)

    def get_host_interfaces(self, host: dict) -> dict:
        cmd = 'ip address show'
        id_re = r'^[0-9]+:\s([^@:]+)'
        lines = self.run_fetch_lines(cmd, host['id'])
        if not lines:
            raise ScanError('No output returned by command: {}'.format(cmd))
        interface_lines = []
        interface_name = None
        interfaces = []
        for line in lines:
            # look for interfaces sections in the output of 'ip address show'
            matches = re.match(id_re, line)
            if not matches:
                # add more lines to an already discovered interface
                interface_lines.append(line)
                continue
            if interface_lines and interface_name != 'lo':
                # handle previous section
                interface = self.get_interface_data(interface_name, interface_lines, host['id'])
                interfaces.append(interface)
            interface_lines = []
            interface_name = matches.group(1)
            interface_lines.append(line)
        # add last interface
        interface = self.get_interface_data(interface_name, interface_lines, host['id'])
        interfaces.append(interface)
        return interfaces
