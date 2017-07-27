###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetcher import Fetcher
##old stuff
class FetchHostObjectTypes(Fetcher):
  
  
  def get(self, parent):
    ret = {
      "type": "host_object_type",
      "id": "",
      "parent": parent,
      "rows": [
        {"id": "instances_root", "text": "Instances", "descendants": 1},
        {"id": "networks_root", "text": "Networks", "descendants": 1},
        {"id": "pnics_root", "text": "pNICs", "descendants": 1},
        {"id": "vservices_root", "text": "vServices", "descendants": 1}
      ]
    }
    return ret

    ## old/moved

