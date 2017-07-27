###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re

from discover.events.event_base import EventBase, EventResult


class EventNetworkUpdate(EventBase):

    def handle(self, env, notification):
        network = notification['payload']['network']
        network_id = network['id']

        network_document = self.inv.get_by_id(env, network_id)
        if not network_document:
            self.log.info('Network document not found, aborting network update')
            return EventResult(result=False, retry=True)

        # update network document
        name = network['name']
        if name != network_document['name']:
            network_document['name'] = name
            network_document['object_name'] = name

            name_path = network_document['name_path']
            network_document['name_path'] = name_path[:name_path.rindex('/') + 1] + name

            # TBD: fix name_path for descendants
            self.inv.values_replace({"environment": env,
                                     "name_path": {"$regex": r"^" + re.escape(name_path + '/')}},
                                    {"name_path": {"from": name_path, "to": network_document['name_path']}})

        network_document['admin_state_up'] = network['admin_state_up']
        self.inv.set(network_document)
        return EventResult(result=True,
                           related_object=network_id,
                           display_context=network_id)
