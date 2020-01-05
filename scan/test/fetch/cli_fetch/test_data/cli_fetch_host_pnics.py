###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
PNICS_FOLDER_ID = "node-6.cisco.com-pnics"
HOST_ID = "node-6.cisco.com"

NETWORK_NODE = {
    "host_type": [
        "Controller",
        "Network"
    ],
    "id": "node-6.cisco.com"
}

WRONG_NODE = {
    "host_type": [
            "Controller"
        ]
}

INTERFACE_LINES = [
    "lrwxrwxrwx 1 root 0 Jul  5 17:17 eno16777728 -> ../../devices/0000:02:00.0/net/eno16777728",
    "lrwxrwxrwx 1 root 0 Jul  5 17:17 eno33554952 -> ../../devices/0000:02:01.0/net/eno33554952"
]

INTERFACE_NAMES = ["eno16777728", "eno33554952"]

INTERFACE = {
        "Advertised auto-negotiation": "Yes",
        "Advertised link modes": [
            "10baseT/Half 10baseT/Full",
            "100baseT/Half 100baseT/Full",
            "1000baseT/Full"
        ],
        "Advertised pause frame use": "No",
        "Auto-negotiation": "on",
        "Current message level": [
            "0x00000007 (7)",
            "drv probe link"
        ],
        "Duplex": "Full",
        "Link detected": "yes",
        "MDI-X": "off (auto)",
        "PHYAD": "0",
        "Port": "Twisted Pair",
        "Speed": "1000Mb/s",
        "Supported link modes": [
            "10baseT/Half 10baseT/Full",
            "100baseT/Half 100baseT/Full",
            "1000baseT/Full"
        ],
        "Supported pause frame use": "No",
        "Supported ports": "[ TP ]",
        "Supports Wake-on": "d",
        "Supports auto-negotiation": "Yes",
        "Transceiver": "internal",
        "Wake-on": "d",
        "data": "Link encap:Ethernet  HWaddr 00:50:56:ac:e8:97\nUP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1\nRX packets:408989052 errors:0 dropped:0 overruns:0 frame:0\nTX packets:293849880 errors:0 dropped:0 overruns:0 carrier:0\ncollisions:0 txqueuelen:1000\nRX bytes:103702814216 (103.7 GB)  TX bytes:165063440009 (165.0 GB)\n",
        "host": "node-6.cisco.com",
        "id": "eno16777728-00:50:56:ac:e8:97",
        "local_name": "eno16777728",
        "mac_address": "00:50:56:ac:e8:97",
        "name": "eno16777728"
}

INTERFACES_GET_RESULTS = [INTERFACE]
