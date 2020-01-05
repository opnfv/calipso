###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import datetime
import logging

from base.messages.message import Message
from base.utils.inventory_mgr import InventoryMgr
from base.utils.logging.logger import Logger
from base.utils.origins import Origin


class MongoLoggingHandler(logging.Handler):
    """
    Logging handler for MongoDB
    """
    SOURCE_SYSTEM = 'Calipso'

    def __init__(self, env: str, level: str, origin: Origin = None):
        super().__init__(Logger.get_numeric_level(level))
        self.str_level = level
        self.env = env
        self.inv = None
        self.origin = origin

    def emit(self, record):
        # Try to invoke InventoryMgr for logging
        if not self.inv:
            try:
                self.inv = InventoryMgr()
            except:
                return

        # make sure we do not try to log to DB when DB is not ready
        if not (self.inv.is_db_ready()
                and 'messages' in self.inv.collections):
            return

        # make ID from current timestamp
        now = datetime.datetime.utcnow()
        d = now - datetime.datetime(1970, 1, 1)
        timestamp_id = '{}.{}.{}'.format(d.days, d.seconds, d.microseconds)
        source = self.SOURCE_SYSTEM

        message = Message(msg_id=timestamp_id, env=self.env, source=source,
                          msg=Logger.formatter.format(record), ts=now,
                          level=record.levelname)
        if self.origin:
            message.extra['origin_id'] = (
                str(self.origin.origin_id)
                if self.origin.origin_id
                else None
            )
            message.extra['origin_type'] = (
                self.origin.origin_type.value
                if self.origin.origin_type
                else None
            )
            for extra_field in self.origin.extra:
                message.extra[extra_field] = getattr(self.origin, extra_field)

        self.inv.collections['messages'].insert_one(message.get())