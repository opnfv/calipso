###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
CONFIGURATIONS = {
    "configuration": [
        {
            "mock": "True",
            "host": "10.56.20.239",
            "name": "mysql",
            "pwd": "102QreDdiD5sKcvNf9qbHrmr",
            "port": 3307.0,
            "user": "root",
            "schema": "nova"
        },
        {
            "name": "OpenStack",
            "host": "10.56.20.239",
            "admin_token": "38MUh19YWcgQQUlk2VEFQ7Ec",
            "port": "5000",
            "user": "admin",
            "pwd": "admin"
        },
        {
            "host": "10.56.20.239",
            "key": "/Users/xiaocdon/.ssh/id_rsa",
            "name": "CLI",
            "pwd": "",
            "user": "root"
        },
        {
            "name": "AMQP",
            "host": "10.56.20.239",
            "port": "5673",
            "user": "nova",
            "pwd": "NF2nSv3SisooxPkCTr8fbfOa"
        }
    ],
    "distribution": "Mirantis",
    "distribution_version": "8.0",
    "last_scanned:": "5/8/16",
    "name": "Mirantis-Liberty-Xiaocong",
    "network_plugins": [
        "OVS"
    ],
    "operational": "yes",
    "type": "environment"
}
