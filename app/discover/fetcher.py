###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.configuration import Configuration
from utils.origins import Origin
from utils.logging.full_logger import FullLogger


class Fetcher:

    ENV_TYPE_KUBERNETES = 'Kubernetes'
    ENV_TYPE_OPENSTACK = 'OpenStack'

    def __init__(self):
        super().__init__()
        self.env = None
        self.log = FullLogger()
        self.configuration = None
        self.origin = None

    @staticmethod
    def escape(string):
        return string

    def set_env(self, env):
        self.env = env
        self.log.setup(env=env)
        self.configuration = Configuration()

    def setup(self, env, origin: Origin = None):
        self.set_env(env=env)
        if origin:
            self.origin = origin
            self.log.setup(origin=origin)

    def get_env(self):
        return self.env

    def get(self, object_id):
        return None

    def set_folder_parent(self,
                          o: dict,
                          object_type: str =None,
                          master_parent_type: str =None,
                          master_parent_id: str =None,
                          parent_objects_name=None,
                          parent_type: str =None,
                          parent_id: str =None,
                          parent_text: str =None):
        if object_type:
            o['type'] = object_type
            if not parent_objects_name:
                parent_objects_name = '{}s'.format(object_type)
        if not master_parent_type:
            self.log.error('set_folder_parent: must specify: '
                           'master_parent_type, master_parent_id, '
                           'parent_type', 'parent_id')
            return
        if not parent_objects_name and not parent_type:
            self.log.error('set_folder_parent: must specify: '
                           'either parent_objects_name (e.g. "vedges") '
                           'or parent_type and parent_id')
            return
        if parent_objects_name and not parent_type:
            parent_type = '{}_folder'.format(parent_objects_name)
        if parent_objects_name and not parent_id:
            parent_id = '{}-{}'.format(master_parent_id, parent_objects_name)
        o.update({
            'master_parent_type': master_parent_type,
            'master_parent_id': master_parent_id,
            'parent_type': parent_type,
            'parent_id': parent_id
        })
        if parent_text:
            o['parent_text'] = parent_text
        elif parent_objects_name:
            o['parent_text'] = parent_objects_name.capitalize()
