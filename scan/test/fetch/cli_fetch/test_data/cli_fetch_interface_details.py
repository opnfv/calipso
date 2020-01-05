###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
HOST_ID = "node-6.cisco.com"

INTERFACE_NAMES = ["ens32", "eno33554952"]

INTERFACE_NAME = INTERFACE_NAMES[0]
IFCONFIG_CM_RESULT = [
    "2: ens32: <BROADCAST,MULTICAST,UP,LOWER_UP> "
    "mtu 1500 qdisc pfifo_fast state UP qlen 1000",
    "    link/ether 00:50:56:99:2a:07 brd ff:ff:ff:ff:ff:ff",
    "    inet 10.56.20.211/24 brd 10.56.20.255 scope global ens32",
    "       valid_lft forever preferred_lft forever",
    "    inet6 2001:420:4482:24c1:250:56ff:fe99:2a07/64 "
    "scope global noprefixroute dynamic",
    "       valid_lft 2591969sec preferred_lft 604769sec",
    "    inet6 fe80::250:56ff:fe99:2a07/64 scope link",
    "       valid_lft forever preferred_lft forever"
]

INTERFACE_DETAILS = {
    "host": "node-6.cisco.com",
    "id": "ens32-unknown_mac",
    "index": "2",
    "lines": [],
    "local_name": "ens32",
    "name": "ens32",
    "state": "UP"
}

MAC_ADDRESS_LINE = "    link/ether 00:50:56:ac:e8:97 brd ff:ff:ff:ff:ff:ff"
MAC_ADDRESS = "00:50:56:ac:e8:97"
RAW_INTERFACE = {
    "host": "node-6.cisco.com",
    "lines": [],
    "local_name": "eno16777728",
    "name": "eno16777728"
}

INTERFACE_AFTER_LINE_HANDLE = {
    "host": "node-6.cisco.com",
    "lines": [MAC_ADDRESS_LINE.strip()],
    "local_name": "eno16777728",
    "name": "eno16777728",
    "id": "eno16777728-" + MAC_ADDRESS,
    "mac_address": MAC_ADDRESS
}

INTERFACE_FOR_SET = {
    "host": "node-6.cisco.com",
    "lines": [
        "Link encap:Ethernet  HWaddr 00:50:56:ac:e8:97",
        "UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1"
    ],
    "local_name": "eno16777728",
    "mac_address": "00:50:56:ac:e8:97"
}

INTERFACE_AFTER_SET = {
    "host": "node-6.cisco.com",
    "data": "Link encap:Ethernet  HWaddr 00:50:56:ac:e8:97" +
            "\nUP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1",
    "local_name": "eno16777728",
    "mac_address": "00:50:56:ac:e8:97",
    "Supported ports": "[ TP ]",
    "Supported link modes": ["10baseT/Half 10baseT/Full",
                             "100baseT/Half 100baseT/Full",
                             "1000baseT/Full"],
    "Supported pause frame use": "No"
}

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
        "data": "Link encap:Ethernet  HWaddr 00:50:56:ac:e8:97\n"
                "UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1\n"
                "RX packets:408989052 errors:0 dropped:0 overruns:0 frame:0\n"
                "TX packets:293849880 errors:0 dropped:0 overruns:0 carrier:0\n"
                "collisions:0 txqueuelen:1000\n"
                "RX bytes:103702814216 (103.7 GB)  "
                "TX bytes:165063440009 (165.0 GB)\n",
        "host": "node-6.cisco.com",
        "id": "eno16777728-00:50:56:ac:e8:97",
        "local_name": "eno16777728",
        "mac_address": "00:50:56:ac:e8:97",
        "name": "eno16777728"
}

INTERFACES_GET_RESULTS = [INTERFACE]

IPV6_ADDRESS_LINE = "    inet6 fe80::f816:3eff:fea1:eb73/64 " \
                    "scope global mngtmpaddr dynamic"
IPV6_ADDRESS = "fe80::f816:3eff:fea1:eb73/64"
IPV4_ADDRESS_LINE = "    inet 172.16.13.2/24 brd 10.56.20.255 scope global eth0"
IPV4_ADDRESS = "172.16.13.2"

ETHTOOL_RESULT = [
    "Settings for eno16777728:",
    "\tSupported ports: [ TP ]",
    "\tSupported link modes:   10baseT/Half 10baseT/Full ",
    "\t                        100baseT/Half 100baseT/Full ",
    "\t                        1000baseT/Full ",
    "\tSupported pause frame use: No",
]
