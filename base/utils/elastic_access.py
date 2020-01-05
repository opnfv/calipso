###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import datetime
import time

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from base.utils.data_access_base import DataAccessBase
from base.utils.inventory_mgr import InventoryMgr
from base.utils.string_utils import stringify_doc


class ElasticAccess(DataAccessBase):
    default_conf_file = '/local_dir/es_access.conf'

    REQUIRED_ENV_VARIABLES = {
        'host': 'CALIPSO_ELASTIC_SERVICE_HOST',
        'port': 'CALIPSO_ELASTIC_SERVICE_PORT'
    }
    OPTIONAL_ENV_VARIABLES = {}

    LOG_FILENAME = 'es_access.log'
    PROJECTIONS = {  # TODO
        'inventory': ['_id', 'id', 'type', 'environment'],
        'links': [],
        'cliques': []
    }
    TREE_ROOT_ID = 'root'
    CONNECTION_RETRIES = 10

    def __init__(self, bulk_chunk_size=1000):
        super().__init__()
        self.inv = InventoryMgr()

        self.bulk_chunk_size = bulk_chunk_size
        self.connection_params = {}
        self.connection = None

    @staticmethod
    def connection_backoff(i):
        return i  # Linear backoff

    @property
    def is_connected(self):
        return self.connection is not None and self.connection.ping()

    def get_connection_text(self):
        src_text = super().get_connection_text()
        if self.is_connected:
            conn_text = "{} is connected to {}:{}".format(self.__class__.__name__,
                                                          self.connection_params.get('host'),
                                                          self.connection_params.get('port'))
        else:
            conn_text = "{} is not connected".format(self.__class__.__name__)
        return "{}. {}".format(src_text, conn_text)

    def get_connection_parameters(self):
        try:
            return self._get_connection_parameters()
        except Exception as e:
            self.log.warning("Failed to connect to ElasticSearch. Error: {}".format(e))
            return {}

    def connect(self, retries=CONNECTION_RETRIES):
        connection_params = self.get_connection_parameters()
        if not connection_params or (connection_params == self.connection_params and self.is_connected):
            return

        self.connection_params = connection_params

        connection = Elasticsearch([self.connection_params])

        attempt = 1
        while True:
            if connection.ping():
                self.log.info("Successfully connected to Elasticsearch at {}:{}".format(self.connection_params['host'],
                                                                                        self.connection_params['port']))
                self.connection = connection
                break
            else:
                fail_msg = "Failed to connect to Elasticsearch at {}:{}".format(self.connection_params['host'],
                                                                                self.connection_params['port'])
                self.connection = None
                if attempt <= retries + 1:
                    backoff = self.connection_backoff(attempt)
                    self.log.info("{}. Retrying after {} seconds".format(fail_msg, backoff))
                    time.sleep(backoff)
                    attempt += 1
                    continue
                raise ConnectionError(fail_msg)

    def create_index(self, index_name, settings=None, delete_if_exists=False):
        if settings is None:
            settings = {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1,
                    "index.mapping.total_fields.limit": 2000
                }
            }

        if self.connection.indices.exists(index_name):
            if not delete_if_exists:
                return False
            self.connection.indices.delete(index=index_name, ignore=[400, 404])

        self.connection.indices.create(index=index_name, ignore=[400, 404], body=settings)
        self.log.info('Created Index {}'.format(index_name))
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

    def dump_collections(self, env, projections=None):
        if not projections:
            projections = ElasticAccess.PROJECTIONS

        actions = []
        for col, projection in projections.items():
            date = datetime.datetime.now().strftime("%Y.%m.%d")
            index_name = 'calipso-{}-{}'.format(col, date)
            self.create_index(index_name)
            self.delete_documents_by_env(index_name, env)

            for doc in self.inv.find({'environment': env}, collection=col):
                stringify_doc(doc)
                actions.append({
                    '_op_type': 'index',
                    '_index': index_name,
                    '_id': doc['_id'],
                    'doc': doc  # TODO: use projections
                })

        ok, errors = bulk(self.connection, actions, stats_only=True, raise_on_error=False, chunk_size=self.bulk_chunk_size)
        self.log.info("Successfully indexed {} documents to Elasticsearch, errors: {}".format(ok, errors))

    def dump_tree(self, env):
        data_list = [
            {
                'id': ElasticAccess.TREE_ROOT_ID,
                'name': 'environments'
            }, {
                'id': "{}:{}".format(env, env),
                'name': env,
                'environment': env,
                'parent': ElasticAccess.TREE_ROOT_ID
            }
        ]

        env_inventory = self.inv.find({'environment': env})
        if not env_inventory:
            self.log.warning("No inventory objects found for environment '{}'".format(env))
            return
        else:
            last_scanned = env_inventory[-1].get('last_scanned')

        for doc in env_inventory:
            data_list.append({
                'id': "{}:{}".format(env, doc['id']),
                'name': doc['name'],
                'parent': "{}:{}".format(env, doc['parent_id'] if env else None),
                'type': doc['type'],
                'environment': env
            })

        index_name = 'calipso-tree-{}'.format(datetime.datetime.now().strftime("%Y.%m.%d"))
        doc_id = '1'

        doc = self.connection.get(index_name, doc_id, ignore=[400, 404])
        if doc and doc.get('found', False) is True:
            for item in doc.get('_source', {}).get('doc', []):
                item_env = item.get('environment')
                if item_env and item_env != env:
                    data_list.append(item)

        # TODO: handle response
        # ok, errors = self.connection.index(index_name, {'doc': data_list})
        # self.log.info("Successfully indexed {} documents to Elasticsearch index '{}', errors: {}".format(
        #     ok, index_name, errors)
        # )
        env_doc = self.inv.find_one({'name': env}, collection='environments_config')
        if env_doc.get('last_scanned'):
            last_scanned = env_doc['last_scanned']

        self.connection.index(index_name, {'last_scanned': last_scanned, 'doc': data_list}, id=doc_id)
