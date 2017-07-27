###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
VEDGE_FOLDER_ID = "ubuntu0-vedges"

HOST = {
    "host_type": [
        "Controller",
        "Compute",
        "Network"
    ],
    "id": "ubuntu0",
}

HOST_WITHOUT_REQUIRED_HOST_TYPE = {
    "host_type": [

    ]
}

VERSION = [
    "vpp v16.09-rc0~157-g203c632 built by localadmin on ubuntu0 at Sun Jun 26 16:35:15 PDT 2016\n"
]

INTERFACES = [
    "              Name               Idx       State          Counter          Count     ",
    "TenGigabitEthernetc/0/0           5         up       rx packets                502022",
    "                                                     rx bytes               663436206",
    "                                                     tx packets                 81404",
    "                                                     tx bytes                 6366378",
    "                                                     drops                       1414",
    "                                                     punts                          1",
    "                                                     rx-miss                    64525",
    "VirtualEthernet0/0/0              7         up       tx packets                 31496",
    "                                                     tx bytes                 2743185",
    "local0                            0        down      ",
    "pg/stream-0                       1        down      ",
]

PORTS = {
    "TenGigabitEthernetc/0/0": {
        "id": "5",
        "name": "TenGigabitEthernetc/0/0",
        "state": "up"
    },
    "VirtualEthernet0/0/0": {
        "id": "7",
        "name": "VirtualEthernet0/0/0",
        "state": "up"
    },
    "local0": {
        "id": "0",
        "name": "local0",
        "state": "down"
    },
    "pg/stream-0": {
        "id": "1",
        "name": "pg/stream-0",
        "state": "down"
    }
}


VEDGE_RESULTS = [
    {
        "host": "ubuntu0",
        "id": "ubuntu0-VPP",
        "name": "VPP-ubuntu0",
        "agent_type": "VPP",
        "binary": "vpp v16.09-rc0~157-g203c632",
        "ports": PORTS
    }
]

VEDGE_RESULTS_WITHOUT_BINARY = [
    {
        "host": "ubuntu0",
        "id": "ubuntu0-VPP",
        "name": "VPP-ubuntu0",
        "agent_type": "VPP",
        "ports": PORTS
    }
]
