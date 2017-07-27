###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
# handle monitoring event for VPP vEdge objects

from monitoring.handlers.monitoring_check_handler import MonitoringCheckHandler


class HandlePnicVpp(MonitoringCheckHandler):

    def __init__(self, args):
        super().__init__(args)

    def handle(self, id, check_result):
        id = self.decode_special_characters(id)
        pnic = self.doc_by_id(id)
        if not pnic:
            return 1
        self.keep_result(pnic, check_result)
        # in vEdge object in corresponding port name, set attributes:
        # "status", "status_timestamp", "status_text"
        return check_result['status']
