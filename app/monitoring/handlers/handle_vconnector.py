###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
# handle monitoring event for pNIC objects

from monitoring.handlers.monitoring_check_handler import MonitoringCheckHandler
from utils.special_char_converter import SpecialCharConverter


class HandleVconnector(MonitoringCheckHandler):

    def handle(self, obj_id, check_result):
        object_id = obj_id[:obj_id.index('-')]
        mac = obj_id[obj_id.index('-')+1:]
        converter = SpecialCharConverter()
        mac_address = converter.decode_special_characters(mac)
        object_id += '-' + mac_address
        doc = self.doc_by_id(object_id)
        if not doc:
            return 1
        self.keep_result(doc, check_result)
        return check_result['status']
