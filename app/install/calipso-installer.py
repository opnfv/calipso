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


class MongoComm:
    # deals with communication from host/installer server to mongoDB, includes methods for future use
    try:

        def __init__(self, host, user, password, port):
            self.uri = "mongodb://%s:%s@%s:%s/%s" % (
                quote_plus(user), quote_plus(password), host, port, "calipso")
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
            doc_id = collection.update_one({'_id': doc['_id']},{'$set': doc}, upsert=upsert)
            return doc_id

    except ConnectionFailure:
        print("MongoDB Server not available")


DockerClient = docker.from_env()   # using local host docker environment parameters

# use the below example for installer against a remote docker host:
# DockerClient = docker.DockerClient(base_url='tcp://korlev-calipso-testing.cisco.com:2375')


def copy_file(filename):
    c = MongoComm(args.hostname, args.dbuser, args.dbpassword, args.dbport)
    txt = open('db/'+filename+'.json')
    data = json.load(txt)
    c.remove_coll(filename)
    doc_id = c.insert(filename, data)
    print("Copied", filename, "mongo doc_ids:\n\n", doc_id, "\n\n")
    time.sleep(1)


C_MONGO_CONFIG = "/local_dir/calipso_mongo_access.conf"
H_MONGO_CONFIG = "/home/calipso/calipso_mongo_access.conf"
PYTHONPATH = "/home/scan/calipso_prod/app"
C_LDAP_CONFIG = "/local_dir/ldap.conf"
H_LDAP_CONFIG = "/home/calipso/ldap.conf"

# functions to check and start calipso containers:
def start_mongo(dbport):
    if not DockerClient.containers.list(all=True, filters={"name": "calipso-mongo"}):
        print("\nstarting container calipso-mongo, please wait...\n")
        image = DockerClient.images.list(all=True, name="korenlev/calipso:mongo")
        if image:
            print(image, "exists...not downloading...")
        else:
            print("image korenlev/calipso:mongo missing, hold on while downloading first...\n")
            image = DockerClient.images.pull("korenlev/calipso:mongo")
            print("Downloaded", image, "\n\n")
        mongocontainer = DockerClient.containers.run('korenlev/calipso:mongo', detach=True, name="calipso-mongo",
                                                     ports={'27017/tcp': dbport, '28017/tcp': 28017},
                                                     restart_policy={"Name": "always"})
        # wait a bit till mongoDB is up before starting to copy the json files from 'db' folder:
        time.sleep(5)
        enable_copy = input("create initial calipso DB ? (copy json files from 'db' folder to mongoDB -"
                            " 'c' to copy, 'q' to skip):")
        if enable_copy == "c":
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

            # note : 'messages', 'roles', 'users' and some of the 'constants' are filled by calipso-ui at runtime
            # some other docs are filled later by scanning, logging and monitoring
        else:
            return
    else:
        print("container named calipso-mongo already exists, please deal with it using docker...\n")
        return


def start_listen():
    if not DockerClient.containers.list(all=True, filters={"name": "calipso-listen"}):
        print("\nstarting container calipso-listen...\n")
        image = DockerClient.images.list(all=True, name="korenlev/calipso:listen")
        if image:
            print(image, "exists...not downloading...")
        else:
            print("image korenlev/calipso:listen missing, hold on while downloading first...\n")
            image = DockerClient.images.pull("korenlev/calipso:listen")
            print("Downloaded", image, "\n\n")
        listencontainer = DockerClient.containers.run('korenlev/calipso:listen', detach=True, name="calipso-listen",
                                                      ports={'22/tcp': 50022},
                                                      restart_policy={"Name": "always"},
                                                      environment=["PYTHONPATH=" + PYTHONPATH,
                                                                   "MONGO_CONFIG=" + C_MONGO_CONFIG],
                                                      volumes={'/home/calipso': {'bind': '/local_dir', 'mode': 'rw'}})
    else:
        print("container named calipso-listen already exists, please deal with it using docker...\n")
        return


def start_ldap():
    if not DockerClient.containers.list(all=True, filters={"name": "calipso-ldap"}):
        print("\nstarting container calipso-ldap...\n")
        image = DockerClient.images.list(all=True, name="korenlev/calipso:ldap")
        if image:
            print(image, "exists...not downloading...")
        else:
            print("image korenlev/calipso:ldap missing, hold on while downloading first...\n")
            image = DockerClient.images.pull("korenlev/calipso:ldap")
            print("Downloaded", image, "\n\n")
        ldapcontainer = DockerClient.containers.run('korenlev/calipso:ldap', detach=True, name="calipso-ldap",
                                                    ports={'389/tcp': 389, '389/udp': 389},
                                                    restart_policy={"Name": "always"},
                                                    volumes={'/home/calipso/': {'bind': '/local_dir/', 'mode': 'rw'}})
    else:
        print("container named calipso-ldap already exists, please deal with it using docker...\n")
        return


def start_api():
    if not DockerClient.containers.list(all=True, filters={"name": "calipso-api"}):
        print("\nstarting container calipso-api...\n")
        image = DockerClient.images.list(all=True, name="korenlev/calipso:api")
        if image:
            print(image, "exists...not downloading...")
        else:
            print("image korenlev/calipso:api missing, hold on while downloading first...\n")
            image = DockerClient.images.pull("korenlev/calipso:api")
            print("Downloaded", image, "\n\n")
        apicontainer = DockerClient.containers.run('korenlev/calipso:api', detach=True, name="calipso-api",
                                                   ports={'8000/tcp': 8000, '22/tcp': 40022},
                                                   restart_policy={"Name": "always"},
                                                   environment=["PYTHONPATH=" + PYTHONPATH,
                                                                "MONGO_CONFIG=" + C_MONGO_CONFIG,
                                                                "LDAP_CONFIG=" + C_LDAP_CONFIG,
                                                                "LOG_LEVEL=DEBUG"],
                                                   volumes={'/home/calipso/': {'bind': '/local_dir/', 'mode': 'rw'}})
    else:
        print("container named calipso-api already exists, please deal with it using docker...\n")
        return


def start_scan():
    if not DockerClient.containers.list(all=True, filters={"name": "calipso-scan"}):
        print("\nstarting container calipso-scan...\n")
        image = DockerClient.images.list(all=True, name="korenlev/calipso:scan")
        if image:
            print(image, "exists...not downloading...")
        else:
            print("image korenlev/calipso:scan missing, hold on while downloading first...\n")
            image = DockerClient.images.pull("korenlev/calipso:scan")
            print("Downloaded", image, "\n\n")
        scancontainer = DockerClient.containers.run('korenlev/calipso:scan', detach=True, name="calipso-scan",
                                                    ports={'22/tcp': 30022},
                                                    restart_policy={"Name": "always"},
                                                    environment=["PYTHONPATH=" + PYTHONPATH,
                                                                 "MONGO_CONFIG=" + C_MONGO_CONFIG],
                                                    volumes={'/home/calipso/': {'bind': '/local_dir/', 'mode': 'rw'}})
    else:
        print("container named calipso-scan already exists, please deal with it using docker...\n")
        return


def start_sensu():
    if not DockerClient.containers.list(all=True, filters={"name": "calipso-sensu"}):
        print("\nstarting container calipso-sensu...\n")
        image = DockerClient.images.list(all=True, name="korenlev/calipso:sensu")
        if image:
            print(image, "exists...not downloading...")
        else:
            print("image korenlev/calipso:sensu missing, hold on while downloading first...\n")
            image = DockerClient.images.pull("korenlev/calipso:sensu")
            print("Downloaded", image, "\n\n")
        sensucontainer = DockerClient.containers.run('korenlev/calipso:sensu', detach=True, name="calipso-sensu",
                                                     ports={'22/tcp': 20022, '3000/tcp': 3000, '4567/tcp': 4567,
                                                            '5671/tcp': 5671, '15672/tcp': 15672},
                                                     restart_policy={"Name": "always"},
                                                     environment=["PYTHONPATH=" + PYTHONPATH],
                                                     volumes={'/home/calipso/': {'bind': '/local_dir/', 'mode': 'rw'}})
    else:
        print("container named calipso-sensu already exists, please deal with it using docker...\n")
        return


def start_ui(host, dbuser, dbpassword, webport, dbport):
    if not DockerClient.containers.list(all=True, filters={"name": "calipso-ui"}):
        print("\nstarting container calipso-ui...\n")
        image = DockerClient.images.list(all=True, name="korenlev/calipso:ui")
        if image:
            print(image, "exists...not downloading...")
        else:
            print("image korenlev/calipso:ui missing, hold on while downloading first...\n")
            image = DockerClient.images.pull("korenlev/calipso:ui")
            print("Downloaded", image, "\n\n")
        uicontainer = DockerClient.containers.run('korenlev/calipso:ui', detach=True, name="calipso-ui",
                                                  ports={'3000/tcp': webport},
                                                  restart_policy={"Name": "always"},
                                                  environment=["ROOT_URL=http://{}:{}".format(host, str(webport)),
                                                               "MONGO_URL=mongodb://{}:{}@{}:{}/calipso".format
                                                               (dbuser, dbpassword, host, str(dbport)),
                                                               "LDAP_CONFIG=" + C_LDAP_CONFIG])
    else:
        print("container named calipso-ui already exists, please deal with it using docker...\n")
        return


# function to check and stop calipso containers:

def container_stop(container_name):
    if DockerClient.containers.list(all=True, filters={"name": container_name}):
        print("fetching container name", container_name, "...\n")
        c = DockerClient.containers.get(container_name)
        if c.status != "running":
            print(container_name, "is not running...")
            time.sleep(1)
            print("removing container name", c.name, "...\n")
            c.remove()
        else:
            print("killing container name", c.name, "...\n")
            c.kill()
            time.sleep(1)
            print("removing container name", c.name, "...\n")
            c.remove()
    else:
        print("no container named", container_name, "found...")


# parser for getting optional command arguments:
parser = argparse.ArgumentParser()
parser.add_argument("--hostname", help="Hostname or IP address of the server (default=172.17.0.1)",type=str,
                    default="172.17.0.1", required=False)
parser.add_argument("--webport", help="Port for the Calipso WebUI (default=80)",type=int,
                    default="80", required=False)
parser.add_argument("--dbport", help="Port for the Calipso MongoDB (default=27017)",type=int,
                    default="27017", required=False)
parser.add_argument("--dbuser", help="User for the Calipso MongoDB (default=calipso)",type=str,
                    default="calipso", required=False)
parser.add_argument("--dbpassword", help="Password for the Calipso MongoDB (default=calipso_default)",type=str,
                    default="calipso_default", required=False)
args = parser.parse_args()

container = ""
action = ""
container_names = ["all", "calipso-mongo", "calipso-scan", "calipso-listen", "calipso-ldap", "calipso-api",
                     "calipso-sensu", "calipso-ui"]
container_actions = ["stop", "start"]
while action not in container_actions:
    action = input("Action? (stop, start, or 'q' to quit):\n")
    if action == "q":
        exit()
while container not in container_names:
    container = input("Container? (all, calipso-mongo, calipso-scan, calipso-listen, calipso-ldap, calipso-api, "
                      "calipso-sensu, calipso-ui or 'q' to quit):\n")
    if container == "q":
        exit()

# starting the containers per arguments:
if action == "start":
    # building /home/calipso/calipso_mongo_access.conf and /home/calipso/ldap.conf files, per the arguments:
    calipso_mongo_access_text = "server " + args.hostname + "\nuser " + args.dbuser + "\npassword " + \
                                args.dbpassword + "\nauth_db calipso"
    ldap_text = "user admin" + "\npassword password" + "\nurl ldap://" + args.hostname + ":389" + \
                "\nuser_id_attribute CN" + "\nuser_pass_attribute userpassword" + \
                "\nuser_objectclass inetOrgPerson" + \
                "\nuser_tree_dn OU=Users,DC=openstack,DC=org" + "\nquery_scope one" + \
                "\ntls_req_cert allow" + \
                "\ngroup_member_attribute member"
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
        start_mongo(args.dbport)
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
        start_ui(args.hostname, args.dbuser, args.dbpassword, args.webport, args.dbport)
        time.sleep(1)

# stopping the containers per arguments:
if action == "stop":
    if container == "calipso-mongo" or container == "all":
        container_stop("calipso-mongo")
    if container == "calipso-listen" or container == "all":
        container_stop("calipso-listen")
    if container == "calipso-ldap" or container == "all":
        container_stop("calipso-ldap")
    if container == "calipso-api" or container == "all":
        container_stop("calipso-api")
    if container == "calipso-scan" or container == "all":
        container_stop("calipso-scan")
    if container == "calipso-sensu" or container == "all":
        container_stop("calipso-sensu")
    if container == "calipso-ui" or container == "all":
        container_stop("calipso-ui")
