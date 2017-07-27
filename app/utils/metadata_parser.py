###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json
import os
from abc import abstractmethod, ABCMeta

from utils.util import get_extension


class MetadataParser(metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self.errors = []

    @abstractmethod
    def get_required_fields(self) -> list:
        pass

    def validate_metadata(self, metadata: dict) -> bool:
        if not isinstance(metadata, dict):
            raise ValueError('metadata needs to be a valid dict')

        # make sure metadata json contains all fields we need
        required_fields = self.get_required_fields()
        if not all([field in metadata for field in required_fields]):
            raise ValueError("Metadata json should contain "
                             "all the following fields: {}"
                             .format(', '.join(required_fields)))
        return True

    @staticmethod
    def _load_json_file(file_path: str):
        with open(file_path) as data_file:
            return json.load(data_file)

    def _parse_json_file(self, file_path: str):
        metadata = self._load_json_file(file_path)

        # validate metadata correctness
        if not self.validate_metadata(metadata):
            return None

        return metadata

    @staticmethod
    def check_metadata_file_ok(file_path: str):
        extension = get_extension(file_path)
        if extension != 'json':
            raise ValueError("Extension '{}' is not supported. "
                             "Please provide a .json metadata file."
                             .format(extension))

        if not os.path.isfile(file_path):
            raise ValueError("Couldn't load metadata file. "
                             "Path '{}' doesn't exist or is not a file"
                             .format(file_path))

    def parse_metadata_file(self, file_path: str) -> dict:
        # reset errors in case same parser is used to read multiple inputs
        self.errors = []
        self.check_metadata_file_ok(file_path)

        # Try to parse metadata file if it has one of the supported extensions
        metadata = self._parse_json_file(file_path)
        self.check_errors()
        return metadata

    def check_errors(self):
        if self.errors:
            raise ValueError("Errors encountered during "
                             "metadata file parsing:\n{}"
                             .format("\n".join(self.errors)))

    def add_error(self, msg):
        self.errors.append(msg)
