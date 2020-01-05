###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
# handle monitoring event for pNIC objects

from bson import ObjectId

from base.fetcher import Fetcher
from base.utils.special_char_converter import SpecialCharConverter
from monitoring.handlers.monitoring_check_handler import MonitoringCheckHandler


class HandleHostPnic(MonitoringCheckHandler):

    def __init__(self, args):
        super().__init__(args)
        self.env_config = self.conf.get_env_config()
        self.env = self.env_config.get('name', '')
        self.is_kubernetes = self.env_config .get('environment_type', '') == \
            Fetcher.ENV_TYPE_KUBERNETES
        self.check_result = None

    def handle(self, obj_id, check_result):
        self.check_result = check_result
        object_id = self.get_pnic_object_id(obj_id)
        doc = self.doc_by_id(object_id)
        if not doc:
            return 1
        self.keep_result(doc, check_result)
        self.propagate_error_state(doc)
        return check_result['status']

    @staticmethod
    def get_pnic_object_id(obj_id: str) -> str:
        object_id = obj_id[:obj_id.index('-')]
        mac = obj_id[obj_id.index('-')+1:]
        converter = SpecialCharConverter()
        mac_address = converter.decode_special_characters(mac)
        object_id += '-' + mac_address
        return object_id

    # for Kubernetes environment only:
    # - when a host pNic change status (from monitoring module) to 'Error':
    #   - all dependent objects should change status to 'Warning'
    #   - set status_text for these object to the status_text from the pnic
    # - when pnic status changes back from error: TBD
    #
    # dependent objects are all objects that are part of a clique that has
    # a link that includes that pNic as either source or target.
    def propagate_error_state(self, pnic: dict):
        if not self.is_kubernetes:
            return
        # find cliques where the pNIC appears in the list of nodes
        related_cliques = self.inv.find_items({'environment': self.env,
                                               'nodes': ObjectId(pnic['_id'])},
                                              projection=['nodes'],
                                              collection='cliques')
        dependents = []
        for clique in related_cliques:
            dependents.extend(clique['nodes'])
        if not dependents:
            return

        is_error = self.check_result['status'] != 0
        fields_to_set = {}
        self.keep_result(fields_to_set, self.check_result, add_message=False)
        action = self.set_action_on_db_object(is_error, fields_to_set, pnic)
        self.inv.inventory_collection.update(
            {
                'environment': self.env,
                '_id': {'$in': dependents},
                # do not change state for other pNIC objects
                'type': {'$ne': pnic['type']},
                'host': pnic['host']
            },
            action,
            multi=True,
        )
        for dependent in dependents:
            self.propagate_container_state(dependent, pnic['host'], action)

    def set_action_on_db_object(self, is_error, fields_to_set, pnic) -> dict:
        status = 1
        fields_to_set['status_value'] = status
        fields_to_set['status'] = self.get_label_for_status(status)
        fields_to_set['root_cause'] = dict(id=pnic['id'], name=pnic['name'],
                                           type=pnic['type'],
                                           host=pnic['host'],
                                           status=pnic['status'],
                                           status_text=pnic['status_text'])
        if is_error:
            # set status fields
            action = {'$set': fields_to_set}
        else:
            fields_to_remove = {k: '' for k in fields_to_set.keys()}
            # clear status fields from dependents
            action = {'$unset': fields_to_remove}
        return action

    def propagate_container_state(self, db_id, host, action):
        item = self.inv.find_one({
            'environment': self.env,
            '_id': db_id,
            'host': host

        })
        if not item or item.get('type') != 'container':
            return
        # find related pod-container links
        related_pod_container_links = self.inv.find_items({
            'environment': self.env,
            'link_type': 'pod-container',
            'target_id': item['id']
        }, collection='links')
        for link in related_pod_container_links:
            self.mark_pod_state(pod_id=link['source_id'], action=action)

    def mark_pod_state(self, pod_id: str=None, action: dict=None):
        pod = self.inv.get_by_id(self.env, pod_id)
        if not pod:
            self.log.error('failed to find pod with id {}'.format(pod_id))
            return
        self.inv.inventory_collection.update({'environment': self.env,
                                              'id': pod['id']},
                                             action)
        self.propagate_state_from_pod_to_service(pod_id, action)

    def propagate_state_from_pod_to_service(self, pod_id: str=None,
                                            action: dict=None):
        # find related vservice-pod links
        related_vservice_pod_links = self.inv.find_items({
            'environment': self.env,
            'link_type': 'vservice-pod',
            'target_id': pod_id
        }, collection='links')
        for link in related_vservice_pod_links:
            self.inv.inventory_collection.update({'_id': link['source']},
                                                 action)
            vservice = self.inv.get_by_id(self.env, link['source_id'])
            if vservice:
                self.keep_message(vservice, self.check_result)
            else:
                self.log.error('failed to find service with ID {}'
                               .format(link['source_id']))
