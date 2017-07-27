###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from typing import List, Tuple

from utils.metadata_parser import MetadataParser


class EventMetadataParser(MetadataParser):

    HANDLERS_PACKAGE = 'handlers_package'
    QUEUES = 'queues'
    EVENT_HANDLERS = 'event_handlers'

    REQUIRED_EXPORTS = [HANDLERS_PACKAGE, EVENT_HANDLERS]

    def __init__(self):
        super().__init__()
        self.handlers_package = None
        self.queues = []
        self.event_handlers = []

    def get_required_fields(self) -> list:
        return self.REQUIRED_EXPORTS

    def validate_metadata(self, metadata: dict) -> bool:
        super().validate_metadata(metadata)

        package = metadata.get(self.HANDLERS_PACKAGE)
        if not package or not isinstance(package, str):
            self.add_error("Handlers package '{}' is invalid".format(package))

        event_handlers = metadata.get(self.EVENT_HANDLERS)
        if not event_handlers or not isinstance(event_handlers, dict):
            self.add_error("Event handlers attribute is invalid or empty"
                           "(should be a non-empty dict)")

        return len(self.errors) == 0

    def _finalize_parsing(self, metadata):
        handlers_package = metadata[self.HANDLERS_PACKAGE]
        queues = metadata.get(self.QUEUES, None)
        event_handlers = metadata[self.EVENT_HANDLERS]

        # Convert variables to EventHandler-friendly format
        self.handlers_package = handlers_package

        try:
            if queues and isinstance(queues, list):
                self.queues = [{"queue": q["queue"],
                                "exchange": q["exchange"]}
                               for q in queues]
        except KeyError:
            self.add_error("Queues variable has invalid format")
            return

        self.event_handlers = event_handlers

    def parse_metadata_file(self, file_path: str) -> dict:
        metadata = super().parse_metadata_file(file_path)
        self._finalize_parsing(metadata)
        super().check_errors()
        return metadata


def parse_metadata_file(file_path: str):
    parser = EventMetadataParser()
    parser.parse_metadata_file(file_path)
    return parser.handlers_package, parser.queues, parser.event_handlers
