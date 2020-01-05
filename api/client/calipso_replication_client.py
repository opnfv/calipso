import argparse
import json
import time
import traceback
import ssl
from pymongo import MongoClient
from sys import exit
from six.moves import input
from six.moves.urllib.parse import quote_plus

DEFAULT_PORT = 27017
DEFAULT_USER = 'calipso'
AUTH_DB = 'calipso'
DEBUG = False

max_connection_attempts = 5
collection_names = ["environments_config", "inventory", "links", "messages", "scans", "scheduled_scans", "cliques"]
reconstructable_collections = ["inventory", "links", "cliques"]


def debug(msg):
    if DEBUG is True:
        print(msg)


class MongoConnector(object):
    def __init__(self, host, port, user, pwd, db, db_label="central DB"):
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
        self.connect()

    def connect(self):
        self.disconnect()
        self.uri = "mongodb://%s:%s@%s:%s/%s" % (quote_plus(self.user), quote_plus(self.pwd),
                                                 self.host, self.port, self.db)
        self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000,
                                  ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
        self.database = self.client[self.db]

    def disconnect(self):
        if self.client:
            print("Disconnecting from {}...".format(self.db_label))
            self.client.close()
            self.client = None

    def clear_collection(self, collection):
        self.database[collection].remove()

    def find_all(self, collection, remove_mongo_ids=False, env=None):
        if not env:
            env = {"$exists": True}
        if collection == "environments_config":
            if env:
                cursor = self.database[collection].find({"name": env})
            else:
                cursor = self.database[collection].find()
        else:
            mongo_filter = {"environment": env}
            cursor = self.database[collection].find(mongo_filter)
        docs = []
        for doc in cursor:
            if remove_mongo_ids is True:
                original_id = doc.pop('_id')
                if collection in reconstructable_collections:
                    doc['original_id'] = original_id
            docs.append(doc)
        return docs

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


def backoff(i):
    return 2 ** (i - 1)


def read_servers_from_cli():
    try:
        servers_count = int(input("How many Calipso Servers to replicate? "))
        if servers_count < 1:
            raise TypeError()
    except TypeError:
        print("Server count should be a positive integer")
        return 1

    servers = []
    for n in range(1, servers_count + 1):
        remote_name = input("Remote Calipso Server #{} Hostname/IP\n".format(n))
        remote_secret = input("Remote Calipso Server #{} Secret\n".format(n))
        servers.append({"name": remote_name, "secret": remote_secret, "attempt": 0, "imported": False})

    central_name = input("Central Calipso Server Hostname/IP\n")
    central_secret = input("Central Calipso Server Secret\n")

    central = {'name': central_name, 'secret': central_secret}
    return servers, central


def read_servers_from_file(filename):
    with open(filename) as f:
        config = json.load(f)

        servers = [
            {"name": r['name'], "secret": r['secret'], "attempt": 0, "imported": False}
            for r in config['remotes']
        ]

        return servers, config['central']


def reconstruct_ids(destination_connector):
    print("Fixing ids for links and cliques")
    rc = {}
    for col in reconstructable_collections:
        rc[col] = {}
        objects = destination_connector.find_all(col)
        for obj in objects:
            original_id = obj.pop("original_id")
            rc[col][original_id] = obj

    for link_orig_id, link in rc["links"].items():
        if 'source' not in link or 'target' not in link:
            debug("Malformed link: {}".format(link))
            continue
        link["source"] = rc["inventory"][link["source"]]["_id"]
        link["target"] = rc["inventory"][link["target"]]["_id"]

    for clique_orig_id, clique in rc["cliques"].items():
        if any(req_field not in clique for req_field in ('links', 'links_detailed')):
            debug("Malformed clique: {}".format(clique))
            continue

        clique["focal_point"] = rc["inventory"][clique["focal_point"]]["_id"]

        if 'nodes' in clique:
            debug("No nodes defined in clique: {}".format(clique["_id"]))
            clique["nodes"] = [rc["inventory"][node_id]["_id"] for node_id in clique["nodes"]]

        clique_new_links, clique_new_links_detailed = [], []
        for link_id in clique["links"]:
            new_link = rc["links"][link_id]
            clique_new_links.append(new_link["_id"])
            clique_new_links_detailed.append(new_link)

        clique["links"] = clique_new_links
        clique["links_detailed"] = clique_new_links_detailed

    for col in reconstructable_collections:
        destination_connector.clear_collection(col)
        destination_connector.insert_collection(col, list(rc[col].values()))


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config",
                        help="Path to server configurations json file",
                        type=str,
                        required=False)
    parser.add_argument("--debug",
                        help="Print debug messages",
                        action="store_true",
                        required=False)
    parser.add_argument("--version",
                        help="get a reply back with replication_client version",
                        action='version',
                        default=None,
                        version='%(prog)s version: 0.6.8')

    args = parser.parse_args()

    global DEBUG
    DEBUG = args.debug

    servers, central = read_servers_from_file(args.config) if args.config else read_servers_from_cli()

    if not servers or all(s['imported'] is True for s in servers):
        print("Nothing to do. Exiting")
        return 0

    destination_connector = MongoConnector(central['name'], DEFAULT_PORT, DEFAULT_USER, central['secret'], AUTH_DB)
    for col in collection_names:
        print ("Clearing collection {} from {}...".format(col, central['name']))
        destination_connector.clear_collection(col)

    while all(s['imported'] is False for s in servers):
        source_connector = None
        for s in servers:
            s['attempt'] += 1
            if s['attempt'] > 1:
                print("Retrying import from remote {}... Attempt #{}".format(s['name'], s['attempt']))
                time.sleep(backoff(s['attempt']))

            try:
                source_connector = MongoConnector(s["name"], DEFAULT_PORT, DEFAULT_USER, s["secret"], AUTH_DB)
                for col in collection_names:
                    # read from remote DBs and export to local json files
                    print("Getting the {} Collection from {}...".format(col, s["name"]))

                    documents = source_connector.find_all(col, remove_mongo_ids=True)

                    # write all in-memory json docs into the central DB
                    print("Pushing the {} Collection into {}...".format(col, central['name']))
                    destination_connector.insert_collection(col, documents)

                s['imported'] = True
                source_connector.disconnect()
                source_connector = None
            except Exception as e:
                print("Failed to connect to {}, error: {}".format(s["name"], e.args))
                if source_connector is not None:
                    source_connector.disconnect()
                # traceback.print_exc()

                if s['attempt'] >= max_connection_attempts:
                    destination_connector.disconnect()
                    print("Failed to perform import from remote {}. Tried {} times".format(s['name'], s['attempt']))
                    return 1
                break

    # reconstruct source-target ids for links and cliques
    reconstruct_ids(destination_connector)
    destination_connector.disconnect()
    print("Workload completed")
    return 0


if __name__ == "__main__":
    exit(run())
