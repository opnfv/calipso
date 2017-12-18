###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from kubernetes.client import Configuration as KubConf, CoreV1Api

from utils.api_access_base import ApiAccessBase


class KubeAccess(ApiAccessBase):

    def __init__(self, config=None):
        super().__init__('Kubernetes', config)
        self.base_url = 'https://{}:{}'.format(self.host, self.port)
        self.bearer_token = self.api_config.get('token', '')
        conf = KubConf()
        conf.host = self.base_url
        conf.user = self.api_config.get('user')
        conf.api_key_prefix['authorization'] = 'Bearer'
        conf.api_key['authorization'] = self.bearer_token
        conf.verify_ssl = False
        self.api = CoreV1Api()

