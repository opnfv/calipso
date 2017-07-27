###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.events.event_base import EventBase, EventResult


class EventPortUpdate(EventBase):

    def handle(self, env, notification):
        # check port document.
        port = notification['payload']['port']
        port_id = port['id']
        port_document = self.inv.get_by_id(env, port_id)
        if not port_document:
            self.log.info('port document does not exist, aborting port update')
            return EventResult(result=False, retry=True)

        # build port document
        port_document['name'] = port['name']
        port_document['admin_state_up'] = port['admin_state_up']
        if port_document['admin_state_up']:
            port_document['status'] = 'ACTIVE'
        else:
            port_document['status'] = 'DOWN'

        port_document['binding:vnic_type'] = port['binding:vnic_type']

        # update port document.
        self.inv.set(port_document)
        return EventResult(result=True,
                           related_object=port_id,
                           display_context=port_document.get('network_id'))
