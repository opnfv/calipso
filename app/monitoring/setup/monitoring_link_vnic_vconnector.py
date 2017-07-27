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


class MonitoringLinkVnicVconnector(MonitoringCheckHandler):

    def __init__(self, env):
        super().__init__(env)

    # add monitoring setup for remote host
    def create_setup(self, link):
        vnic = self.inv.get_by_id(self.env, link['source_id'])
        if not vnic:
            self.log.error('could not find vnic for vnic-vconnector link')
            return
        if 'mac_address' not in vnic:
            self.log.error('could not find MAC address in vNIC: ' + vnic['id'])
            return
        vconnector = self.inv.get_by_id(self.env, link['target_id'])
        if not vnic:
            self.log.error('could not find vconnector for vnic-vconnector link')
            return
        values = {
            'linktype': 'vnic-vconnector',
            'fromobjid': self.encode_special_characters(vnic['id']),
            'toobjid': vconnector['id'],
            'bridge': vconnector['object_name'],
            'mac_address': vnic['mac_address']}
        self.create_monitoring_for_object(link, values)
