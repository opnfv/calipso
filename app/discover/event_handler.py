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
from utils.inventory_mgr import InventoryMgr
from utils.logging.full_logger import FullLogger
from utils.util import ClassResolver


class EventHandler:

    def __init__(self, env: str, inventory_collection: str):
        super().__init__()
        self.inv = InventoryMgr()
        self.inv.set_collections(inventory_collection)
        self.env = env
        self.log = FullLogger(env=env)
        self.handlers = {}

    def discover_handlers(self, handlers_package: str, event_handlers: dict):
        if not event_handlers:
            raise TypeError("Event handlers list is empty")

        for event_name, handler_name in event_handlers.items():
            handler = ClassResolver.get_instance_of_class(handler_name, handlers_package)
            if not issubclass(handler.__class__, EventBase):
                raise TypeError("Event handler '{}' is not a subclass of EventBase"
                                .format(handler_name))
            if event_name in self.handlers:
                self.log.warning("A handler is already registered for event type '{}'. Overwriting"
                                 .format(event_name))
            self.handlers[event_name] = handler

    def handle(self, event_name: str, notification: dict) -> EventResult:
        if event_name not in self.handlers:
            self.log.info("No handler is able to process event of type '{}'"
                          .format(event_name))
        return self.handlers[event_name].handle(self.env, notification)

