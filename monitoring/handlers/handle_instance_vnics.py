###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from time import strftime

from monitoring.handlers.monitoring_check_handler import MonitoringCheckHandler


class HandleInstanceVnics(MonitoringCheckHandler):
    def handle(self, object_id, check_result):
        doc = self.doc_by_id(object_id)
        if not doc:
            self.log.error('unable to find instance with id={}'.format(object_id))
            return 1
        doc['vnics_status'] = check_result['status']
        doc['vnics_status_text'] = check_result['output']
        doc['vnics_status_timestamp'] = strftime(self.TIME_FORMAT,
                                                 self.check_ts(check_result))
        self.inv.set(doc)
        return check_result['status']
