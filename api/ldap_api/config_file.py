###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import os


class ConfigFile:

    def __init__(self, file_path):
        super().__init__()

        if not os.path.isfile(file_path):
            raise ValueError("config file doesn't exist in "
                             "the system: {0}"
                             .format(file_path))
        self.config_file = file_path

    def read_config(self):
        params = {}
        try:
            with open(self.config_file) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") or " " not in line:
                        continue
                    index = line.index(" ")
                    key = line[: index].strip()
                    value = line[index + 1:].strip()
                    if value:
                        params[key] = value
        except Exception as e:
            raise e
        return params
