###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.cli.cli_fetch_instance_vnics_base import CliFetchInstanceVnicsBase


class CliFetchInstanceVnics(CliFetchInstanceVnicsBase):
    def __init__(self):
        super().__init__()

    def set_vnic_properties(self, v, instance):
        super().set_vnic_properties(v, instance)
        v["source_bridge"] = v["source"]["@bridge"]

    def get_vnic_name(self, v, instance):
        return v["target"]["@dev"]
