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

class HandlePnic(MonitoringCheckHandler):

  def __init__(self, args):
    super().__init__(args)

  def handle(self, id, check_result):
    object_id = id[:id.index('-')]
    mac = id[id.index('-')+1:]
    mac_address = '%s:%s:%s:%s:%s:%s' % \
      (mac[0:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:12])
    object_id += '-' + mac_address
    doc = self.doc_by_id(object_id)
    if not doc:
      return 1
    self.keep_result(doc, check_result)
    return check_result['status']
