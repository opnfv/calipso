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

from scan.test.fetch.kube_fetch.test_data.kube_fetch_pods import PODS_RESPONSE

POD_DOCUMENT = {
    "_id": "5aafe39f89f6e7759a516a58",
    "environment": "kube-aci",
    "id": "01df21c6-1b34-11e8-9d88-00505699cf9e",
    "type": "pod",
    "show_in_tree": True,
    "last_scanned": "2018-03-19T16:21:57.743+0000",
    "scheduler_name": "default-scheduler",
    "parent_type": "pods_folder",
    "name_path": "/kube-aci/Hosts/kub2-aci/Pods/cisco-portal-deployment-ha-74f6b66557-wjpg2",
    "dns_policy": "ClusterFirst",
    "id_path": "/kube-aci/kube-aci-hosts/kub2-aci/kub2-aci-pods/01df21c6-1b34-11e8-9d88-00505699cf9e",
    "node_name": "kub2-aci",
    "namespace": "default",
    "uid": "01df21c6-1b34-11e8-9d88-00505699cf9e",
    "pod_status": {
        "pod_ip": "10.244.1.3",
        "host_ip": "10.56.0.116",
        "container_statuses": [
            {
                "state": {
                    "running": {
                        "swagger_types": {
                            "started_at": "datetime"
                        },
                        "started_at": "2018-03-18T15:07:47.000+0000",
                        "attribute_map": {
                            "started_at": "startedAt"
                        }
                    },
                    "attribute_map": {
                        "running": "running",
                        "terminated": "terminated",
                        "waiting": "waiting"
                    },
                    "terminated": None,
                    "waiting": None,
                    "swagger_types": {
                        "running": "V1ContainerStateRunning",
                        "terminated": "V1ContainerStateTerminated",
                        "waiting": "V1ContainerStateWaiting"
                    }
                },
                "attribute_map": {
                    "state": "state",
                    "restart_count": "restartCount",
                    "name": "name",
                    "last_state": "lastState",
                    "container_id": "containerID",
                    "image": "image",
                    "ready": "ready",
                    "image_id": "imageID"
                },
                "restart_count": 1,
                "name": "cisco-web-portal",
                "last_state": {
                    "running": None,
                    "attribute_map": {
                        "running": "running",
                        "terminated": "terminated",
                        "waiting": "waiting"
                    },
                    "terminated": {
                        "swagger_types": {
                            "started_at": "datetime",
                            "finished_at": "datetime",
                            "message": "str",
                            "container_id": "str",
                            "signal": "int",
                            "exit_code": "int",
                            "reason": "str"
                        },
                        "started_at": "2018-02-26T20:31:23.000+0000",
                        "finished_at": "2018-03-18T15:07:37.000+0000",
                        "exit_code": 255,
                        "container_id": "docker://aa335750544c05fadd473dd841ff86111af4508311365e07391c5374e7e3c858",
                        "signal": None,
                        "message": None,
                        "attribute_map": {
                            "started_at": "startedAt",
                            "finished_at": "finishedAt",
                            "message": "message",
                            "container_id": "containerID",
                            "signal": "signal",
                            "exit_code": "exitCode",
                            "reason": "reason"
                        },
                        "reason": "Error"
                    },
                    "waiting": None,
                    "swagger_types": {
                        "running": "V1ContainerStateRunning",
                        "terminated": "V1ContainerStateTerminated",
                        "waiting": "V1ContainerStateWaiting"
                    }
                },
                "container_id": "docker://c6e22b9b79bd39309efbad6aa14a379e35b17379737a5a405d31f7186f327d83",
                "image": "korenlev/calipso:cisco-web",
                "image_id": "docker-pullable://korenlev/calipso@sha256:c877b2df87cc5f05c190c0e2473880d007408b0be421830d2fbd83c8f9e29b35",
                "swagger_types": {
                    "state": "V1ContainerState",
                    "restart_count": "int",
                    "name": "str",
                    "last_state": "V1ContainerState",
                    "container_id": "str",
                    "image": "str",
                    "ready": "bool",
                    "image_id": "str"
                },
                "ready": True
            }
        ]
    },
    "name": "cisco-portal-deployment-ha-74f6b66557-wjpg2",
    "parent_text": "Pods",
    "host": "kub2-aci",
    "object_name": "cisco-portal-deployment-ha-74f6b66557-wjpg2",
    "parent_id": "kub2-aci-pods"
}

CONTAINERS_FOLDER_ID = '{}-containers'.format(POD_DOCUMENT['id'])

PODS_RESPONSE_NO_MATCH = deepcopy(PODS_RESPONSE)
PODS_RESPONSE_NO_MATCH['items'][0]['metadata']['uid'] = "ee4d79c3-376b-456a-b474-fdfefd1796ee"

_CONTAINER_STATUS = POD_DOCUMENT['pod_status']['container_statuses'][0]
_CONTAINER_NAME = _CONTAINER_STATUS['name']
_CONTAINER_ID = _CONTAINER_STATUS['container_id'].split("docker://")[-1]
EXPECTED_CONTAINER_DOC = {
    'id': "{}-{}".format(POD_DOCUMENT['id'], _CONTAINER_NAME),
    'container_id': _CONTAINER_ID,
    'type': "container",
    'name': _CONTAINER_NAME,
    'pod': {'id': POD_DOCUMENT['id'], 'name': POD_DOCUMENT['name']},
    'namespace': POD_DOCUMENT['namespace'],
    'host': POD_DOCUMENT['host'],
}
