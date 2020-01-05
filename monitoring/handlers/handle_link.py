###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
# handle monitoring event for links

from monitoring.handlers.monitoring_check_handler import MonitoringCheckHandler


class HandleLink(MonitoringCheckHandler):

    def __init__(self, args):
        super().__init__(args)

    def handle(self, link_id_from_check, check_result):
        # link ID from check is formatted like this:
        # <link type>_<source_id>_<target_id>
        link_type = link_id_from_check[:link_id_from_check.index('_')]
        remainder = link_id_from_check[len(link_type)+1:]
        source_id = remainder[:remainder.index('_')]
        target_id = remainder[len(source_id)+1:]
        search = {
            'link_type': link_type,
            'source_id': source_id,
            'target_id': target_id
        }
        doc = self.inv.find_items(search, collection='links', get_single=True)
        if not doc:
            return 1
        self.keep_result(doc, check_result)
        return check_result['status']
