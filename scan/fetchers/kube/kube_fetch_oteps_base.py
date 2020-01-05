###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import abc

from base.fetcher import Fetcher
from base.utils.constants import EnvironmentFeatures
from base.utils.inventory_mgr import InventoryMgr


class KubeFetchOtepsBase(Fetcher, metaclass=abc.ABCMeta):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def get_ports(self, host: str, ip: str, overlay_type: str) -> list:
        ports = []
        existing_oteps = self.inv.get_by_field(self.env, 'otep')
        for other_otep in existing_oteps:
            port = self.get_port(overlay_type, ip, other_otep['ip_address'],
                                 other_otep['host'])
            ports.append(port)
            self.add_port_to_other_otep(other_otep, ip, host)
        return ports

    def add_port_to_other_otep(self, other_otep: dict, local_ip: str,
                               local_host: str):
        port_in_other = self.get_port(other_otep['overlay_type'],
                                      other_otep['ip_address'],
                                      local_ip, local_host)
        other_ports = other_otep.get('ports', [])
        if not next((p for p in other_ports if p.get('name') == port_in_other['name']), None):
            other_ports.append(port_in_other)
        other_otep['ports'] = other_ports
        self.inv.set(other_otep)
        # repeat call to create_setup() as initial call
        # did not include this port
        if self.inv.is_feature_supported(self.env,
                                         EnvironmentFeatures.MONITORING):
            self.inv.monitoring_setup_manager.create_setup(other_otep)

    @classmethod
    @abc.abstractmethod
    def get_port(cls, overlay_type: str, local_ip: str,
                 remote_ip: str, remote_host: str) -> dict:
        return {}
