###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from kubernetes.client.models import V1Pod, V1ObjectMeta, V1PodSpec, V1PodStatus

from base.utils.inventory_mgr import InventoryMgr
from scan.fetchers.cli.cli_fetcher import CliFetcher
from scan.fetchers.kube.kube_access import KubeAccess


class KubeFetchPods(KubeAccess, CliFetcher):

    def __init__(self, config=None):
        super().__init__(config)
        self.k8s_host = None

    def get(self, host_id) -> list:
        self.k8s_host = self.inv.get_by_id(self.get_env(), host_id)
        if not self.k8s_host:
            self.log.error('failed to find node with id={}'.format(host_id))
            return []

        host_name = self.k8s_host['name']
        pod_filter = 'spec.nodeName={}'.format(host_name)
        pods = self.api.list_pod_for_all_namespaces(field_selector=pod_filter)

        self.update_resource_version(
            method='list_pod_for_all_namespaces',
            resource_version=pods.metadata.resource_version
        )

        results = [self.get_pod_document(pod) for pod in pods.items]
        if 'cattle-system' in (p['namespace'] for p in results):
            results.append(self.get_rancher_proxy())
        return results

    # TODO: temporary
    def get_rancher_proxy(self):
        pod_id = '{}-kube-proxy-pod'.format(self.k8s_host['name'])
        doc = {
            'id': pod_id,
            'name': pod_id,
            'environment': self.env,
            'host': self.k8s_host['name'],
            'namespace': 'cattle-system',
            'labels': {
                'calipso-rancher-pod-for-kube-proxy': True
            },
            'containers': [
                {'name': 'kube-proxy'}
            ]
        }
        self.set_folder_parent(doc, object_type='pod',
                                    master_parent_type='host',
                                    master_parent_id=self.k8s_host['id'])
        doc['type'] = 'pod'
        self.add_pod_ref_to_namespace(doc)
        return doc

    def get_pod_document(self, pod: V1Pod):
        doc = self.get_pod_details(pod)
        if self.k8s_host:
            self.set_folder_parent(doc, object_type='pod',
                                   master_parent_type='host',
                                   master_parent_id=self.k8s_host['id'])
            doc['host'] = self.k8s_host['name']
        doc['type'] = 'pod'
        doc['environment'] = self.env
        self.add_pod_ref_to_namespace(doc)
        return doc

    @classmethod
    def get_pod_details(cls, pod: V1Pod):
        doc = {}
        try:
            cls.get_pod_metadata(doc, pod.metadata)
        except AttributeError:
            pass
        try:
            cls.get_pod_data(doc, pod.spec)
        except AttributeError:
            pass
        try:
            cls.get_pod_status(doc, pod.status)
        except AttributeError:
            pass
        return doc

    @staticmethod
    def get_pod_metadata(doc: dict, metadata: V1ObjectMeta):
        attrs = ['uid', 'name', 'cluster_name', 'annotations', 'labels',
                 'owner_references', 'namespace']
        for attr in attrs:
            try:
                val = getattr(metadata, attr)
                if val is not None:
                    doc[attr] = val
            except AttributeError:
                pass
        doc['id'] = doc['uid']

    ATTRIBUTES_TO_FETCH = [
        'containers',
        'node_name',
        'scheduler_name',
        'dns_policy',
        'termination_grace_period_seconds',
        'tolerations',
        'volumes'
    ]

    @staticmethod
    def get_pod_data(doc: dict, spec: V1PodSpec):
        for attr in KubeFetchPods.ATTRIBUTES_TO_FETCH:
            try:
                val = getattr(spec, attr)
                KubeAccess.del_attribute_map(val)
                doc[attr] = val
            except AttributeError:
                pass

    @staticmethod
    def get_pod_status(doc: dict, pod_status: V1PodStatus):
        status_data = {}
        for k in dir(pod_status):
            if k.startswith('_'):
                continue
            if k not in [
                    'conditions',
                    'container_statuses',
                    'host_ip',
                    'init_container_statuses',
                    'message', 'phase',
                    'pod_ip', 'qos_class', 'reason', 'start_time']:
                continue
            try:
                val = getattr(pod_status, k)
                if val is None:
                    continue
                status_data[k] = val
            except AttributeError:
                pass
        if status_data:
            doc['pod_status'] = status_data

    @staticmethod
    def get_pod_namespace(inv_mgr: InventoryMgr, pod: dict) -> dict:
        namespace = inv_mgr.find_one({
            'environment': pod['environment'],
            'name': pod['namespace']
        })
        if not namespace:
            return {}
        return namespace

    def add_pod_ref_to_namespace(self, pod):
        namespace = self.get_pod_namespace(self.inv, pod)
        if not namespace:
            self.log.error('unable to find namespace {} for pod {}'
                           .format(pod['namespace'], pod['name']))
            return
        if 'pods' not in namespace:
            namespace['pods'] = []
        namespace['pods'].append(dict(id=pod['id'], name=pod['name'],
                                      host=pod['host']))
        self.inv.set(namespace)
