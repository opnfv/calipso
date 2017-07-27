CONFIGURATIONS = { 
    "app_path": "/home/scan/calipso_prod/app/",
    "scanners_file": "/home/yarony/osdna_dev/app/discover/scanners.json",
    "configuration": [
        {
            "mock": "True",
            "host": "10.56.20.239",
            "name": "mysql",
            "password": "102QreDdiD5sKcvNf9qbHrmr",
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
            "key": "/Users/ngrandhi/.ssh/id_rsa",
            "name": "CLI",
            "pwd": "",
            "user": "root"
        },
        {
            "name": "AMQP",
            "host": "10.56.20.239",
            "port": "5673",
            "user": "nova",
            "password": "NF2nSv3SisooxPkCTr8fbfOa"
        },
        {
            "config_folder": "/tmp/sensu_config",
            "provision": "Deploy",
            "env_type": "development",
            "name": "Monitoring",
            "rabbitmq_port": "5672",
            "rabbitmq_pass": "osdna",
            "rabbitmq_user": "sensu",
            "ssh_port": "20022",
            "ssh_user": "scan",
            "ssh_password": "scan",
            "server_ip": "korlev-osdna-staging1.cisco.com",
            "server_name": "osdna-sensu",
            "type": "Sensu"
        }
    ],
    "distribution": "Mirantis-8.0",
    "last_scanned:": "5/8/16",
    "name": "Mirantis-Liberty-Nvn",
    "mechanism_drivers": [
        "OVS"
    ],
    "operational": "yes",
    "type": "environment"
}
