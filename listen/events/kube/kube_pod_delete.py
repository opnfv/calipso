###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from listen.events.kube.kube_event_delete_base import KubeEventDeleteBase
from scan.fetchers.kube.kube_fetch_pods import KubeFetchPods


class KubePodDelete(KubeEventDeleteBase):

    def handle(self, env, values):
        super().handle(env, values)
        self.delete_pod_references(object_id=self.object_id)
        return self.delete_handler(env=env,
                                   object_id=self.object_id,
                                   object_type="pod")

    def _get_pod_proxy_service(self, pod: dict) -> dict:
        labels = pod.get('labels', {})
        app_field = 'k8s-app'
        app_name = labels.get(app_field, '')
        if not app_name:
            app_name = labels.get('app')
            app_field = 'app'
        if not app_name:
            return {}
        cond = {
            'environment': pod['environment'],
            'type': 'vservice',
            'selector.{}'.format(app_field): app_name
        }
        service = self.inv.find_one(cond)
        if not service:
            return {}

    def delete_pod_references(self, object_id=None):
        pod = self.inv.get_by_id(self.env, object_id)
        if not pod:
            self.log.error('unable to find pod with ID {}'.format(object_id))
            return
        self.delete_pod_reference_from_namespace(pod)

    def delete_pod_reference_from_vservice(self, pod):
        service = self._get_pod_proxy_service(pod)
        if not service:
            self.log.error('unable to find service for pod {} (ID: {}'
                           .format(pod['object_name'], pod['id']))
            return
        pods = list(filter(lambda p: p['id'] != pod['id'],
                           service.get('pods', [])))
        self.inv.inventory_collection.update({'_id': service['_id']},
                                             {'$set': {'pods': pods}})

    def delete_pod_reference_from_namespace(self, pod):
        namespace = KubeFetchPods.get_pod_namespace(self.inv, pod)
        if not namespace:
            self.log.error('unable to find namespace {} '
                           'for pod {} (ID: {})'
                           .format(pod['namespace'], pod['object_name'],
                                   pod['id']))
            return
        pods = list(filter(lambda p: p['id'] != pod['id'],
                           namespace.get('pods', [])))
        self.inv.inventory_collection.update({'_id': namespace['_id']},
                                             {'$set': {'pods': pods}})
