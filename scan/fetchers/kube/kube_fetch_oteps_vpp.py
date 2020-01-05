###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.utils.inventory_mgr import InventoryMgr
from scan.fetchers.kube.kube_fetch_oteps_base import KubeFetchOtepsBase


class KubeFetchOtepsVpp(KubeFetchOtepsBase):

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    OTEP_UDP_PORT = 8285

    def get(self, vedge_id) -> list:
        host_id = vedge_id.replace('-VPP', '') if vedge_id.endswith('-VPP') \
            else vedge_id
        host = self.inv.get_by_id(self.get_env(), host_id)
        if not host:
            self.log.error('failed to find host by ID: {}'.format(host_id))
            return []
        host_interfaces = host.get('interfaces', [])
        vpp_interface = next((interface for interface in host_interfaces if interface['name'].startswith('vpp1-')), {})
        ip_address = vpp_interface.get('IP Address', '')
        otep_mac = vpp_interface.get('mac_address')
        overlay_type = self.configuration.environment.get('type_drivers')
        doc = {
            'id': '{}-otep'.format(host_id),
            'name': '{}-otep'.format(host['name']),
            'host': host['name'],
            'parent_type': 'vedge',
            'parent_id': vedge_id,
            'ip_address': ip_address,
            'overlay_type': overlay_type,
            'overlay_mac_address': otep_mac,
            'ports': self.get_ports(host['name'], ip_address, overlay_type),
            'udp_port': self.OTEP_UDP_PORT
        }
        return [doc]

    PORT_ID_PREFIX = 'vxlan-remote-'

    @staticmethod
    def get_port_id(remote_host_id: str) -> str:
        return '{}{}'.format(KubeFetchOtepsVpp.PORT_ID_PREFIX, remote_host_id)

    @classmethod
    def get_port(cls, overlay_type: str, local_ip: str,
                 remote_ip: str, remote_host: str) -> dict:
        port_id = KubeFetchOtepsVpp.get_port_id(remote_host)
        return {
            'name': port_id,
            'type': overlay_type,
            'remote_host': remote_host,
            'interface': port_id,
            'options': {
                'local_ip': local_ip,
                'remote_ip': remote_ip
            }
        }
