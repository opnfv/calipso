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

from listen.events.event_base import EventBase, EventResult
from listen.events.event_instance_add import EventInstanceAdd
from listen.events.event_instance_delete import EventInstanceDelete


class EventInstanceUpdate(EventBase):

    def handle(self, env, values):
        # find the host, to serve as parent
        payload = values['payload']
        instance_id = payload['instance_id']
        state = payload['state']
        old_state = payload['old_state']

        if state == 'building':
            return EventResult(result=False, retry=False)

        if state == 'active' and old_state == 'building':
            return EventInstanceAdd().handle(env, values)

        if state == 'deleted' and old_state == 'active':
            return EventInstanceDelete().handle(env, values)

        name = payload['display_name']
        instance = self.inv.get_by_id(env, instance_id)
        if not instance:
            self.log.info('instance document not found, aborting instance update')
            return EventResult(result=False, retry=True)

        instance['name'] = name
        instance['object_name'] = name
        name_path = instance['name_path']
        instance['name_path'] = name_path[:name_path.rindex('/') + 1] + name

        # TBD: fix name_path for descendants
        if name_path != instance['name_path']:
            self.inv.values_replace({
                "environment": env,
                "name_path": {"$regex": r"^" + re.escape(name_path + '/')}},
                {"name_path": {"from": name_path, "to": instance['name_path']}})
        self.inv.set(instance)
        return EventResult(result=True,
                           related_object=instance_id,
                           display_context=instance_id)
