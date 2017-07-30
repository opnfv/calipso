###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
DB_CONFIG = {
            "host": "10.56.20.239",
            "name": "mysql",
            "pwd": "102QreDdiD5sKcvNf9qbHrmr",
            "port": 3307.0,
            "user": "root",
            "schema": "nova"
        }

QUERY_WITHOUT_ID = """
              SELECT id, name
              FROM nova.aggregates
              WHERE deleted = 0
            """

QUERY_WITH_ID = """
      SELECT CONCAT('aggregate-', a.name, '-', host) AS id, host AS name
      FROM nova.aggregate_hosts ah
        JOIN nova.aggregates a ON a.id = ah.aggregate_id
      WHERE ah.deleted = 0 AND aggregate_id = %s
    """

ID = "2"
OBJECT_TYPE = "host aggregate"

OBJECTS_LIST = [
    {
        "id": 1,
        "name": "osdna-agg"
    }
]
