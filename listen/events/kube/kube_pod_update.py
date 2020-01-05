###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from listen.events.event_base import EventResult
from listen.events.kube.kube_event_base import KubeEventBase


class KubePodUpdate(KubeEventBase):

    def handle(self, env, values):
        super().handle(env, values)

        pod = self.inv.get_by_id(environment=env, item_id=self.object_id)
        if not pod:
            return EventResult(result=False,
                               retry=True,  # TODO: doesn't work atm
                               related_object=self.object_id,
                               display_context=self.object_id,
                               message='Pod doesn\'t exist')

        self.save_pod_doc()
        return EventResult(result=True,
                           related_object=self.object_id,
                           display_context=self.object_id)