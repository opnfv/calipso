###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from monitoring.setup.monitoring_check_handler import MonitoringCheckHandler


class MonitoringOtep(MonitoringCheckHandler):

    def __init__(self, env):
        super().__init__(env)

    # add monitoring setup for remote host
    def create_setup(self, o):
        if o['ports']:
            for port in o['ports'].values():
                self.create_monitoring_for_otep_port(o, port)

    def create_monitoring_for_otep_port(self, o, port):
        if port['type'] not in ['vxlan', 'gre']:
            return  # we only handle vxlan and gre
        opt = port['options']
        values = {
            "objtype": "otep",
            "objid": o['id'],
            "portid": port['name'],
            "otep_src_ip": opt['local_ip'],
            "otep_dest_ip": opt['remote_ip']}
        self.create_monitoring_for_object(o, values)
