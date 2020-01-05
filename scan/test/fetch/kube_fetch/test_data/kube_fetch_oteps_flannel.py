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

from scan.test.fetch.kube_fetch.test_data.kube_access import HOST_DOC

HOST_DOC = deepcopy(HOST_DOC)
HOST_DOC['annotations'] = {
    "node.alpha.kubernetes.io/ttl": "0",
    "flannel.alpha.coreos.com/backend-data": "{\"VtepMAC\":\"be:9b:77:4d:31:9c\"}",
    "flannel.alpha.coreos.com/backend-type": "vxlan",
    "volumes.kubernetes.io/controller-managed-attach-detach": "true",
    "flannel.alpha.coreos.com/public-ip": "172.16.100.2",
    "flannel.alpha.coreos.com/kube-subnet-manager": "true"
}

OTEPS_PARENT = '{}-vedge'.format(HOST_DOC['id'])

OTEPS_LIST = [
    {
        "_id": "5aafe3a189f6e7759a516b63",
        "environment": "kube-aci",
        "id": "kub1-aci-otep",
        "type": "otep",
        "name": "kub1-aci-otep",
        "overlay_type": "vxlan",
        "parent_type": "vedge",
        "ip_address": "172.16.100.1",
        "name_path": "/kube-aci/Hosts/kub1-aci/vEdges/kube-flannel-ds-642n5/kub1-aci-otep",
        "host": "kub1-aci",
        "ports": {
            "vxlan-remote-kub2-aci": {
                "remote_host": "kub2-aci",
                "options": {
                    "remote_ip": "172.16.100.2",
                    "local_ip": "172.16.100.1"
                },
                "interface": "vxlan-remote-kub2-aci",
                "name": "vxlan-remote-kub2-aci",
                "type": "vxlan"
            },
            "vxlan-remote-kub3-aci": {
                "remote_host": "kub3-aci",
                "options": {
                    "remote_ip": "172.16.100.3",
                    "local_ip": "172.16.100.1"
                },
                "interface": "vxlan-remote-kub3-aci",
                "name": "vxlan-remote-kub3-aci",
                "type": "vxlan"
            }
        },
        "id_path": "/kube-aci/kube-aci-hosts/kub1-aci/kub1-aci-vedges/kub1-aci-vedge/kub1-aci-otep",
        "object_name": "kub1-aci-otep",
        "parent_id": "kub1-aci-vedge"
    },
    {
        "_id": "5aafe3a389f6e7759a516bef",
        "environment": "kube-aci",
        "id": "kub3-aci-otep",
        "type": "otep",
        "name": "kub3-aci-otep",
        "overlay_type": "vxlan",
        "parent_type": "vedge",
        "ip_address": "172.16.100.3",
        "name_path": "/kube-aci/Hosts/kub3-aci/vEdges/kube-flannel-ds-vhkbl/kub3-aci-otep",
        "host": "kub3-aci",
        "ports": {
            "vxlan-remote-kub2-aci": {
                "remote_host": "kub2-aci",
                "options": {
                    "remote_ip": "172.16.100.2",
                    "local_ip": "172.16.100.3"
                },
                "interface": "vxlan-remote-kub2-aci",
                "name": "vxlan-remote-kub2-aci",
                "type": "vxlan"
            },
            "vxlan-remote-kub1-aci": {
                "remote_host": "kub1-aci",
                "options": {
                    "remote_ip": "172.16.100.1",
                    "local_ip": "172.16.100.3"
                },
                "interface": "vxlan-remote-kub1-aci",
                "name": "vxlan-remote-kub1-aci",
                "type": "vxlan"
            }
        },
        "id_path": "/kube-aci/kube-aci-hosts/kub3-aci/kub3-aci-vedges/kub3-aci-vedge/kub3-aci-otep",
        "object_name": "kub3-aci-otep",
        "parent_id": "kub3-aci-vedge"
    }
]

EXPECTED_OTEP = {
    'id': '{}-otep'.format(HOST_DOC['id']),
    'name': '{}-otep'.format(HOST_DOC['name']),
    'host': HOST_DOC['id'],
    'parent_id': OTEPS_PARENT,
    'parent_type': 'vedge'
}