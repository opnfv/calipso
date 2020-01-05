###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
# handle monitoring event for OTEP objects

from monitoring.handlers.monitoring_check_handler import MonitoringCheckHandler


class HandleOtep(MonitoringCheckHandler):

    def __init__(self, args):
        super().__init__(args)

    def handle(self, id, check_result):
        object_id = id[:id.index('_')]
        port_id = id[id.index('_')+1:]
        doc = self.doc_by_id(object_id)
        if not doc:
            return 1
        ports = doc['ports']
        port = ports[port_id]
        if not port:
            self.log.error('Port not found: ' + port_id)
            return 1
        status = check_result['status']
        port['status'] = self.get_label_for_status(status)
        port['status_value'] = status
        port['status_text'] = check_result['output']

        # set object status based on overall state of ports
        status_list = [p['status'] for p in ports.values() if 'status' in p]
        # OTEP overall status:
        # - Critical if no port is OK
        # - Warning if some ports not OK
        # - otherwise OK
        status = \
            2 if 'OK' not in status_list \
            else 1 if 'Critical' in status_list or 'Warning' in status_list \
            else 0
        self.set_doc_status(doc, status, None, self.check_ts(check_result))
        self.keep_message(doc, check_result)
        return status
