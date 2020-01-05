###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.utils.util import encode_router_id
from listen.events.event_base import EventResult
from listen.events.event_delete_base import EventDeleteBase


class EventRouterDelete(EventDeleteBase):

    def handle(self, env, values):
        payload = values['payload']

        if 'publisher_id' not in values:
            self.log.error("Publisher_id is not in event values. Aborting router delete")
            return EventResult(result=False, retry=False)

        if 'router_id' in payload:
            router_id = payload['router_id']
        elif 'id' in payload:
            router_id = payload['id']
        else:
            router_id = payload.get('router', {}).get('id')

        if not router_id:
            self.log.error("Router id is not in payload. Aborting router delete")
            return EventResult(result=False, retry=False)

        router_full_id = encode_router_id(router_id)
        return self.delete_handler(env, router_full_id, "vservice")
