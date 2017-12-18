###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import functools
import mysql.connector

from discover.configuration import Configuration
from discover.fetcher import Fetcher
from discover.scan_error import ScanError
from utils.string_utils import jsonify


def with_cursor(method):
    @functools.wraps(method)
    def wrap(self, *args, **kwargs):
        self.connect_to_db(DbAccess.query_count_per_con >= 25)
        DbAccess.query_count_per_con += 1
        cursor = DbAccess.conn.cursor(dictionary=True)
        try:
            res = method(self, *args, cursor=cursor, **kwargs)
            DbAccess.conn.commit()
            return res
        except:
            DbAccess.conn.rollback()
            raise
        finally:
            cursor.close()
    return wrap


class DbAccess(Fetcher):
    conn = None
    query_count_per_con = 0

    # connection timeout set to 5 seconds
    TIMEOUT = 5

    def __init__(self, mysql_config=None):
        super().__init__()
        self.config = {'mysql': mysql_config} if mysql_config \
            else Configuration()
        self.conf = self.config.get("mysql")
        self.connect_timeout = int(self.conf['connect_timeout']) \
            if 'connect_timeout' in self.conf \
            else self.TIMEOUT
        self.connect_to_db()
        self.neutron_db = self.get_neutron_db_name()

    def db_connect(self, _host, _port, _user, _pwd, _database):
        if DbAccess.conn:
            return
        try:
            connector = mysql.connector
            conn = connector.connect(host=_host, port=_port,
                                     connection_timeout=self.connect_timeout,
                                     user=_user,
                                     password=_pwd,
                                     database=_database,
                                     raise_on_warnings=True)
            DbAccess.conn = conn
            DbAccess.conn.ping(True)  # auto-reconnect if necessary
        except Exception as e:
            msg = "failed to connect to MySQL DB: {}".format(str(e))
            self.log.critical(msg)
            raise ScanError(msg)
            return
        DbAccess.query_count_per_con = 0

    @with_cursor
    def get_neutron_db_name(self, cursor=None):
        # check if DB schema 'neutron' exists
        cursor.execute('SHOW DATABASES')
        matches = [row.get('Database', '') for row in cursor
                   if 'neutron' in row.get('Database', '')]
        if not matches:
            raise ScanError('Unable to find Neutron schema in OpenStack DB')
        if len(matches) > 1:
            raise ScanError('Found multiple possible names for Neutron schema '
                            'in OpenStack DB')
        return matches[0]

    def connect_to_db(self, force=False):
        if DbAccess.conn:
            if not force:
                return
            self.log.info("DbAccess: ****** forcing reconnect, " +
                          "query count: %s ******",
                          DbAccess.query_count_per_con)
            DbAccess.conn.commit()
            DbAccess.conn.close()
            DbAccess.conn = None
        self.conf = self.config.get("mysql")
        cnf = self.conf
        pwd = cnf.get('pwd', '')
        if not pwd:
            raise ScanError('db_access: attribute pwd is missing')
        self.db_connect(cnf.get('host', ''), cnf.get('port', ''),
                        cnf.get('user', ''), pwd,
                        cnf.get('schema', 'nova'))

    @with_cursor
    def get_objects_list_for_id(self, query, object_type, object_id,
                                cursor=None):
        self.log.debug("query count: %s, running query:\n%s\n",
                       str(DbAccess.query_count_per_con), query)

        try:
            if object_id:
                cursor.execute(query, [str(object_id)])
            else:
                cursor.execute(query)
        except (AttributeError, mysql.connector.errors.OperationalError) as e:
            self.log.error(e)
            self.connect_to_db(True)
            # try again to run the query
            cursor = DbAccess.conn.cursor(dictionary=True)
            if object_id:
                cursor.execute(query, [str(object_id)])
            else:
                cursor.execute(query)

        rows = []
        for row in cursor.fetchall():
            rows.append(row)
        return rows

    def get_objects_list(self, query, object_type):
        return self.get_objects_list_for_id(query, object_type, None)

    def get_objects(self, qry, type, id):
        return jsonify(self.get_objects_list(qry, type))

    def get(self, id):
        # return list of available fetch types
        ret = {
            "description": "List of available fetch calls for this interface",
            "types": {
                "regions": "Regions of this environment",
                "projects": "Projects (tenants) of this environment",
                "availability_zones": "Availability zones",
                "aggregates": "Host aggregates",
                "aggregate_hosts": "Hosts in aggregate X (parameter: id)",
                "az_hosts": "Host in availability_zone X (parameter: id)"
            }
        }
        return jsonify(ret)

