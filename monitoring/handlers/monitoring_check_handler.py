###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
# handle monitoring event
import datetime
import sys
from time import gmtime, strftime

from bson import ObjectId

from base.messages.message import Message
from base.utils.configuration import Configuration
from base.utils.inventory_mgr import InventoryMgr
from base.utils.logging.full_logger import FullLogger
from base.utils.special_char_converter import SpecialCharConverter

SOURCE_SYSTEM = 'Sensu'
ERROR_LEVEL = ['info', 'warn', 'error']


class MonitoringCheckHandler(SpecialCharConverter):
    status_labels = {}
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S %Z'

    def __init__(self, args):
        super().__init__()
        self.log = FullLogger(env=args.env, level=args.loglevel)
        self.env = args.env
        try:
            self.conf = Configuration(args.mongo_config)
            self.inv = InventoryMgr()
            self.inv.log.set_loglevel(args.loglevel)
            self.inv.set_collections(args.inventory)
            self.status_labels = self.get_status_labels()
        except FileNotFoundError:
            sys.exit(1)

    def get_status_labels(self):
        statuses_name_search = {'name': 'monitoring_check_statuses'}
        labels_data = self.inv.find_one(search=statuses_name_search,
                                        collection='constants')
        if not isinstance(labels_data, dict) or 'data' not in labels_data:
            return ''
        labels = {}
        for status_data in labels_data['data']:
            if not isinstance(status_data, dict):
                continue
            val = int(status_data['value'])
            label = status_data['label']
            labels[val] = label
        return labels

    def get_label_for_status(self, status: int) -> str:
        if status not in self.status_labels.keys():
            return ''
        return self.status_labels.get(status, '')

    def doc_by_id(self, object_id):
        doc = self.inv.get_by_id(self.env, object_id)
        if not doc:
            self.log.warn('No matching object found with ID: ' + object_id)
        return doc

    def doc_by_db_id(self, db_id, coll_name=None):
        coll = self.inv.collections[coll_name] if coll_name else None
        doc = self.inv.find({'_id': ObjectId(db_id)},
                            get_single=True, collection=coll)
        if not doc:
            self.log.warn('No matching object found with DB ID: ' + db_id)
        return doc

    def set_doc_status(self, doc, status, status_text, timestamp):
        doc['status_value'] = status if isinstance(status, int) \
            else status
        doc['status'] = self.get_label_for_status(status) \
            if isinstance(status, int) \
            else status
        if status_text:
            doc['status_text'] = status_text
        doc['status_timestamp'] = strftime(self.TIME_FORMAT, timestamp)
        if 'link_type' in doc:
            self.inv.write_link(doc)
        elif 'type' in doc:
            self.inv.set(doc)
            # for some reason, in some cases the set() does not take effect
            # unless we fetch the same record again from the DB
            doc_in_db = self.doc_by_db_id(doc.get('_id', ''))
            if not doc_in_db:
                self.log.error('set_doc_status: could not find doc in DB')

    @staticmethod
    def check_ts(check_result):
        return gmtime(check_result['executed'])

    def keep_result(self, doc, check_result, add_message=True):
        status = check_result['status']
        ts = self.check_ts(check_result)
        self.set_doc_status(doc, status, check_result['output'], ts)
        if add_message:
            self.keep_message(doc, check_result)

    def keep_message(self, doc, check_result, error_level=None):
        is_link = 'link_type' in doc
        msg_id = check_result['id']
        obj_id = 'link_{}_{}'.format(doc['source_id'], doc['target_id']) \
            if is_link \
            else doc['id']
        obj_type = 'link_{}'.format(doc['link_type']) if is_link else \
            doc['type']
        display_context = obj_id if is_link \
            else doc['network_id'] if doc['type'] == 'port' else doc['id']
        level = error_level if error_level\
            else ERROR_LEVEL[check_result['status']]
        dt = datetime.datetime.utcfromtimestamp(check_result['executed'])
        message = Message(msg_id=msg_id, env=self.env, source=SOURCE_SYSTEM,
                          object_id=obj_id, object_type=obj_type,
                          display_context=display_context, level=level,
                          msg=check_result, ts=dt)
        collection = self.inv.collections['messages']
        collection.insert_one(message.get())
