###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

from monitoring.handlers.monitoring_check_handler import MonitoringCheckHandler


class HandleInstanceVnic(MonitoringCheckHandler):
    def handle(self, object_id, check_result):
        object_id = object_id.replace("vnic_", "")
        doc = self.doc_by_id(object_id)
        if not doc:
            self.log.error('unable to find vnic with id={}'.format(object_id))
            return 1
        self.keep_result(doc, check_result)
        return check_result['status']
