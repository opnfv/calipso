###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from copy import deepcopy

from scan.test.fetch.kube_fetch.test_data.kube_access import BASE_RESPONSE

VSERVICES_FOLDER_DOC = {
    "_id": "5aaf8369c6ad1791934c9a15",
    "environment": "kube-aci",
    "id": "b5fee42e-1b31-11e8-9d88-00505699cf9e-vservices",
    "type": "vservices_folder",
    "parent_type": "namespace",
    "name": "Vservices",
    "id_path": "/kube-aci/kube-aci-namespaces/b5fee42e-1b31-11e8-9d88-00505699cf9e/b5fee42e-1b31-11e8-9d88-00505699cf9e-vservices",
    "name_path": "/kube-aci/Namespaces/default/Vservices",
    "object_name": "Vservices",
    "parent_id": "b5fee42e-1b31-11e8-9d88-00505699cf9e"
}

NAMESPACE_DOC = {
    "_id": "5aaf8369c6ad1791934c9a03",
    "environment": "kube-aci",
    "id": "b5fee42e-1b31-11e8-9d88-00505699cf9e",
    "type": "namespace",
    "parent_type": "namespaces_folder",
    "uid": "b5fee42e-1b31-11e8-9d88-00505699cf9e",
    "name": "default",
    "id_path": "/kube-aci/kube-aci-namespaces/b5fee42e-1b31-11e8-9d88-00505699cf9e",
    "object_name": "default",
    "self_link": "/api/v1/namespaces/default",
    "name_path": "/kube-aci/Namespaces/default",
    "parent_id": "kube-aci-namespaces"
}

VSERVICE_PODS = [
    [
        {'id': 'pod1', 'name': 'pod1'},
        {'id': 'pod2', 'name': 'pod2'}
    ],
    []
]

EMPTY_RESPONSE = deepcopy(BASE_RESPONSE)
EMPTY_RESPONSE['kind'] = "ServiceList"
EMPTY_RESPONSE['metadata']['selfLink'] = "/api/v1/namespaces/{}/services".format(NAMESPACE_DOC['name'])

VSERVICES_RESPONSE = deepcopy(EMPTY_RESPONSE)
VSERVICES_RESPONSE['items'] = [
    {
        "metadata": {
            "name": "cisco-portal-service",
            "namespace": "default",
            "selfLink": "/api/v1/namespaces/default/services/cisco-portal-service",
            "uid": "16600875-1b34-11e8-9d88-00505699cf9e",
        },
        "spec": {
            "ports": [
                {
                    "protocol": "TCP",
                    "port": 8008,
                    "targetPort": 22,
                    "nodePort": 30679
                }
            ],
            "selector": {
                "app": "cisco-web"
            },
            "clusterIP": "10.98.44.236",
            "type": "NodePort",
            "sessionAffinity": "None",
            "externalTrafficPolicy": "Cluster"
        }
    },
    {
        "metadata": {
            "name": "kubernetes",
            "namespace": "default",
            "selfLink": "/api/v1/namespaces/default/services/kubernetes",
            "uid": "b861f17e-1b31-11e8-9d88-00505699cf9e",
            "labels": {
                "component": "apiserver",
                "provider": "kubernetes"
            }
        },
        "spec": {
            "ports": [
                {
                    "name": "https",
                    "protocol": "TCP",
                    "port": 443,
                    "targetPort": 6443
                }
            ],
            "clusterIP": "10.96.0.1",
            "type": "ClusterIP",
            "sessionAffinity": "ClientIP",
            "sessionAffinityConfig": {
                "clientIP": {
                    "timeoutSeconds": 10800
                }
            }
        }
    }
]

EXPECTED_VSERVICES = [
    {
        'id': vs['metadata']['uid'],
        'type': 'vservice',
        'name': vs['metadata']['name'],
        'namespace': vs['metadata']['namespace'],
        'pods': VSERVICE_PODS[i],
    } for i, vs in enumerate(VSERVICES_RESPONSE['items'])
]
