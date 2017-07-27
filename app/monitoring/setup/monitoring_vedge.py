###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from monitoring.setup.monitoring_simple_object import MonitoringSimpleObject


class MonitoringVedge(MonitoringSimpleObject):

    def __init__(self, env):
        super().__init__(env)

    def create_setup(self, o):
        self.setup('vedge', o)
