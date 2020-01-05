###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json
from datetime import datetime
import time
import argparse
from bson import ObjectId

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from calipso_replication_client import MongoConnector


class ESIndex(object):
    def __init__(self, name, projections=None, shards=1, replicas=1, field_limit=1000):
        self.name = name
        self.projections = projections if projections and isinstance(projections, list) else []
        self.shards = shards
        self.replicas = replicas
        self.field_limit = field_limit

    @property
    def settings(self):
        return {
            "settings": {
                "number_of_shards": self.shards,
                "number_of_replicas": self.replicas,
                "index.mapping.total_fields.limit": self.field_limit
            }
        }

    @property
    def full_name(self):
        return "-".join(("calipso", self.name, datetime.now().strftime("%Y.%m.%d")))


INDICES = [
    ESIndex(name="inventory", field_limit=2500),
    ESIndex(name="links", field_limit=200),
    ESIndex(name="cliques", field_limit=200),
]


class ElasticClient(object):

    LOG_FILENAME = 'es_access.log'
    PROJECTIONS = {  # TODO
        'inventory': ['_id', 'id', 'type', 'environment'],
        'links': [],
        'cliques': []
    }
    TREE_ROOT_ID = 'root'
    TREE_DOC_ID = '1'
    CONNECTION_RETRIES = 10

    def __init__(self, host, port, user, pwd, db, bulk_chunk_size=1000, db_label="central DB"):
        self.bulk_chunk_size = bulk_chunk_size
        self.connection = None
        self.inventory_collection = None
        self.inventory_collection_name = None
        self.collections = {}
        self.mongo = MongoConnector(host, port, user, pwd, db, db_label)
        self.stringify_map = {
            ObjectId: self.stringify_object_id,
            datetime: self.stringify_datetime
        }

    @staticmethod
    def stringify_datetime(dt):
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

    @staticmethod
    def stringify_object_id(object_id):
        return str(object_id)

    def stringify_object_values_by_type(self, obj, object_type):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, object_type):
                    obj[key] = self.stringify_map[object_type](value)
                else:
                    self.stringify_object_values_by_type(value, object_type)
        elif isinstance(obj, list):
            for index, value in enumerate(obj):
                if isinstance(value, object_type):
                    obj[index] = self.stringify_map[object_type](value)
                else:
                    self.stringify_object_values_by_type(value, object_type)

    def stringify_object_values_by_types(self, obj, object_types):
        for object_type in object_types:
            self.stringify_object_values_by_type(obj, object_type)

    def stringify_doc(self, doc):
        self.stringify_object_values_by_types(doc, self.stringify_map.keys())

    @staticmethod
    def connection_backoff(i):
        return i  # Linear backoff

    @property
    def is_connected(self):
        return self.connection is not None and self.connection.ping()

    def connect(self, conn_params):
        connection = Elasticsearch([conn_params])
        attempt = 1
        while True:
            if connection.ping():
                print("Successfully connected to Elasticsearch at {}:{}\n".format(conn_params['host'],
                                                                                conn_params['port']))
                self.connection = connection
                break
            else:
                fail_msg = "Failed to connect to Elasticsearch at {}:{}\n".format(conn_params['host'],
                                                                                conn_params['port'])
                if attempt <= self.CONNECTION_RETRIES:
                    backoff = self.connection_backoff(attempt)
                    print("{}. Retrying after {} seconds\n".format(fail_msg, backoff))
                    time.sleep(backoff)
                    attempt += 1
                    continue
                raise ConnectionError(fail_msg)
        self.connection = connection

    def create_index(self, index, delete_if_exists=False):
        if self.connection.indices.exists(index.full_name):
            if not delete_if_exists:
                return False
            self.connection.indices.delete(index=index.full_name, ignore=[400, 404])

        self.connection.indices.create(index=index.full_name, ignore=[400, 404], body=index.settings)
        print('Created Index {}'.format(index.full_name))
        return True

    def delete_documents_by_env(self, index, env):
        query = {
          "query": {
            "match": {
              "environment": env
            }
          }
        }
        self.connection.delete_by_query(index, query)

    def dump_collections(self, env=None):
        actions = []

        for index in INDICES:
            self.create_index(index, delete_if_exists=False if env else True)
            if env:
                self.delete_documents_by_env(index.full_name, env)

            docs = self.mongo.find_all(collection=index.name, env=env)
            for doc in docs:
                self.stringify_doc(doc)
                actions.append({
                    '_op_type': 'index',
                    '_index': index.full_name,
                    '_id': doc['_id'],
                    'doc': doc  # TODO: use projections
                })
            self.connection.indices.refresh(index=index.full_name)
            print("Indexing {} docs to '{}' collection...\n".format(len(docs), index.full_name))

        ok, errors = bulk(self.connection, actions, raise_on_error=False,
                          chunk_size=self.bulk_chunk_size, request_timeout=30)
        print("Successfully indexed {} documents to Elasticsearch, errors: {}\n".format(ok, json.dumps(errors)))

    def _get_tree_for_env(self, env):
        return [{
            'id': "{}:{}".format(env, doc['id']),
            'name': doc['name'],
            'parent': "{}:{}".format(env, doc['parent_id']),
            'type': doc['type'],
            'environment': env
        } for doc in self.mongo.find_all(collection="inventory", env=env)]

    def dump_tree(self, env=None):
        print("Creating VEGA tree model for visualizations...")

        index_name = 'calipso-tree-{}'.format(datetime.now().strftime("%Y.%m.%d"))
        data_list = [{
            'id': self.TREE_ROOT_ID,
            'name': "enviroments",
        }]
        if env:
            data_list.append({
                'id': "{}:{}".format(env, env),
                'name': env,
                'environment': env,
                'parent': ElasticClient.TREE_ROOT_ID
            })
            data_list.extend(self._get_tree_for_env(env))
            current_tree_doc = self.connection.get(index_name, self.TREE_DOC_ID, ignore=[400, 404])
            if current_tree_doc and current_tree_doc.get('found', False) is True:
                for item in current_tree_doc.get('_source', {}).get('doc', []):
                    item_env = item.get('environment')
                    if item_env and item_env != env:
                        data_list.append(item)
        else:
            for env in self.mongo.find_all(collection="environments_config"):
                env_name = env['name']
                data_list.append({
                    'id': "{}:{}".format(env_name, env_name),
                    'name': env_name,
                    'environment': env_name,
                    'parent': ElasticClient.TREE_ROOT_ID
                })
                data_list.extend(self._get_tree_for_env(env_name))

        # TODO: handle response
        # ok, errors = self.connection.index(index_name, {'doc': data_list})
        # self.log.info("Successfully indexed {} documents to Elasticsearch index '{}', errors: {}".format(
        #     ok, index_name, errors)
        # )
        tree_time = datetime.now()
        self.connection.index(index=index_name, body={'last_scanned': tree_time, 'doc': data_list},
                              id=self.TREE_DOC_ID, request_timeout=30)
        self.connection.indices.refresh(index=index_name)
        print("Successfully created VEGA tree model with {} nodes\n".format(len(data_list)))


def fatal(err):
    print(err)
    exit(1)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--es_server",
                        help="FQDN or IP address of the ElasticSearch Server"
                             " (default=localhost)",
                        type=str,
                        default="localhost",
                        required=False)
    parser.add_argument("--m_server",
                        help="FQDN or IP address of the MongoDB Server"
                             " (default=localhost)",
                        type=str,
                        default="localhost",
                        required=False)
    parser.add_argument("--es_port",
                        help="TCP Port exposed on the ElasticSearch Server "
                             " (default=9200)",
                        type=int,
                        default=9200,
                        required=False)
    parser.add_argument("--m_port",
                        help="TCP Port exposed on the MongoDB Server "
                             " (default=27017)",
                        type=int,
                        default=27017,
                        required=False)
    parser.add_argument("-e", "--environment",
                        help="specify environment(pod) name configured in MongoDB"
                             " (default=None)",
                        type=str,
                        default=None,
                        required=False)
    parser.add_argument("--m_user",
                        help="specify username with calipso access privileges on MongoDB"
                             " (default=calipso)",
                        type=str,
                        default="calipso",
                        required=False)
    parser.add_argument("--m_pwd",
                        help="specify password for m_user on MongoDB"
                             " (default=calipso_default)",
                        type=str,
                        default="calipso_default",
                        required=False)
    parser.add_argument("--version",
                        help="get a reply back with calipso_elastic_client version",
                        action='version',
                        default=None,
                        version='%(prog)s version: 0.6.8')

    args = parser.parse_args()
    es = ElasticClient(args.m_server, args.m_port, args.m_user, args.m_pwd, "calipso")
    es_conn_params = {"host": args.es_server, "port": args.es_port}
    es.connect(es_conn_params)
    es.dump_collections(args.environment)
    es.dump_tree(args.environment)
    exit(0)


if __name__ == "__main__":
    run()
