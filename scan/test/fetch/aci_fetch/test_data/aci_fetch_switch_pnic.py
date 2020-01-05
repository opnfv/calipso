###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
HOST_PNIC = {
    "_id": "5a9d738fc6ad1791937aaec8",
    "environment": "kube-aci",
    "id": "ens192-00:50:56:99:5d:70",
    "type": "host_pnic",
    "host": "kub1-aci",
    "name": "ens192",
    "local_name": "ens192",
    "mac_address": "00:50:56:99:5d:70",
    "IP Address": "172.16.100.1",
    "state": "DOWN",
    "show_in_tree": True,
    "parent_id": "kub1-aci-host_pnics",
    "parent_type": "pnics_folder",
    "id_path": "/kube-aci/kube-aci-hosts/kub1-aci/kub1-aci-host_pnics/ens192-00:50:56:99:5d:70",
    "name_path": "/kube-aci/Hosts/kub1-aci/pNICs/ens192",
    "object_name": "ens192"
}

SWITCH_PNIC_RESPONSE = {
    "totalCount": "1",
    "imdata": [
        {
            "epmMacEp": {
                "attributes": {
                    "addr": "00:50:56:99:5D:70",
                    "childAction": "",
                    "createTs": "2018-03-02T16:42:24.776+02:00",
                    "dn": "topology/pod-1/node-103/sys/ctx-[vxlan-2883584]/bd-[vxlan-15925207]/vlan-[vlan-111]/initial_data-ep/mac-00:50:56:99:5D:70",
                    "flags": "local,mac",
                    "ifId": "eth1/33",
                    "modTs": "never",
                    "name": "",
                    "pcTag": "49155",
                    "status": ""
                }
            }
        }
    ]
}

SWITCH_RESPONSE = {
    "totalCount": "1",
    "imdata": [
        {
            "topSystem": {
                "attributes": {
                    "address": "10.0.16.91",
                    "dn": "topology/pod-1/node-103/sys",
                    "id": "103",
                    "name": "Leaf-103",
                    "role": "leaf",
                    "serial": "SAL1924GTQS",
                }
            }
        }
    ]
}

FVCEP_RESPONSE = {
    "totalCount": "1",
    "imdata": [
        {
            "fvCEp": {
                "attributes": {
                    "dn": "uni/tn-Koren-k8s/ap-Koren-k8s/epg-Koren-k8s/cep-00:50:56:99:5D:70",
                    "id": "0",
                    "ip": "0.0.0.0",
                    "mac": "00:50:56:99:5D:70",
                    "name": "00:50:56:99:5D:70",
                    "uid": "0",
                },
                "children": [
                    {
                        "fvRsCEpToPathEp": {
                            "attributes": {
                                "rn": "rscEpToPathEp-[topology/pod-1/paths-103/pathep-[eth1/33]]",
                                "tDn": "topology/pod-1/paths-103/pathep-[eth1/33]",
                                "tType": "mo"
                            }
                        }
                    }
                ]
            }
        }
    ]
}

L1PHYSIF_RESPONSE = {
    "totalCount": "1",
    "imdata": [
        {
            "l1PhysIf": {
                "attributes": {
                    "adminSt": "up",
                    "dn": "topology/pod-1/node-103/sys/phys-[eth1/33]",
                    "id": "eth1/33",
                    "layer": "Layer2",
                    "medium": "broadcast",
                    "modTs": "2018-03-19T17:27:32.981+03:00",
                    "mode": "trunk",
                    "portT": "leaf",
                    "routerMac": "not-applicable",
                    "spanMode": "not-a-span-dest",
                    "speed": "1G",
                    "status": "",
                    "switchingSt": "enabled",
                    "trunkLog": "default",
                    "usage": "epg"
                }
            }
        }
    ]
}