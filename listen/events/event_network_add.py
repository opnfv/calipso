###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from listen.events.event_base import EventBase, EventResult


class EventNetworkAdd(EventBase):

    def handle(self, env, notification):
        network = notification['payload']['network']
        network_id = network['id']
        network_document = self.inv.get_by_id(env, network_id)
        if network_document:
            self.log.info('network already existed, aborting network add')
            return EventResult(result=False, retry=False)

        # build network document for adding network
        project_name = notification['_context_project_name']
        project_id = notification['_context_project_id']
        parent_id = project_id + '-networks'
        network_name = network['name']

        network['environment'] = env
        network['type'] = 'network'
        network['id_path'] = "/%s/%s-projects/%s/%s/%s" \
                             % (env, env, project_id, parent_id, network_id)
        network['cidrs'] = []
        network['subnet_ids'] = []
        network['last_scanned'] = notification['timestamp']
        network['name_path'] = "/%s/Projects/%s/Networks/%s" \
                               % (env, project_name, network_name)
        network['network'] = network_id
        network['object_name'] = network_name
        network['parent_id'] = parent_id
        network['parent_text'] = "Networks"
        network['parent_type'] = "networks_folder"
        network['project'] = project_name
        network["show_in_tree"] = True
        network['subnets'] = {}

        self.inv.set(network)
        return EventResult(result=True,
                           related_object=network_id,
                           display_context=network_id)
