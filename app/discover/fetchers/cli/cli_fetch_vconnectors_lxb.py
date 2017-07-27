###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json

from discover.fetchers.cli.cli_fetch_vconnectors_ovs import CliFetchVconnectorsOvs
from discover.fetchers.db.db_access import DbAccess


class CliFetchVconnectorsLxb(CliFetchVconnectorsOvs, DbAccess):

    def __init__(self):
        super().__init__()

    def get(self, id):
        ret = super().get(id)
        for doc in ret:
            query = """
              SELECT configurations
              FROM {}.agents
              WHERE agent_type="Linux bridge agent" AND host = %s
            """.format(self.neutron_db)
            host = doc['host']
            matches = self.get_objects_list_for_id(query, '', host)
            if not matches:
                raise ValueError('No Linux bridge agent in DB for host: {}'.format(host))
            agent = matches[0]
            doc['configurations'] = json.loads(agent['configurations'])
        return ret
