###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
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

    @staticmethod
    def get(file_name):
        # config file is taken from app/config by default
        # look in the current work directory to get the
        # config path
        python_path = os.environ['PYTHONPATH']
        if os.pathsep in python_path:
            python_path = python_path.split(os.pathsep)[0]
        return python_path + '/config/' + file_name
