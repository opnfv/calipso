###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.fetchers.cli.cli_access import CliAccess
from discover.fetchers.db.db_access import DbAccess
from utils.inventory_mgr import InventoryMgr


class CliFetchOtepsLxb(CliAccess, DbAccess):

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def get(self, parent_id):
        vconnector = self.inv.get_by_id(self.get_env(), parent_id)
        if not vconnector:
            return []
        configurations = vconnector['configurations']
        tunneling_ip = configurations['tunneling_ip']
        tunnel_types_used = configurations['tunnel_types']
        if not tunnel_types_used:
            return []
        tunnel_type = tunnel_types_used[0]
        if not tunnel_type:
            return []
        # check only interfaces with name matching tunnel type
        ret = [i for i in vconnector['interfaces'].values()
               if i['name'].startswith(tunnel_type + '-')]
        for otep in ret:
            otep['ip_address'] = tunneling_ip
            otep['host'] = vconnector['host']
            self.get_otep_ports(otep)
            otep['id'] = otep['host'] + '-otep-' + otep['name']
            otep['name'] = otep['id']
            otep['vconnector'] = vconnector['name']
            otep['overlay_type'] = tunnel_type
            self.get_udp_port(otep)
        return ret

    """
    fetch OTEP data from CLI command 'ip -d link show'
    """
    def get_otep_ports(self, otep):
        cmd = 'ip -d link show'
        lines = self.run_fetch_lines(cmd, otep['host'])
        header_format = '[0-9]+: ' + otep['name'] + ':'
        interface_lines = self.get_section_lines(lines, header_format, '\S')
        otep['data'] = '\n'.join(interface_lines)
        regexps = [
            {'name': 'state', 're': ',UP,', 'default': 'DOWN'},
            {'name': 'mac_address', 're': '.*\slink/ether\s(\S+)\s'},
            {'name': 'mtu', 're': '.*\smtu\s(\S+)\s'},
        ]
        self.get_object_data(otep, interface_lines, regexps)
        cmd = 'bridge fdb show'
        dst_line_format = ' dev ' + otep['name'] + ' dst '
        lines = self.run_fetch_lines(cmd, otep['host'])
        lines = [l for l in lines if dst_line_format in l]
        if lines:
            l = lines[0]
            otep['bridge dst'] = l[l.index(' dst ')+5:]
        return otep

    def get_udp_port(self, otep):
        table_name = "neutron.ml2_" + otep['overlay_type'] + "_endpoints"
        results = None
        try:
            results = self.get_objects_list_for_id(
                """
                SELECT udp_port
                FROM {}
                WHERE host = %s
                """.format(table_name),
                "vedge", otep['host'])
        except Exception as e:
            self.log.error('failed to fetch UDP port for OTEP: ' + str(e))
        otep['udp_port'] = 0
        for result in results:
            otep['udp_port'] = result['udp_port']
