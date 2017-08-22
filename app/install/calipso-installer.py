###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from pymongo import MongoClient, ReturnDocument
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus
import docker
import argparse
import dockerpycreds
# note : not used, useful for docker api security if used
import time
import json


C_MONGO_CONFIG = "/local_dir/calipso_mongo_access.conf"
H_MONGO_CONFIG = "/home/calipso/calipso_mongo_access.conf"
PYTHONPATH = "/home/scan/calipso_prod/app"
C_LDAP_CONFIG = "/local_dir/ldap.conf"
H_LDAP_CONFIG = "/home/calipso/ldap.conf"


calipso_volume = {'/home/calipso': {'bind': '/local_dir', 'mode': 'rw'}}
RESTART_POLICY = {"Name": "always"}

# environment variables definitions
PYTHON_PATH = "PYTHONPATH=" + PYTHONPATH
MONGO_CONFIG = "MONGO_CONFIG=" + C_MONGO_CONFIG
LDAP_CONFIG = "LDAP_CONFIG=" + C_LDAP_CONFIG
LOG_LEVEL = "LOG_LEVEL=DEBUG"


class MongoComm:
    # deals with communication from host/installer server to mongoDB,
    # includes methods for future use
    try:

        def __init__(self, host, user, pwd, port):
            self.uri = "mongodb://%s:%s@%s:%s/%s" % (
                quote_plus(user), quote_plus(pwd), host, port, "calipso")
            self.client = MongoClient(self.uri)

        def find(self, coll, key, val):
            collection = self.client.calipso[coll]
            doc = collection.find({key: val})
            return doc

        def get(self, coll, doc_name):
            collection = self.client.calipso[coll]
            doc = collection.find_one({"name": doc_name})
            return doc

        def insert(self, coll, doc):
            collection = self.client.calipso[coll]
            doc_id = collection.insert(doc)
            return doc_id

        def remove_doc(self, coll, doc):
            collection = self.client.calipso[coll]
            collection.remove(doc)

        def remove_coll(self, coll):
            collection = self.client.calipso[coll]
            collection.remove()

        def find_update(self, coll, key, val, data):
            collection = self.client.calipso[coll]
            collection.find_one_and_update(
                {key: val},
                {"$set": data},
                upsert=True
            )

        def update(self, coll, doc, upsert=False):
            collection = self.client.calipso[coll]
            doc_id = collection.update_one({'_id': doc['_id']},
                                           {'$set': doc},
                                           upsert=upsert)
            return doc_id

    except ConnectionFailure:
        print("MongoDB Server not available")


# using local host docker environment parameters
DockerClient = docker.from_env()

# use the below example for installer against a remote docker host:
# DockerClient = \
# docker.DockerClient(base_url='tcp://korlev-calipso-testing.cisco.com:2375')


def copy_file(filename):
    c = MongoComm(args.hostname, args.dbuser, args.dbpassword, args.dbport)
    txt = open( 'db/' + filename +'.json')
    data = json.load(txt)
    c.remove_coll(filename)
    doc_id = c.insert(filename, data)
    print("Copied", filename, "mongo doc_ids:\n\n", doc_id, "\n\n")
    time.sleep(1)


def container_started(name: str, print_message=True):
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
def start_mongo(dbport, copy):
    name = "calipso-mongo"
    if container_started(name):
        return
    print("\nstarting container {}, please wait...\n".format(name))
    image_name = "korenlev/calipso:mongo"
    download_image(image_name)
    mongo_ports = {'27017/tcp': dbport, '28017/tcp': 28017}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=mongo_ports,
                                restart_policy=RESTART_POLICY)
    # wait a bit till mongoDB is up before starting to copy the json files
    # from 'db' folder:
    time.sleep(5)
    if copy is not None:
        enable_copy = copy
    else:
        enable_copy = input("create initial calipso DB ? "
                            "(copy json files from 'db' folder to mongoDB - "
                            "'c' to copy, 'q' to skip):")
    if enable_copy != "c":
        return
    print("\nstarting to copy json files to mongoDB...\n\n")
    print("-----------------------------------------\n\n")
    time.sleep(1)
    copy_file("attributes_for_hover_on_data")
    copy_file("clique_constraints")
    copy_file("clique_types")
    copy_file("cliques")
    copy_file("constants")
    copy_file("environments_config")
    copy_file("inventory")
    copy_file("link_types")
    copy_file("links")
    copy_file("messages")
    copy_file("meteor_accounts_loginServiceConfiguration")
    copy_file("users")
    copy_file("monitoring_config")
    copy_file("monitoring_config_templates")
    copy_file("network_agent_types")
    copy_file("roles")
    copy_file("scans")
    copy_file("scheduled_scans")
    copy_file("statistics")
    copy_file("supported_environments")

    # note : 'messages', 'roles', 'users' and some of the 'constants'
    # are filled by calipso-ui at runtime
    # some other docs are filled later by scanning, logging
    # and monitoring


def start_listen():
    name = "calipso-listen"
    if container_started(name):
        return
    print("\nstarting container {}...\n".format(name))
    image_name = "korenlev/calipso:listen"
    download_image(image_name)
    ports = {'22/tcp': 50022}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=ports,
                                restart_policy=RESTART_POLICY,
                                environment=[PYTHON_PATH, MONGO_CONFIG],
                                volumes=calipso_volume)


def start_ldap():
    name = "calipso-ldap"
    if container_started(name):
        return
    print("\nstarting container {}...\n".format(name))
    image_name = "korenlev/calipso:ldap"
    download_image(image_name)
    ports = {'389/tcp': 389, '389/udp': 389}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=ports,
                                restart_policy=RESTART_POLICY,
                                volumes=calipso_volume)


def start_api():
    name = "calipso-api"
    if container_started(name):
        return
    print("\nstarting container {}...\n".format(name))
    image_name = "korenlev/calipso:api"
    download_image(image_name)
    api_ports = {'8000/tcp': 8000, '22/tcp': 40022}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=api_ports,
                                restart_policy=RESTART_POLICY,
                                environment=[PYTHON_PATH, MONGO_CONFIG,
                                             LDAP_CONFIG,
                                             LOG_LEVEL],
                                volumes=calipso_volume)


def start_scan():
    name = "calipso-scan"
    if container_started(name):
        return
    print("\nstarting container {}...\n".format(name))
    image_name = "korenlev/calipso:scan"
    download_image(image_name)
    ports = {'22/tcp': 30022}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=ports,
                                restart_policy=RESTART_POLICY,
                                environment=[PYTHON_PATH, MONGO_CONFIG],
                                volumes=calipso_volume)


def start_sensu():
    name = "calipso-sensu"
    if container_started(name):
        return
    print("\nstarting container {}...\n".format(name))
    image_name = "korenlev/calipso:sensu"
    download_image(image_name)
    sensu_ports = {'22/tcp': 20022, '3000/tcp': 3000, '4567/tcp': 4567,
                   '5671/tcp': 5671, '15672/tcp': 15672}
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
    image_name = "korenlev/calipso:ui"
    download_image(image_name)
    root_url = "ROOT_URL=http://{}:{}".format(host, str(webport))
    mongo_url = "MONGO_URL=mongodb://{}:{}@{}:{}/calipso" \
        .format(dbuser, dbpassword, host, str(dbport))
    ports = {'3000/tcp': webport}
    DockerClient.containers.run(image_name,
                                detach=True,
                                name=name,
                                ports=ports,
                                restart_policy=RESTART_POLICY,
                                environment=[root_url, mongo_url, LDAP_CONFIG])


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
                    help="Hostname or IP address of the server "
                         "(default=172.17.0.1)",
                    type=str,
                    default="172.17.0.1",
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
parser.add_argument("--command",
                    help="'start-all' or 'stop-all' the calipso containers "
                         "(default=None)",
                    type=str,
                    default=None,
                    required=False)
parser.add_argument("--copy",
                    help="'c' to copy json files from 'db' folder to mongoDB, 'q' to skip copy of files "
                         "(default=q)",
                    type=str,
                    default=None,
                    required=False)
args = parser.parse_args()

if args.command == "start-all":
    container = "all"
    action = "start"
elif args.command == "stop-all":
    container = "all"
    action = "stop"
else:
    container = ""
    action = ""

container_names = ["calipso-mongo", "calipso-scan", "calipso-listen",
                   "calipso-ldap", "calipso-api", "calipso-sensu", "calipso-ui"]
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

# starting the containers per arguments:
if action == "start":
    # building /home/calipso/calipso_mongo_access.conf and
    # /home/calipso/ldap.conf files, per the arguments:
    calipso_mongo_access_text = \
        "server {}\n" \
        "user {}\n" \
        "pwd {}\n" \
        "auth_db calipso" \
            .format(args.hostname, args.dbuser, args.dbpassword)
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
    print("creating default", H_MONGO_CONFIG, "file...\n")
    calipso_mongo_access_file = open(H_MONGO_CONFIG, "w+")
    time.sleep(1)
    calipso_mongo_access_file.write(calipso_mongo_access_text)
    calipso_mongo_access_file.close()
    print("creating default", H_LDAP_CONFIG, "file...\n")
    ldap_file = open(H_LDAP_CONFIG, "w+")
    time.sleep(1)
    ldap_file.write(ldap_text)
    ldap_file.close()

    if container == "calipso-mongo" or container == "all":
        start_mongo(args.dbport, args.copy)
        time.sleep(1)
    if container == "calipso-listen" or container == "all":
        start_listen()
        time.sleep(1)
    if container == "calipso-ldap" or container == "all":
        start_ldap()
        time.sleep(1)
    if container == "calipso-api" or container == "all":
        start_api()
        time.sleep(1)
    if container == "calipso-scan" or container == "all":
        start_scan()
        time.sleep(1)
    if container == "calipso-sensu" or container == "all":
        start_sensu()
        time.sleep(1)
    if container == "calipso-ui" or container == "all":
        start_ui(args.hostname, args.dbuser, args.dbpassword, args.webport,
                 args.dbport)
        time.sleep(1)

# stopping the containers per arguments:
if action == "stop":
    for name_to_stop in container_names:
        if container == name_to_stop or container == "all":
            container_stop(name_to_stop)
