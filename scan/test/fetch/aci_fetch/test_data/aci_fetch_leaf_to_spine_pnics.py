###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
HOSTLINK_PNIC = {
    "_id": "5a9d7399c6ad1791937ab017",
    "environment": "kube-aci",
    "id": "switch-pod-1__node-103-leaf-eth1__33-00:50:56:99:5d:70",
    "type": "switch_pnic",
    "object_name": "eth1/33",
    "role": "hostlink",
    "parent_id": "switch-pod-1__node-103-leaf",
    "parent_type": "switch",
    "mac_address": "00:50:56:99:5d:70",
    "switch": "switch-pod-1__node-103-leaf",
    "aci_document": {
        "addr": "00:50:56:99:5D:70",
        "dn": "topology/pod-1/node-103/sys/ctx-[vxlan-2883584]/bd-[vxlan-15925207]/vlan-[vlan-111]/initial_data-ep/mac-00:50:56:99:5D:70",
        "ifId": "eth1/33",
    },
    "fvCEp": [
        {
            "dn": "uni/tn-Koren-k8s/ap-Koren-k8s/epg-Koren-k8s/cep-00:50:56:99:5D:70",
            "id": "0",
            "ip": "0.0.0.0",
            "mac": "00:50:56:99:5D:70",
            "monPolDn": "uni/tn-common/monepg-default",
            "name": "00:50:56:99:5D:70",
            "fvRsCEpToPathEp": [
                {
                    "lcOwn": "local",
                    "modTs": "2018-03-02T16:42:48.770+02:00",
                    "rn": "rscEpToPathEp-[topology/pod-1/paths-103/pathep-[eth1/33]]",
                    "tDn": "topology/pod-1/paths-103/pathep-[eth1/33]",
                }
            ]
        }
    ],
    "show_in_tree": True,
    "name": "switch-pod-1__node-103-leaf-eth1__33-00:50:56:99:5d:70",
    "id_path": "/kube-aci/kube-aci-switches/switch-pod-1__node-103-leaf/switch-pod-1__node-103-leaf-eth1__33-00:50:56:99:5d:70",
    "name_path": "/kube-aci/Switches/switch-pod-1__node-103-leaf/switch-pod-1__node-103-leaf-eth1__33-00:50:56:99:5d:70",
}

SPINES_RESPONSE = {
    "totalCount": "2",
    "imdata": [
        {
            "fabricNode": {
                "attributes": {
                    "dn": "topology/pod-1/node-201",
                    "id": "201",
                    "name": "Spine-201",
                    "role": "spine",
                    "serial": "SAL1825V6D0",
                }
            }
        },
        {
            "fabricNode": {
                "attributes": {
                    "dn": "topology/pod-1/node-202",
                    "id": "202",
                    "name": "Spine-202",
                    "role": "spine",
                    "serial": "SAL184642FA",
                }
            }
        }
    ]
}

ADJACENT_SPINES_RESPONSE = {
    "totalCount": "1",
    "imdata": [
        {
            "lldpAdjEp": {
                "attributes": {
                    "capability": "bridge,router",
                    "chassisIdT": "mac",
                    "chassisIdV": "50:87:89:d4:89:12",
                    "dn": "topology/pod-1/node-103/sys/lldp/inst/if-[eth1/49]/adj-1",
                    "id": "1",
                    "mgmtPortMac": "50:87:89:D4:89:12",
                    "portDesc": "topology/pod-1/paths-201/pathep-[eth1/3]",
                    "portIdV": "Eth1/3",
                    "sysDesc": "topology/pod-1/node-201",
                    "sysName": "Spine-201"
                }
            }
        }
    ]
}