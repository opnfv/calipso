###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from monitoring.setup.monitoring_check_handler import MonitoringCheckHandler


class MonitoringSimpleObject(MonitoringCheckHandler):

    def __init__(self, env):
        super().__init__(env)

    # add monitoring setup for remote host
    def setup(self, type: str, o: dict, values: dict = None):
        if not values:
            values = {}
        values['objtype'] = type
        objid = values.get('objid', o['id'])
        values['objid'] = self.encode_special_characters(objid)
        self.create_monitoring_for_object(o, values)
