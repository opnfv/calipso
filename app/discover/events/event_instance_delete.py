###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.events.event_delete_base import EventDeleteBase


class EventInstanceDelete(EventDeleteBase):

    def handle(self, env, values):
        # find the corresponding object
        instance_id = values['payload']['instance_id']
        return self.delete_handler(env, instance_id, "instance")
