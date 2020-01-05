###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

import kubernetes.client as kube_client

from base.utils.api_access_base import ApiAccessBase
from base.utils.inventory_mgr import InventoryMgr
from base.utils.kube_utils import update_resource_version
from base.utils.origins import Origin


class KubeAccess(ApiAccessBase):

    def __init__(self, config=None):
        # Reset api client to support multiple configurations
        kube_client.configuration.api_client = None

        super().__init__('Kubernetes', config)

        self.inv = InventoryMgr()
        self.base_url = None
        self.bearer_token = None
        self.api = None
        self.set_kube_config()

    def set_kube_config(self):
        self.base_url = 'https://{}:{}'.format(self.host, self.port)
        self.bearer_token = self.api_config.get('token', '')
        conf = kube_client.Configuration()
        conf.host = self.base_url
        conf.user = self.api_config.get('user')
        conf.api_key_prefix['authorization'] = 'Bearer'
        conf.api_key['authorization'] = self.bearer_token
        conf.verify_ssl = False
        self.api = kube_client.CoreV1Api(kube_client.ApiClient(conf))

    def setup(self, env, origin: Origin = None):
        super().setup(env, origin)
        self.set_kube_config()

    @staticmethod
    def del_attribute_map(o):
        if isinstance(o, list):
            for item in o:
                KubeAccess.del_attribute_map(item)
            return
        elif isinstance(o, dict):
            for attr in ['attribute_map', 'swagger_types']:
                if attr in o:
                    o.pop(attr)
        else:
            for attr in ['attribute_map', 'swagger_types']:
                if hasattr(o, attr):
                    delattr(o, attr)

    def update_resource_version(self, method: str,
                                resource_version):
        update_resource_version(inv=self.inv,
                                env=self.env,
                                method=method,
                                resource_version=resource_version)