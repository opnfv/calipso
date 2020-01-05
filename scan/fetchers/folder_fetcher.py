#!/usr/bin/env python3
###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.fetcher import Fetcher
from base.utils.string_utils import jsonify


class FolderFetcher(Fetcher):
    def __init__(self, types_name, parent_type, text="", create_folder=True):
        super(FolderFetcher, self).__init__()
        self.types_name = types_name
        self.parent_type = parent_type
        self.text = text
        self.create_folder = create_folder
        if not self.text:
            self.text = self.types_name.capitalize()

    def get(self, id):
        oid = id + "-" + self.types_name
        root_obj = {
            "id": oid,
            "create_object": self.create_folder,
            "name": oid,
            "text": self.text,
            "type": self.types_name + "_folder",
            "parent_id": id,
            "parent_type": self.parent_type
        }
        return jsonify([root_obj])
