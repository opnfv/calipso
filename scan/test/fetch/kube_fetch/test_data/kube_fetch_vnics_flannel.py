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

_INTERFACE_ID = "vethd8ade2d8"
HOST_DOC = deepcopy(HOST_DOC)
HOST_DOC['interfaces'] = {
    _INTERFACE_ID: {
        "lines": [
            "7: {}@if3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master cni0 state UP mode DEFAULT group default ",
            "    link/ether 66:3d:dc:96:6d:a1 brd ff:ff:ff:ff:ff:ff link-netnsid 0".format(_INTERFACE_ID)
        ],
        "id": _INTERFACE_ID,
        "mac_address": "66:3d:dc:96:6d:a1",
        "index": "7",
        "state": "UP",
        "mtu": "1450"
    },
    "docker0": {
        "lines": [
            "4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default ",
            "    link/ether 02:42:c9:9c:d7:5d brd ff:ff:ff:ff:ff:ff"
        ],
        "id": "docker0",
        "mac_address": "02:42:c9:9c:d7:5d",
        "index": "4",
        "state": "DOWN",
        "mtu": "1500"
    },
}

_INTERFACE = HOST_DOC['interfaces'][_INTERFACE_ID]
EXPECTED_VNIC = {
    'id': '{}-{}'.format(HOST_DOC['id'], _INTERFACE_ID),
    'type': 'vnic',
    'host': HOST_DOC['id'],
    'mac_address':  _INTERFACE['mac_address'],
    'parent_id': '{}-vnics'.format(HOST_DOC['id']),
    'parent_type': 'vnics_folder'
}