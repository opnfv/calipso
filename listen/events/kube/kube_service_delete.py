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


class KubeServiceDelete(KubeEventDeleteBase):

    def handle(self, env, values):
        super().handle(env, values)
        return self.delete_handler(env=env,
                                   object_id=self.object_id,
                                   object_type="vservice")