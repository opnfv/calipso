###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from scan.fetchers.db.db_access import DbAccess


class DbFetchAvailabilityZones(DbAccess):

    def get(self, id):
        query = """
      SELECT DISTINCT availability_zone,
        availability_zone AS id, COUNT(DISTINCT host) AS descendants
      FROM nova.instances
      WHERE availability_zone IS NOT NULL
      GROUP BY availability_zone
    """
        return self.get_objects_list(query, "availability zone")
