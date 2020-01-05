import argparse
import json
import os
import time
import traceback
import ssl
from urllib import quote_plus
from pymongo import MongoClient


INITIAL_DATA_PATH = "/calipso/mongo/initial_data"
DEFAULT_DB = "calipso"
DEFAULT_PORT = os.environ.get("CALIPSO_MONGO_SERVICE_PORT", 27017)
HOST = os.environ["CALIPSO_MONGO_SERVICE_HOST"]
DB_USER = os.environ["CALIPSO_MONGO_SERVICE_USER"]
DB_PWD = os.environ.get("CALIPSO_MONGO_SERVICE_PWD")
AUTH_DB = os.environ["CALIPSO_MONGO_SERVICE_AUTH_DB"]

STATUS_CODES = ["OK", "ERROR"]
max_connection_attempts = 5


class MongoConnector(object):
    def __init__(self, host, port, user, pwd, db):
        # Create calipso db and user if they don't exist
        base_uri = "mongodb://%s:%s/" % (host, port)
        base_client = MongoClient(base_uri, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
        if db not in base_client.database_names():
            new_db = base_client[db]
            new_db.add_user(user, pwd)
        base_client.close()

        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db

        self.uri = None
        self.client = None
        self.database = None
        self.connect()

    def connect(self):
        self.disconnect()
        self.uri = "mongodb://%s:%s@%s:%s/%s" % (quote_plus(self.user), quote_plus(self.pwd),
                                                 self.host, self.port, self.db)
        self.client = MongoClient(self.uri, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
        self.database = self.client[self.db]

    def disconnect(self):
        if self.client:
            print("Disconnecting from mongo...")
            self.client.close()
            self.client = None

    def drop_collection(self, name):
        self.database[name].drop()

    def find(self, collection, query=None):
        return self.database[collection].find(query)

    def find_one(self, collection, query=None):
        return self.database[collection].find_one(query)

    def insert(self, collection, docs):
        return self.database[collection].insert(docs)

    def update(self, collection, spec, doc, upsert=False):
        return self.database[collection].update(spec, doc, upsert=upsert)

    def collection_exists(self, name):
        return name in self.database.collection_names()

    def create_collection(self, name):
        return self.database.create_collection(name)

    def insert_collection(self, name, file_name=None):
        file_name = "%s.json" % (file_name if file_name else name)
        with open(os.path.join(INITIAL_DATA_PATH, file_name)) as f:
            data = json.load(f)
            if self.collection_exists(name):
                self.drop_collection(name)

            if data:
                doc_ids = self.insert(name, data)
                doc_count = len(doc_ids) if isinstance(doc_ids, list) else 1
                print("Inserted '%s' collection in db. Documents inserted: %s" % (name, doc_count))
            else:
                self.create_collection(name)
                print("Inserted empty '%s' collection in db" % (name,))

    def change_password(self, new_pwd):
        print("Changing password for user '%s'" % self.user)
        if not new_pwd:
            print("New password is empty")
        elif new_pwd == self.pwd:
            print("Passwords are identical")
        else:
            self.database.add_user(self.user, new_pwd)
            self.pwd = new_pwd
            self.connect()
            print("Password for user '%s' succesfully changed" % self.user)


def backoff(i):
    return 2 ** (i - 1)


# Exit with a pre-formatted message
def _exit(status_code, exit_code=None):
    # check STATUS_CODES for appropriate status texts
    print("Status code: %s" % STATUS_CODES[status_code])
    exit(exit_code if exit_code is not None else status_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--db_name",
                        help="Database name (default={})".format(DEFAULT_DB),
                        type=str,
                        default=DEFAULT_DB,
                        required=False)
    parser.add_argument("-p", "--port",
                        help="Port for the MongoDB daemon (default={})".format(DEFAULT_PORT),
                        type=int,
                        default=DEFAULT_PORT,
                        required=False)
    args = parser.parse_args()

    attempt = 1
    while True:
        try:
            mongo_connector = MongoConnector(HOST, args.port, DB_USER, DB_PWD, args.db_name)
            break
        except:
            traceback.print_exc()
            if attempt >= max_connection_attempts:
                raise ValueError("Failed to connect to mongod. Tried %s times" % attempt)
            attempt += 1
            print("Waiting for mongod to come online... Attempt #%s" % attempt)
            time.sleep(backoff(attempt))

    environments_collection = mongo_connector.database['environments_config']
    if environments_collection.count() > 0:
        print("Database and at least one environment already exist, skipping data setup...")
    else:
        for collection_name in ("api_tokens", "attributes_for_hover_on_data", "clique_constraints",
                                "clique_types", "cliques", "connection_tests", "constants",
                                "environments_config", "environment_options", "inventory", "link_types",
                                "links", "messages", "meteor_accounts_loginServiceConfiguration",
                                "monitoring_config", "monitoring_config_templates",
                                "network_agent_types", "roles", "scans", "scheduled_scans",
                                "statistics", "supported_environments", "user_settings", "users"):
            mongo_connector.insert_collection(collection_name)

    mongo_connector.disconnect()
    print("Initial data setup finished")
    _exit(0)


