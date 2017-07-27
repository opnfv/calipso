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

from discover.fetchers.db.db_access import DbAccess


class DbFetchAZNetworkHosts(DbAccess):

  def get(self, id):
    query = """
      SELECT DISTINCT host, host AS id, configurations
      FROM neutron.agents
      WHERE agent_type = 'Metadata agent'
    """
    results = self.get_objects_list(query, "host")
    for r in results:
      self.set_host_details(r)
    return results

  def set_host_details(self, r):
    config = json.loads(r["configurations"])
    r["ip_address"] = config["nova_metadata_ip"]
    r["host_type"] = "Network Node"
