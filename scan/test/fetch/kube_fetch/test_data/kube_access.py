###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
KUBE_CONFIG = {
    "name": "Kubernetes",
    "user": "admin",
    "host": "10.0.0.1",
    "token": "token",
    "port": "6443"
}

BASE_RESPONSE = {
    "kind": None,  # Fill in fetcher test classes
    "apiVersion": "v1",
    "metadata": {
        "selfLink": None,  # Fill in fetcher test classes
        "resourceVersion": "2017411"
    },
    "items": []
}

HOST_DOC = {
    "_id": "5aae890147d0b83dd2989dd7",
    "environment": "kube-aci",
    "id": "kub2-aci",
    "name": "kub2-aci",
    "name_path": "/kube-aci/Hosts/kub2-aci",
    "host": "kub2-aci",
    "uid": "6671a0b8-1b33-11e8-9d88-00505699cf9e",
    "parent_type": "hosts_folder",
    "parent_id": "kube-aci-hosts",
    "object_name": "kub2-aci",
    "id_path": "/kube-aci/kube-aci-hosts/kub2-aci"
}