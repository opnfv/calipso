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

from scan.test.fetch.kube_fetch.test_data.kube_access import BASE_RESPONSE

EMPTY_RESPONSE = deepcopy(BASE_RESPONSE)
EMPTY_RESPONSE['kind'] = "NodeList"
EMPTY_RESPONSE['metadata']['selfLink'] = "/api/v1/nodes"

NODES_RESPONSE = deepcopy(EMPTY_RESPONSE)
NODES_RESPONSE['items'] = [
    {
        "metadata": {
            "name": "kub1-aci",
            "selfLink": "/api/v1/nodes/kub1-aci",
            "uid": "b5fc42cf-1b31-11e8-9d88-00505699cf9e",
            "resourceVersion": "2022069",
            "creationTimestamp": "2018-02-26T20:14:55Z",
            "labels": {
                "beta.kubernetes.io/arch": "amd64",
                "beta.kubernetes.io/os": "linux",
                "kubernetes.io/hostname": "kub1-aci",
                "node-role.kubernetes.io/master": ""
            },
            "annotations": {
                "flannel.alpha.coreos.com/public-ip": "172.16.100.1",
            }
        },
        "spec": {
            "podCIDR": "10.244.0.0/24",
            "externalID": "kub1-aci"
        },
        "status": {
            "capacity": {
                "cpu": "2",
                "memory": "16432840Ki",
                "pods": "110"
            },
            "allocatable": {
                "cpu": "2",
                "memory": "16330440Ki",
                "pods": "110"
            },
            "addresses": [
                {
                    "type": "InternalIP",
                    "address": "10.56.0.117"
                },
                {
                    "type": "Hostname",
                    "address": "kub1-aci"
                }
            ],
            "daemonEndpoints": {
                "kubeletEndpoint": {
                    "Port": 10250
                }
            },
            "nodeInfo": {
                "machineID": "d1e524fa2d6b92a8a7fd55bc5a9419ab",
                "systemUUID": "4219C414-6073-9C04-43E9-FBEE1498A59A",
                "bootID": "f2f8a217-0282-478b-a0d2-7051c5369f50",
                "kernelVersion": "4.4.0-62-generic",
                "osImage": "Ubuntu 16.04.2 LTS",
                "containerRuntimeVersion": "docker://17.12.0-ce",
                "kubeletVersion": "v1.9.3",
                "kubeProxyVersion": "v1.9.3",
                "operatingSystem": "linux",
                "architecture": "amd64"
            },
        }
    },
    {
        "metadata": {
            "name": "kub2-aci",
            "selfLink": "/api/v1/nodes/kub2-aci",
            "uid": "6671a0b8-1b33-11e8-9d88-00505699cf9e",
            "resourceVersion": "2022063",
            "creationTimestamp": "2018-02-26T20:27:01Z",
            "labels": {
                "beta.kubernetes.io/arch": "amd64",
                "beta.kubernetes.io/os": "linux",
                "kubernetes.io/hostname": "kub2-aci"
            },
            "annotations": {
                "flannel.alpha.coreos.com/public-ip": "172.16.100.2"
            }
        },
        "spec": {
            "podCIDR": "10.244.1.0/24",
            "externalID": "kub2-aci"
        },
        "status": {
            "addresses": [
                {
                    "type": "InternalIP",
                    "address": "10.56.0.116"
                },
                {
                    "type": "Hostname",
                    "address": "kub2-aci"
                }
            ],
            "daemonEndpoints": {
                "kubeletEndpoint": {
                    "Port": 10250
                }
            },
            "nodeInfo": {
                "machineID": "d1e524fa2d6b92a8a7fd55bc5a9419ab",
                "systemUUID": "42198DD0-A393-9695-2207-C56505993966",
                "bootID": "4dc100cd-e646-48ed-9c91-df12025f9e1c",
                "kernelVersion": "4.4.0-62-generic",
                "osImage": "Ubuntu 16.04.2 LTS",
                "containerRuntimeVersion": "docker://17.12.0-ce",
                "kubeletVersion": "v1.9.3",
                "kubeProxyVersion": "v1.9.3",
                "operatingSystem": "linux",
                "architecture": "amd64"
            },
        }
    },
    {
        "metadata": {
            "name": "kub3-aci",
            "selfLink": "/api/v1/nodes/kub3-aci",
            "uid": "67dfe5f4-1b33-11e8-9d88-00505699cf9e",
            "resourceVersion": "2022068",
            "creationTimestamp": "2018-02-26T20:27:03Z",
            "labels": {
                "beta.kubernetes.io/arch": "amd64",
                "beta.kubernetes.io/os": "linux",
                "kubernetes.io/hostname": "kub3-aci"
            },
            "annotations": {
                "flannel.alpha.coreos.com/public-ip": "172.16.100.3"
            }
        },
        "spec": {
            "podCIDR": "10.244.2.0/24",
            "externalID": "kub3-aci"
        },
        "status": {
            "addresses": [
                {
                    "type": "InternalIP",
                    "address": "10.56.0.113"
                },
                {
                    "type": "Hostname",
                    "address": "kub3-aci"
                }
            ],
            "daemonEndpoints": {
                "kubeletEndpoint": {
                    "Port": 10250
                }
            },
            "nodeInfo": {
                "machineID": "d1e524fa2d6b92a8a7fd55bc5a9419ab",
                "systemUUID": "42193E70-A613-5A7B-20B8-7E71EDE2F164",
                "bootID": "dff71c30-e4b4-4336-9a7e-8689f8617f85",
                "kernelVersion": "4.4.0-62-generic",
                "osImage": "Ubuntu 16.04.2 LTS",
                "containerRuntimeVersion": "docker://17.12.0-ce",
                "kubeletVersion": "v1.9.3",
                "kubeProxyVersion": "v1.9.3",
                "operatingSystem": "linux",
                "architecture": "amd64"
            }
        }
    }
]

CLI_LINES = {
    'kub1-aci': ['1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1',
                 '    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00',
                 '2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000',
                 '    link/ether 00:50:56:99:cf:9e brd ff:ff:ff:ff:ff:ff',
                 '3: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000',
                 '    link/ether 00:50:56:99:5d:70 brd ff:ff:ff:ff:ff:ff',
                 '4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default ',
                 '    link/ether 02:42:82:dd:b7:0c brd ff:ff:ff:ff:ff:ff',
                 '5: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN mode DEFAULT group default ',
                 '    link/ether ae:9b:95:99:73:6b brd ff:ff:ff:ff:ff:ff',
                 '6: cni0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP mode DEFAULT group default qlen 1000',
                 '    link/ether 0a:58:0a:f4:00:01 brd ff:ff:ff:ff:ff:ff',
                 '7: veth499167ff@if3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master cni0 state UP mode DEFAULT group default ',
                 '    link/ether e2:59:f7:0f:0e:8a brd ff:ff:ff:ff:ff:ff link-netnsid 0'],
    'kub2-aci': ['1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1',
                 '    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00',
                 '2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000',
                 '    link/ether 00:50:56:99:2e:a7 brd ff:ff:ff:ff:ff:ff',
                 '3: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000',
                 '    link/ether e8:b7:48:7b:8f:ae brd ff:ff:ff:ff:ff:ff',
                 '4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default ',
                 '    link/ether 02:42:c9:9c:d7:5d brd ff:ff:ff:ff:ff:ff',
                 '5: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN mode DEFAULT group default ',
                 '    link/ether be:9b:77:4d:31:9c brd ff:ff:ff:ff:ff:ff',
                 '6: cni0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP mode DEFAULT group default qlen 1000',
                 '    link/ether 0a:58:0a:f4:01:01 brd ff:ff:ff:ff:ff:ff',
                 '7: vethd8ade2d8@if3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master cni0 state UP mode DEFAULT group default ',
                 '    link/ether 66:3d:dc:96:6d:a1 brd ff:ff:ff:ff:ff:ff link-netnsid 0'],
    'kub3-aci': ['1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1',
                 '    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00',
                 '2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000',
                 '    link/ether 00:50:56:99:75:f1 brd ff:ff:ff:ff:ff:ff',
                 '3: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000',
                 '    link/ether e8:b7:48:7b:8f:af brd ff:ff:ff:ff:ff:ff',
                 '4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default ',
                 '    link/ether 02:42:a3:1a:e9:93 brd ff:ff:ff:ff:ff:ff',
                 '5: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN mode DEFAULT group default ',
                 '    link/ether 42:35:21:32:eb:53 brd ff:ff:ff:ff:ff:ff',
                 '6: cni0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP mode DEFAULT group default qlen 1000',
                 '    link/ether 0a:58:0a:f4:02:01 brd ff:ff:ff:ff:ff:ff',
                 '7: vethba9e7701@if3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master cni0 state UP mode DEFAULT group default ',
                 '    link/ether 12:21:ed:da:24:ea brd ff:ff:ff:ff:ff:ff link-netnsid 0',
                 '8: vethbe6bd76f@if3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master cni0 state UP mode DEFAULT group default ',
                 '    link/ether a2:ec:75:ef:91:4f brd ff:ff:ff:ff:ff:ff link-netnsid 1']
}

EXPECTED_NODES = [
    {
        'id': node['metadata']['name'],
        'uid': node['metadata']['uid'],
        'host': node['metadata']['name'],
        'ip_address': node['status']['addresses'][0]['address']
    } for node in NODES_RESPONSE['items']
]
