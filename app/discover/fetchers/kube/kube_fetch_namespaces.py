###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.kube.kube_access import KubeAccess


class KubeFetchNamespaces(KubeAccess):

    def __init__(self, config=None):
        super().__init__(config)

    def get(self, object_id):
        namespaces = self.api.list_namespace()
        return [self.get_namespace(i) for i in namespaces.items]

    @staticmethod
    def get_namespace(namespace):
        attrs = ['creation_timestamp', 'self_link', 'uid']
        namespace_details = {
            'name': namespace.metadata.name,
            'status': namespace.status.phase
        }
        namespace_details.update({x: getattr(namespace.metadata, x, '')
                                  for x in attrs})
        namespace_details['id'] = namespace_details['uid']
        return namespace_details
