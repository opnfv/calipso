###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import docker
import argparse
# note : not used, useful for docker api security if used
import time
import json
import socket
# by default, we want to use the docker0 interface ip address for inter-contatiner communications,
# if hostname argument will not be provided as argument for the calipso-installer
import os
import errno
from six.moves import input

from pymongo import MongoClient
from six.moves.urllib.parse import quote_plus


dockerip = os.popen('ip addr show docker0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'')
local_hostname = dockerip.read().replace("\n", "")

C_MONGO_CONFIG = "/local_dir/calipso_mongo_access.conf"
H_MONGO_CONFIG = "calipso_mongo_access.conf"
C_ES_CONFIG = "/local_dir/calipso_es_access.conf"
H_ES_CONFIG = "calipso_es_access.conf"
PYTHONPATH = "/home/scan/calipso"
C_LDAP_CONFIG = "/local_dir/ldap.conf"
H_LDAP_CONFIG = "ldap.conf"

RESTART_POLICY = {"Name": "always"}

# environment variables definitions
PYTHON_PATH = "PYTHONPATH={}".format(PYTHONPATH)
MONGO_CONFIG = "MONGO_CONFIG={}".format(C_MONGO_CONFIG)
ES_CONFIG = "ES_CONFIG={}".format(C_ES_CONFIG)
LDAP_CONFIG = "LDAP_CONFIG={}".format(C_LDAP_CONFIG)
LOG_LEVEL = "LOG_LEVEL=DEBUG"

# using local host docker environment parameters
DockerClient = docker.from_env()

# to use the below example for installer against a remote docker host:
# DockerClient = \
# docker.DockerClient(base_url='tcp://korlev-calipso-testing.cisco.com:2375')


class MongoConnector(object):
    def __init__(self, host, port, user, pwd, db, db_label="db"):
        # Create calipso db and user if they don't exist
        base_uri = "mongodb://%s:%s/" % (host, port)
        base_client = MongoClient(base_uri)
        base_client.close()

        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db
        self.db_label = db_label

        self.uri = None
        self.client = None
        self.database = None

    def connect(self):
        self.disconnect()
        self.uri = "mongodb://%s:%s@%s:%s/%s" % (quote_plus(self.user), quote_plus(self.pwd),
                                                 self.host, self.port, self.db)
        self.client = MongoClient(self.uri)
        self.database = self.client[self.db]

    def __enter__(self):
        self.connect()
        return self

    def disconnect(self):
        if self.client:
            print("Disconnecting from {}...".format(self.db_label))
            self.client.close()
            self.client = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def clear_collection(self, collection):
        self.database[collection].remove()

    def collection_exists(self, name):
        return name in self.database.collection_names()

    def create_collection(self, name):
        return self.database.create_collection(name)

    def insert_collection(self, collection, data):
        if data:
            doc_ids = self.database[collection].insert(data)
            doc_count = len(doc_ids) if isinstance(doc_ids, list) else 1
            print("Inserted '{}' collection in {}, Total docs inserted: {}".format(collection, self.db_label, doc_count))
        elif not self.collection_exists(collection):
            self.create_collection(collection)
            print("Inserted empty '{}' collection in {}".format(collection, self.db_label))
        else:
            print("Skipping empty '{}' collection".format(collection,))


def insert_data(conn, filename):
    with open('../../mongo/initial_data/{}.json'.format(filename)) as file:
        data = json.load(file)
        conn.clear_collection(filename)
        conn.insert_collection(filename, data)


def container_started(name, print_message=True):
    found = DockerClient.containers.list(all=True, filters={"name": name})
    if found and print_message:
        print("container named {} already exists, "
              "please deal with it using docker...\n"
              .format(name))
    return bool(found)


def download_image(image_name):
    image = DockerClient.images.list(all=True, name=image_name)

    if image:
        print(image, "exists...not downloading...")
        return

    print("image {} missing, "
          "hold on while downloading first...\n"
          .format(image_name))
    image = DockerClient.images.pull(image_name)
    print("Downloaded", image, "\n\n")


# functions to check and start calipso containers:
def start_elastic(esport):
    name = "calipso-elastic"
    if container_started(name):
        return
    print("\nstarting container {}, please wait...\n".format(name))
    image_name = "korenlev/calipso:elastic-v2"
    download_image(image_name)
    elastic_ports = {'9200/tcp': esport, '9300/tcp': 9300}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=elastic_ports,
                                restart_policy=RESTART_POLICY)


def start_kibana(kport, esport):
    name = "calipso-kibana"
    if container_started(name):
        return
    print("\nstarting container {}, please wait...\n".format(name))
    image_name = "korenlev/calipso:kibana-v2"
    download_image(image_name)
    elastic_vars = ["CALIPSO_ELASTIC_SERVICE_HOST={}".format(local_hostname),
                    "CALIPSO_ELASTIC_SERVICE_PORT={}".format(esport)]
    kibana_ports = {'5601/tcp': kport}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=kibana_ports,
                                environment=elastic_vars,
                                restart_policy=RESTART_POLICY)


def start_grafana(gport):
    name = "calipso-grafana"
    if container_started(name):
        return
    print("\nstarting container {}, please wait...\n".format(name))
    image_name = "korenlev/calipso:grafana-v2"
    download_image(image_name)
    grafana_ports = {'30000/tcp': gport}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=grafana_ports,
                                restart_policy=RESTART_POLICY)


def start_mongo(dbport, copy):
    name = "calipso-mongo"
    if container_started(name):
        return
    print("\nstarting container {}, please wait...\n".format(name))
    image_name = "korenlev/calipso:mongo-v2"
    download_image(image_name)
    mongo_ports = {'27017/tcp': dbport, '28017/tcp': 28017}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                volumes=calipso_volume,
                                ports=mongo_ports,
                                restart_policy=RESTART_POLICY)
    # wait a bit till mongoDB is up before starting to copy the json files
    # from 'initial_data' folder:
    time.sleep(5)
    if copy is not None:
        enable_copy = copy
    else:
        enable_copy = input("create initial calipso DB ? "
                            "(copy json files from 'initial_data' folder to mongoDB - "
                            "'c' to copy, 'q' to skip):")
    if enable_copy != "c":
        return
    print("\nstarting to copy json files to mongoDB...\n\n")
    print("-----------------------------------------\n\n")
    with MongoConnector(host=args.hostname, port=args.dbport, user=args.dbuser, pwd=args.dbpassword,
                        db="calipso", db_label="db") as conn:
        for collection in ("api_tokens", "attributes_for_hover_on_data", "clique_constraints", "clique_types",
                           "cliques", "connection_tests", "constants", "environment_options", "environments_config",
                           "inventory", "link_types", "links", "messages", "meteor_accounts_loginServiceConfiguration",
                           "monitoring_config", "monitoring_config_templates", "network_agent_types", "roles", "scans",
                           "scheduled_scans", "statistics", "supported_environments", "user_settings", "users"):
            insert_data(conn, collection)
    # note : 'messages', 'roles', 'users' and some of the 'constants'
    # are filled by calipso-ui at runtime
    # some other docs are filled later by scanning, logging
    # and monitoring


def start_listen():
    name = "calipso-listen"
    if container_started(name):
        return
    print("\nstarting container {}...\n".format(name))
    image_name = "korenlev/calipso:listen-v2"
    download_image(image_name)
    ports = {'22/tcp': 50022}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=ports,
                                restart_policy=RESTART_POLICY,
                                environment=[PYTHON_PATH, MONGO_CONFIG, ES_CONFIG],
                                volumes=calipso_volume)


def start_ldap():
    name = "calipso-ldap"
    if container_started(name):
        return
    print("\nstarting container {}...\n".format(name))
    image_name = "korenlev/calipso:ldap-v2"
    download_image(image_name)
    ports = {'389/tcp': 389, '389/udp': 389}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=ports,
                                restart_policy=RESTART_POLICY,
                                volumes=calipso_volume)


def start_api(apiport):
    name = "calipso-api"
    if container_started(name):
        return
    print("\nstarting container {}...\n".format(name))
    image_name = "korenlev/calipso:api-v2"
    download_image(image_name)
    api_ports = {'8000/tcp': apiport, '22/tcp': 40022}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=api_ports,
                                restart_policy=RESTART_POLICY,
                                environment=[PYTHON_PATH, MONGO_CONFIG,
                                             LDAP_CONFIG,
                                             LOG_LEVEL, ES_CONFIG],
                                volumes=calipso_volume)


def start_scan():
    name = "calipso-scan"
    if container_started(name):
        return
    print("\nstarting container {}...\n".format(name))
    image_name = "korenlev/calipso:scan-v2"
    download_image(image_name)
    ports = {'22/tcp': 30022}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=ports,
                                restart_policy=RESTART_POLICY,
                                environment=[PYTHON_PATH, MONGO_CONFIG, ES_CONFIG],
                                volumes=calipso_volume)


def start_monitor(uchiwaport, sensuport, rabbitport, rabbitmport):
    name = "calipso-monitor"
    if container_started(name):
        return
    print("\nstarting container {}...\n".format(name))
    image_name = "korenlev/calipso:monitor-v2"
    download_image(image_name)
    sensu_ports = {'22/tcp': 20022, '3000/tcp': uchiwaport, '4567/tcp': sensuport,
                   '5671/tcp': rabbitport, '15672/tcp': rabbitmport}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=sensu_ports,
                                restart_policy=RESTART_POLICY,
                                environment=[PYTHON_PATH],
                                volumes=calipso_volume)


def start_ui(host, dbuser, dbpassword, webport, dbport):
    name = "calipso-ui"
    if container_started(name):
        return
    print("\nstarting container {}...\n".format(name))
    image_name = "korenlev/calipso:ui-v2"
    download_image(image_name)
    root_url = "ROOT_URL=http://{}:{}".format(host, str(webport))
    mongo_url = "MONGO_URL=mongodb://{}:{}@{}:{}/calipso" \
        .format(dbuser, dbpassword, host, str(dbport))
    ports = {'4000/tcp': webport}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=ports,
                                restart_policy=RESTART_POLICY,
                                environment=[root_url, mongo_url, LDAP_CONFIG])


def start_test():
    name = "calipso-test"
    if container_started(name):
        return
    print("\nstarting container {}...\n".format(name))
    image_name = "korenlev/calipso:test-v2"
    download_image(image_name)
    ports = {'22/tcp': 10022}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=ports,
                                restart_policy=RESTART_POLICY,
                                environment=[PYTHON_PATH, MONGO_CONFIG, ES_CONFIG],
                                volumes=calipso_volume)


# check and stop a calipso container by given name
def container_stop(container_name):
    if not container_started(container_name, print_message=False):
        print("no container named", container_name, "found...")
        return
    print("fetching container name", container_name, "...\n")
    c = DockerClient.containers.get(container_name)
    if c.status != "running":
        print(container_name, "is not running...")
    else:
        print("killing container name", c.name, "...\n")
        c.kill()
        time.sleep(1)
    print("removing container name", c.name, "...\n")
    c.remove()


# parser for getting optional command arguments:
parser = argparse.ArgumentParser()
parser.add_argument("--hostname",
                    help="FQDN (ex:mysrv.cisco.com) or IP address of the Server"
                         "(default=docker0 interface ip address)",
                    type=str,
                    default=local_hostname,
                    required=False)
parser.add_argument("--webport",
                    help="Port for the Calipso WebUI "
                         "(default=80)",
                    type=int,
                    default="80",
                    required=False)
parser.add_argument("--dbport",
                    help="Port for the Calipso MongoDB "
                         "(default=27017)",
                    type=int,
                    default="27017",
                    required=False)
parser.add_argument("--apiport",
                    help="Port for the Calipso API "
                         "(default=8747)",
                    type=int,
                    default="8747",
                    required=False)
parser.add_argument("--uchiwaport",
                    help="Port for the Calipso Uchiwa "
                         "(default=3000)",
                    type=int,
                    default="3000",
                    required=False)
parser.add_argument("--rabbitmport",
                    help="Port for the Calipso Sensu RabbitMQ Management "
                         "(default=15672)",
                    type=int,
                    default="15672",
                    required=False)
parser.add_argument("--sensuport",
                    help="Port for the Calipso Sensu-api "
                         "(default=4567)",
                    type=int,
                    default="4567",
                    required=False)
parser.add_argument("--rabbitport",
                    help="Port for the Calipso Sensu RabbitMQ BUS"
                         "(default=5671)",
                    type=int,
                    default="5671",
                    required=False)
parser.add_argument("--dbuser",
                    help="User for the Calipso MongoDB "
                         "(default=calipso)",
                    type=str,
                    default="calipso",
                    required=False)
parser.add_argument("--dbpassword",
                    help="Password for the Calipso MongoDB "
                         "(default=calipso_default)",
                    type=str,
                    default="calipso_default",
                    required=False)
parser.add_argument("--es_index",
                    help="allow indexing environment inventory, links and cliques on ElasticSearch DB"
                         " options: boolean, add argument or not"
                         " (default=False)",
                    action='store_true',
                    default=False,
                    required=False)
parser.add_argument("--es_host",
                    help="Host with ElasticSearch if ElasticSearch indexing is needed "
                         "(default=docker0 interface ip address)",
                    type=str,
                    default=local_hostname,
                    required=False)
parser.add_argument("--es_port",
                    help="Port for ElasticSearch if ElasticSearch indexing is needed "
                         "(default=9200)",
                    type=str,
                    default="9200",
                    required=False)
parser.add_argument("--g_port",
                    help="Port for Grafana if grafana is needed "
                         "(default=30000)",
                    type=str,
                    default="30000",
                    required=False)
parser.add_argument("--k_port",
                    help="Port for Kibana if kibana  is needed "
                         "(default=5601)",
                    type=str,
                    default="5601",
                    required=False)
parser.add_argument("--home",
                    help="Home directory for configuration files "
                         "(default=/home/calipso)",
                    type=str,
                    default="/home/calipso",
                    required=False)
parser.add_argument("--command",
                    help="'start-all' or 'stop-all' the Calipso containers "
                         "(default=None)",
                    type=str,
                    default=None,
                    required=False)
parser.add_argument("--copy",
                    help="'c' to copy json files from 'initial_data' folder to mongoDB, 'q' to skip copy of files "
                         "(default=None)",
                    type=str,
                    default=None,
                    required=False)


args = parser.parse_args()
calipso_volume = {args.home: {'bind': '/local_dir', 'mode': 'rw'}, "/etc/localtime": {'bind': '/etc/localtime', 'mode': 'rw'}}

print("\nrunning installer against host:", args.hostname, "\n")

if args.command == "start-all":
    container = "all"
    action = "start"
elif args.command == "stop-all":
    container = "all"
    action = "stop"
else:
    container = ""
    action = ""

container_names = ["calipso-ui", "calipso-scan", "calipso-test", "calipso-listen",
                   "calipso-ldap", "calipso-api", "calipso-monitor", "calipso-mongo",
                   "calipso-elastic", "calipso-kibana", "calipso-grafana"]
container_actions = ["stop", "start"]
while action not in container_actions:
    action = input("Action? (stop, start, or 'q' to quit):\n")
    if action == "q":
        exit()
while container != "all" and container not in container_names:
    container = input("Container? (all, {} or 'q' to quit):\n"
                      .format(", ".join(container_names)))
    if container == "q":
        exit()

# create local directory on host, raise error if it doesn't exists 
try:
    os.makedirs(os.path.join(args.home, 'log/calipso'))
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# starting the containers per arguments:
if action == "start":
    # building mongo.conf and ldap.conf files, per the arguments:
    calipso_mongo_access_text = \
        "server {}\n" \
        "user {}\n" \
        "port {}\n" \
        "pwd {}\n" \
        "auth_db calipso".format(args.hostname, args.dbuser, args.dbport, args.dbpassword)

    LDAP_PWD_ATTRIBUTE = "password password"
    LDAP_USER_PWD_ATTRIBUTE = "userpassword"
    ldap_text = \
        "user admin\n" + \
        "{}\n" + \
        "url ldap://{}:389\n" + \
        "user_id_attribute CN\n" + \
        "user_pass_attribute {}\n" + \
        "user_objectclass inetOrgPerson\n" + \
        "user_tree_dn OU=Users,DC=openstack,DC=org\n" + \
        "query_scope one\n" + \
        "tls_req_cert allow\n" + \
        "group_member_attribute member"
    ldap_text = ldap_text.format(LDAP_PWD_ATTRIBUTE, args.hostname,
                                 LDAP_USER_PWD_ATTRIBUTE)
    if args.es_index:
        calipso_es_access_text = \
            "host {}\n" \
            "port {}\n".format(args.es_host, args.es_port)
        es_file_path = os.path.join(args.home, H_ES_CONFIG)
        calipso_es_access_file = open(es_file_path, "w+")
        calipso_es_access_file.write(calipso_es_access_text)
        calipso_es_access_file.close()
        print("\ncreating default", es_file_path, "file...\n")
        time.sleep(1)
    mongo_file_path = os.path.join(args.home, H_MONGO_CONFIG)
    print("\ncreating default", mongo_file_path, "file...\n")
    calipso_mongo_access_file = open(mongo_file_path, "w+")
    calipso_mongo_access_file.write(calipso_mongo_access_text)
    calipso_mongo_access_file.close()
    time.sleep(1)
    ldap_file_path = os.path.join(args.home, H_LDAP_CONFIG)
    print("\ncreating default", ldap_file_path, "file...\n")
    ldap_file = open(ldap_file_path, "w+")
    time.sleep(1)
    ldap_file.write(ldap_text)
    ldap_file.close()

    if container == "calipso-elastic" or container == "all":
        a = "elastic"
        start_elastic(args.es_port)
        time.sleep(4)
    if container == "calipso-grafana" or container == "all":
        start_grafana(args.g_port)
        time.sleep(1)
    if container == "calipso-mongo" or container == "all":
        start_mongo(args.dbport, args.copy)
        time.sleep(1)
    if container == "calipso-ldap" or container == "all":
        start_ldap()
        time.sleep(1)
    if container == "calipso-listen" or container == "all":
        start_listen()
        time.sleep(1)
    if container == "calipso-api" or container == "all":
        start_api(args.apiport)
        time.sleep(1)
    if container == "calipso-test" or container == "all":
        start_test()
        time.sleep(1)
    if container == "calipso-monitor" or container == "all":
        start_monitor(args.uchiwaport, args.sensuport, args.rabbitport, args.rabbitmport)
        time.sleep(1)
    if container == "calipso-ui" or container == "all":
        start_ui(args.hostname, args.dbuser, args.dbpassword, args.webport,
                 args.dbport)
        time.sleep(1)
    if container == "calipso-scan" or container == "all":
        start_scan()
        time.sleep(1)
    if container == "calipso-kibana" or container == "all":
        start_kibana(args.k_port, args.es_port)
        time.sleep(1)

# stopping the containers per arguments:
if action == "stop":
    for name_to_stop in container_names:
        if container == name_to_stop or container == "all":
            container_stop(name_to_stop)
