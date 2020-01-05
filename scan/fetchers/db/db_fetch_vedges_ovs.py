###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json

import re

from base.utils.inventory_mgr import InventoryMgr
from scan.fetchers.cli.cli_fetcher import CliFetcher
from scan.fetchers.db.db_access import DbAccess


class DbFetchVedgesOvs(DbAccess, CliFetcher):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()
        self.port_re = re.compile("^\s*port (\d+): ([^(]+)( \(internal\))?$")
        self.port_line_header_prefix = " " * 8 + "Port "

    def get(self, parent_id):
        host_id = parent_id[:parent_id.rindex('-')]
        results = self.get_objects_list_for_id(
            """
              SELECT *
              FROM {}.agents
              WHERE host = %s AND agent_type = 'Open vSwitch agent'
            """.format(self.neutron_db),
            "vedge", host_id)
        host = self.inv.get_by_id(self.get_env(), host_id)
        if not host:
            self.log.error("unable to find host in inventory: %s", host_id)
            return []
        host_types = host["host_type"]
        if "Network" not in host_types and "Compute" not in host_types:
            return []
        vsctl_lines = self.run_fetch_lines("ovs-vsctl show", host["id"])
        ports = self.fetch_ports(host, vsctl_lines)
        for doc in results:
            doc["vedge_type"] = "OVS"
            doc["name"] = "{}-OVS".format(doc["host"])
            doc["configurations"] = json.loads(doc["configurations"])
            if doc.get('admin_state_up') in (0, 1):
                doc['admin_state_up'] = bool(doc['admin_state_up'])
            doc["ports"] = list(ports.values())
            doc["tunnel_ports"] = self.get_overlay_tunnels(doc, vsctl_lines)
        return results

    def fetch_ports(self, host, vsctl_lines):
        host_types = host["host_type"]
        if "Network" not in host_types and "Compute" not in host_types:
            return {}
        ports = self.fetch_ports_from_dpctl(host["id"])
        self.fetch_port_tags_from_vsctl(vsctl_lines, ports)
        return ports

    def fetch_ports_from_dpctl(self, host_id):
        cmd = "ovs-dpctl show"
        lines = self.run_fetch_lines(cmd, host_id)
        ports = {}
        for l in lines:
            port_matches = self.port_re.match(l)
            if not port_matches:
                continue
            port = {}
            port_id = port_matches.group(1)
            name = port_matches.group(2)
            is_internal = port_matches.group(3) == " (internal)"
            port["internal"] = is_internal
            port["id"] = port_id
            port["name"] = name
            ports[name] = port
        return ports

    # from ovs-vsctl, fetch tags of ports
    # example format of ovs-vsctl output for a specific port:
    #        Port "tap9f94d28e-7b"
    #            tag: 5
    #            Interface "tap9f94d28e-7b"
    #                type: internal
    def fetch_port_tags_from_vsctl(self, vsctl_lines, ports):
        port = None
        for l in vsctl_lines:
            if l.startswith(self.port_line_header_prefix):
                port = None
                port_name = l[len(self.port_line_header_prefix):]
                # remove quotes from port name
                if '"' in port_name:
                    port_name = port_name[1:][:-1]
                if port_name in ports:
                    port = ports[port_name]
                continue
            if not port:
                continue
            if l.startswith(" " * 12 + "tag: "):
                port["tag"] = l[l.index(":") + 2:]
                ports[port["name"]] = port
        return ports

    def get_overlay_tunnels(self, doc, vsctl_lines):
        if doc["agent_type"] != "Open vSwitch agent":
            return {}
        if "tunneling_ip" not in doc["configurations"]:
            return {}
        if not doc["configurations"]["tunneling_ip"]:
            self.get_pnics(doc)
            return {}

        # read the 'br-tun' interface ports
        # this will be used later in the OTEP
        tunnel_bridge_header = " " * 4 + "Bridge br-tun"
        try:
            br_tun_loc = vsctl_lines.index(tunnel_bridge_header)
        except ValueError:
            return []
        lines = vsctl_lines[br_tun_loc + 1:]
        tunnel_ports = {}
        port = None
        for l in lines:
            # if we have only 4 or less spaces in the beginng,
            # the br-tun section ended so return
            if not l.startswith(" " * 5):
                break
            if l.startswith(self.port_line_header_prefix):
                if port:
                    tunnel_ports[port["name"]] = port
                name = l[len(self.port_line_header_prefix):].strip('" ')
                port = {"name": name}
            elif port and l.startswith(" " * 12 + "Interface "):
                interface = l[10 + len("Interface ") + 1:].strip('" ')
                port["interface"] = interface
            elif port and l.startswith(" " * 16):
                colon_pos = l.index(":")
                attr = l[:colon_pos].strip()
                val = l[colon_pos + 2:].strip('" ')
                if attr == "options":
                    opts = val.strip('{}')
                    val = {}
                    for opt in opts.split(", "):
                        opt_name = opt[:opt.index("=")]
                        opt_val = opt[opt.index("=") + 1:].strip('" ')
                        val[opt_name] = opt_val
                port[attr] = val
        if port:
            tunnel_ports[port["name"]] = port
        return tunnel_ports

    def get_pnics(self, vedge) -> dict:
        bridges = vedge["configurations"].get("bridge_mappings", {})
        pnics = {}
        for bridge in bridges.values():
            self.get_bridge_pnic(pnics, vedge, bridge)
        return pnics

    MIRANTIS_DIST = "Mirantis"

    def get_bridge_pnic(self, pnics: dict, vedge: dict, bridge: dict):
        cmd = "ovs-vsctl list-ifaces {}".format(bridge)
        ifaces_list_lines = self.run_fetch_lines(cmd, vedge["host"])
        env_config = self.configuration.get_env_config()
        distribution = env_config.get("distribution")
        dist_version = env_config.get("distribution_version")
        use_br_postfix = distribution == self.MIRANTIS_DIST and \
            dist_version in ["6.0", "7.0", "8.0"]
        for l in ifaces_list_lines:
            if use_br_postfix:
                br_pnic_postfix = "{}--br-".format(bridge)
                interface = l[len(br_pnic_postfix):] \
                    if l.startswith(br_pnic_postfix) \
                    else ""
            else:
                interface = l
            if interface:
                pnic = self.find_pnic_for_interface(vedge, interface)
                if pnic:
                    pnics[pnic["name"]] = pnic

    def find_pnic_for_interface(self, vedge, interface):
        # add port ID to pNIC
        pnic = self.inv.find_items({
            "environment": self.get_env(),
            "type": "host_pnic",
            "host": vedge["host"],
            "name": interface
        }, get_single=True)
        if not pnic:
            return
        vedge["pnic"] = interface
        port = next((i for i in vedge["ports"] if i['name'] == interface), None)
        if port:
            pnic["port_id"] = port.get("id", "")
            self.inv.set(pnic)
        return pnic
