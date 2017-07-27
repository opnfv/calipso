###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from test.api.responders_test.test_data import base


URL = "/environment_configs"

NAME = "Mirantis-Liberty-API"
UNKNOWN_NAME = "UNKNOWN NAME"
WRONG_DISTRIBUTION = base.WRONG_DISTRIBUTION
CORRECT_DISTRIBUTION = base.CORRECT_DISTRIBUTION
WRONG_MECHANISM_DRIVER = base.WRONG_MECHANISM_DRIVER
CORRECT_MECHANISM_DRIVER = base.CORRECT_MECHANISM_DRIVER
WRONG_TYPE_DRIVER = base.WRONG_TYPE_DRIVER
CORRECT_TYPE_DRIVER = base.CORRECT_TYPE_DRIVER
USER = "WS7j8oTbWPf3LbNne"
NON_BOOL_LISTEN = NON_BOOL_SCANNED = \
    NON_BOOL_MONITORING_SETUP_DONE = base.NON_BOOL

BOOL_LISTEN = BOOL_SCANNED = \
    BOOL_MONITORING_SETUP_DONE = base.BOOL

ENV_CONFIGS = [
    {
        "distribution": "Mirantis-8.0",
        "name": "Mirantis-Liberty-API"
    },
    {
        "distribution": "Mirantis-9.0",
        "name": "Mirantis-Liberty"
    }
]

ENV_CONFIGS_RESPONSE = {
    "environment_configs": ENV_CONFIGS
}

ENV_CONFIGS_WITH_SPECIFIC_NAME = [
    {
        "distribution": "Mirantis-8.0",
        "name": NAME
    }
]

ENV_CONFIGS_WITH_SPECIFIC_DISTRIBUTION = [
    {
        "distribution": CORRECT_DISTRIBUTION,
        "name": "Mirantis-Liberty-API",
    },
    {
        "distribution": CORRECT_DISTRIBUTION,
        "name": "Mirantis-Liberty"
    }
]

ENV_CONFIGS_WITH_SPECIFIC_DISTRIBUTION_RESPONSE = {
    "environment_configs": ENV_CONFIGS_WITH_SPECIFIC_DISTRIBUTION
}

ENV_CONFIGS_WITH_SPECIFIC_MECHANISM_DRIVER = [
    {
        "name": "Mirantis-Liberty-API",
        "mechanism_drivers": [
            CORRECT_MECHANISM_DRIVER
        ]
    },
    {
        "name": "Mirantis-Liberty",
        "mechanism_drivers": [
            CORRECT_MECHANISM_DRIVER
        ]
    }
]

ENV_CONFIGS_WITH_SPECIFIC_MECHANISM_DRIVER_RESPONSE = {
    "environment_configs": ENV_CONFIGS_WITH_SPECIFIC_MECHANISM_DRIVER
}

ENV_CONFIGS_WITH_SPECIFIC_TYPE_DRIVER = [
    {
        "type_drivers": CORRECT_TYPE_DRIVER,
        "name": "Mirantis-Liberty-API",
    },
    {
        "type_drivers": CORRECT_TYPE_DRIVER,
        "name": "Mirantis-Liberty"
    }
]

ENV_CONFIGS_WITH_SPECIFIC_TYPE_DRIVER_RESPONSE = {
    'environment_configs': ENV_CONFIGS_WITH_SPECIFIC_TYPE_DRIVER
}

ENV_CONFIGS_WITH_SPECIFIC_USER = [
    {
        "user": USER,
        "name": "Mirantis-Liberty-API",
    },
    {
        "user": USER,
        "name": "Mirantis-Liberty"
    }
]

ENV_CONFIGS_WITH_SPECIFIC_USER_RESPONSE = {
    "environment_configs": ENV_CONFIGS_WITH_SPECIFIC_USER
}

ENV_CONFIGS_WITH_SPECIFIC_LISTEN = [
    {
        "listen": BOOL_LISTEN,
        "name": "Mirantis-Liberty-API",
    },
    {
        "listen": BOOL_LISTEN,
        "name": "Mirantis-Liberty"
    }
]

ENV_CONFIGS_WITH_SPECIFIC_LISTEN_RESPONSE = {
    "environment_configs": ENV_CONFIGS_WITH_SPECIFIC_LISTEN
}

ENV_CONFIGS_WITH_SPECIFIC_SCANNED = [
    {
        "scanned": BOOL_SCANNED,
        "name": "Mirantis-Liberty-API",
    },
    {
        "scanned": BOOL_SCANNED,
        "name": "Mirantis-Liberty"
    }
]

ENV_CONFIGS_WITH_SPECIFIC_SCANNED_RESPONSE = {
    "environment_configs": ENV_CONFIGS_WITH_SPECIFIC_SCANNED
}

ENV_CONFIGS_WITH_SPECIFIC_MONITORING_SETUP_DONE = [
    {
        "monitoring_setup_done": BOOL_MONITORING_SETUP_DONE,
        "name": "Mirantis-Liberty-API",
    },
    {
        "monitoring_setup_done": BOOL_MONITORING_SETUP_DONE,
        "name": "Mirantis-Liberty"
    }
]

ENV_CONFIGS_WITH_SPECIFIC_MONITORING_SETUP_DONE_RESPONSE = {
    "environment_configs": ENV_CONFIGS_WITH_SPECIFIC_MONITORING_SETUP_DONE
}

ENV_CONFIG = {
    "app_path": "/home/korenlev/Calipso/app/",
    "configuration": [
        {
            "host": "10.56.20.239",
            "name": "mysql",
            "password": "G1VKEbcqKZXoPthrtNma2D9Y",
            "port": "3307",
            "user": "root"
        },
        {
            "name": "OpenStack",
            "host": "10.56.20.239",
            "admin_token": "wLWefGuD0uYJ7tqkeEScdnNo",
            "port": "5000",
            "user": "admin",
            "pwd": "admin"
        },
        {
            "host": "10.56.20.239",
            "key": "/etc/calipso/keys/Mirantis-Liberty-id_rsa",
            "name": "CLI",
            "user": "root"
        },
        {
            "host": "10.56.20.239",
            "name": "AMQP",
            "password": "YVWMiKMshZhlJCGqFu5PdT9d",
            "port": "5673",
            "user": "nova"
        },
        {
            "config_folder": "/tmp/sensu_test",
            "provision": "None",
            "env_type": "development",
            "name": "Monitoring",
            "api_port": "4567",
            "rabbitmq_port": "5671",
            "rabbitmq_pass": "sensuaccess",
            "rabbitmq_user": "sensu",
            "ssh_port": "20022",
            "ssh_user": "root",
            "ssh_password": "calipso",
            "server_ip": "korlev-calipso-staging1.cisco.com",
            "server_name": "calipso-sensu",
            "type": "Sensu"
        }
    ],
    "distribution": "Mirantis-8.0",
    "last_scanned": "2017-03-16T11:14:54Z",
    "listen": True,
    "mechanism_drivers": [
        "ovs"
    ],
    "name": "Mirantis-Liberty",
    "operational": "running",
    "scanned": True,
    "type": "environment",
    "type_drivers": "vxlan",
    "user": "WS7j8oTbWPf3LbNne"
}
