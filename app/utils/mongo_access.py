###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import os

from pymongo import MongoClient

from utils.config_file import ConfigFile
from utils.dict_naming_converter import DictNamingConverter
from utils.logging.console_logger import ConsoleLogger
from utils.logging.file_logger import FileLogger


# Provides access to MongoDB using PyMongo library
#
# Notes on authentication:
# default config file is calipso_mongo_access.conf
# you can also specify name of file from CLI with --mongo_config


class MongoAccess(DictNamingConverter):
    client = None
    db = None
    default_conf_file = '/local_dir/calipso_mongo_access.conf'
    config_file = None

    DB_NAME = 'calipso'
    LOG_FILENAME = 'mongo_access.log'
    DEFAULT_LOG_FILE = os.path.join(os.path.abspath("."), LOG_FILENAME)

    def __init__(self):
        super().__init__()
        self.log_file = os.path.join(FileLogger.LOG_DIRECTORY,
                                     MongoAccess.LOG_FILENAME)

        try:
            self.log = FileLogger(self.log_file)
        except OSError as e:
            ConsoleLogger().warning("Couldn't use file {} for logging. "
                                    "Using default location: {}.\n"
                                    "Error: {}"
                                    .format(self.log_file,
                                            self.DEFAULT_LOG_FILE,
                                            e))

            self.log_file = self.DEFAULT_LOG_FILE
            self.log = FileLogger(self.log_file)

        self.connect_params = {}
        self.mongo_connect(self.config_file)

    def is_db_ready(self) -> bool:
        return MongoAccess.client is not None

    @staticmethod
    def set_config_file(_conf_file):
        MongoAccess.config_file = _conf_file

    def mongo_connect(self, config_file_path=""):
        if MongoAccess.client:
            return

        self.connect_params = {
            "server": "localhost",
            "port": 27017
        }

        if not config_file_path:
            config_file_path = self.default_conf_file

        try:
            config_file = ConfigFile(config_file_path)
            # read connection parameters from config file
            config_params = config_file.read_config()
            self.connect_params.update(config_params)
        except Exception as e:
            self.log.exception(e)
            raise

        self.prepare_connect_uri()
        MongoAccess.client = MongoClient(
            self.connect_params["server"],
            int(self.connect_params["port"])
        )
        MongoAccess.db = getattr(MongoAccess.client,
                                 config_params.get('auth_db', self.DB_NAME))
        MongoAccess.db.authenticate(name=self.connect_params['user'],
                                    password=self.connect_params['pwd'])
        self.log.info('Connected to MongoDB')

    def prepare_connect_uri(self):
        params = self.connect_params
        self.log.debug('connecting to MongoDB server: {}'
                       .format(params['server']))
        uri = 'mongodb://'
        if 'pwd' in params:
            uri = uri + params['user'] + ':' + params['pwd'] + '@'
        else:
            self.log.info('MongoDB credentials missing')
        uri = uri + params['server']
        if 'auth_db' in params:
            uri = uri + '/' + params['auth_db']
        self.connect_params['server'] = uri

    @staticmethod
    def update_document(collection, document, upsert=False):
        if isinstance(collection, str):
            collection = MongoAccess.db[collection]
        doc_id = document.pop('_id')
        collection.update_one({'_id': doc_id}, {'$set': document},
                              upsert=upsert)
        document['_id'] = doc_id

    @staticmethod
    def encode_dots(s):
        return s.replace(".", "[dot]")

    @staticmethod
    def decode_dots(s):
        return s.replace("[dot]", ".")

    # Mongo will not accept dot (".") in keys, or $ in start of keys
    # $ in beginning of key does not happen in OpenStack,
    # so need to translate only "." --> "[dot]"
    @staticmethod
    def encode_mongo_keys(item):
        return MongoAccess.change_dict_naming_convention(item, MongoAccess.encode_dots)

    @staticmethod
    def decode_mongo_keys(item):
        return MongoAccess.change_dict_naming_convention(item, MongoAccess.decode_dots)

    @staticmethod
    def decode_object_id(item: dict):
        return dict(item, **{"_id": str(item["_id"])}) if item and "_id" in item else item
