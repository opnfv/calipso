###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.utils.exceptions import ResourceGoneError
from listen.events.event_base import EventResult
from listen.events.kube.kube_event_base import KubeEventBase


class KubeErrorHandler(KubeEventBase):

    GONE_CODE = 410

    def handle(self, env, values):
        super().handle(env, values)
        if values['raw_object'].get('code') == self.GONE_CODE:
            raise ResourceGoneError()
        return EventResult(result=True)
