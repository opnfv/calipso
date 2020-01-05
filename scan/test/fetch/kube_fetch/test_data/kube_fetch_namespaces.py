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

EMPTY_RESPONSE = deepcopy(BASE_RESPONSE)
EMPTY_RESPONSE['kind'] = "NamespaceList"
EMPTY_RESPONSE['metadata']['selfLink'] = "/api/v1/namespaces"

NAMESPACES_RESPONSE = deepcopy(EMPTY_RESPONSE)
NAMESPACES_RESPONSE['items'] = [
    {
        "metadata": {
            "name": "default",
            "selfLink": "/api/v1/namespaces/default",
            "uid": "b5fee42e-1b31-11e8-9d88-00505699cf9e",
            "resourceVersion": "6",
            "creationTimestamp": "2018-02-26T20:14:55Z"
        },
        "status": {
            "phase": "Active"
        }
    },
    {
        "metadata": {
            "name": "kube-public",
            "selfLink": "/api/v1/namespaces/kube-public",
            "uid": "b863c683-1b31-11e8-9d88-00505699cf9e",
            "resourceVersion": "59",
            "creationTimestamp": "2018-02-26T20:14:59Z"
        },
        "status": {
            "phase": "Active"
        }
    },
    {
        "metadata": {
            "name": "kube-system",
            "selfLink": "/api/v1/namespaces/kube-system",
            "uid": "b6816509-1b31-11e8-9d88-00505699cf9e",
            "resourceVersion": "12",
            "creationTimestamp": "2018-02-26T20:14:56Z"
        },
        "status": {
            "phase": "Active"
        }
    }
]

EXPECTED_NAMESPACES = [
    {
        'id': ns['metadata']['uid'],
        'self_link': ns['metadata']['selfLink']
    } for ns in NAMESPACES_RESPONSE['items']
]
