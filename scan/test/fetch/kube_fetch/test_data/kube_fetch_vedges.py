###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from scan.test.fetch.kube_fetch.test_data.kube_access import HOST_DOC

PODS_LIST = [{
    "_id": "5aafe39f89f6e7759a516a5f",
    "environment": "kube-aci",
    "id": "66745de5-1b33-11e8-9d88-00505699cf9e",
    "type": "pod",
    "parent_type": "pods_folder",
    "labels": {
        "controller-revision-hash": "1818740607",
        "app": "flannel",
        "pod-template-generation": "1",
        "tier": "node"
    },
    "name_path": "/kube-aci/Hosts/kub2-aci/Pods/kube-flannel-ds-4bn8q",
    "id_path": "/kube-aci/kube-aci-hosts/kub2-aci/kub2-aci-pods/66745de5-1b33-11e8-9d88-00505699cf9e",
    "node_name": "kub2-aci",
    "namespace": "kube-system",
    "uid": "66745de5-1b33-11e8-9d88-00505699cf9e",
    "name": "kube-flannel-ds-4bn8q",
    "parent_text": "Pods",
    "host": "kub2-aci",
    "object_name": "kube-flannel-ds-4bn8q",
    "parent_id": "kub2-aci-pods"
}]

_POD = PODS_LIST[0]
EXPECTED_VEDGE = {
    'id': '{}-vedge'.format(HOST_DOC['id']),
    'host': HOST_DOC['id'],
    'environment': HOST_DOC['environment'],
    'name': _POD['name'],
    'namespace': _POD['namespace'],
    'node_name': HOST_DOC['id'],
    'parent_id': '{}-vedges'.format(HOST_DOC['id']),
    'parent_type': 'vedges_folder'
}