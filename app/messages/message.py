###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import datetime
from typing import Union

from bson import ObjectId


class Message:

    LEVELS = ['info', 'warn', 'error']
    DEFAULT_LEVEL = LEVELS[0]

    def __init__(self,
                 msg_id: str,
                 msg: dict,
                 source: str,
                 env: str = None,
                 object_id: Union[str, ObjectId] = None,
                 display_context: Union[str, ObjectId] = None,
                 level: str = DEFAULT_LEVEL,
                 object_type: str = None,
                 ts: datetime = None,
                 received_ts: datetime = None,
                 finished_ts: datetime = None,
                 **kwargs):
        super().__init__()

        if level and level.lower() in self.LEVELS:
            self.level = level.lower()
        else:
            self.level = self.DEFAULT_LEVEL

        self.id = msg_id
        self.environment = env
        self.source_system = source
        self.related_object = object_id
        self.related_object_type = object_type
        self.display_context = display_context
        self.message = msg
        self.timestamp = ts if ts else received_ts
        self.received_timestamp = received_ts
        self.finished_timestamp = finished_ts
        self.viewed = False
        self.extra = kwargs

    def get(self):
        return {
            "id": self.id,
            "environment": self.environment,
            "source_system": self.source_system,
            "related_object": self.related_object,
            "related_object_type": self.related_object_type,
            "display_context": self.display_context,
            "level": self.level,
            "message": self.message,
            "timestamp": self.timestamp,
            "received_timestamp": self.received_timestamp,
            "finished_timestamp": self.finished_timestamp,
            "viewed": self.viewed,
            **self.extra
        }
