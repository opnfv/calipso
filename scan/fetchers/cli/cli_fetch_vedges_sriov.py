###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re

from base.utils.inventory_mgr import InventoryMgr

from scan.fetchers.cli.cli_fetcher import CliFetcher


class CliFetchVedgesSriov(CliFetcher):
    VF_REGEX = re.compile("vf\s+(?P<vf>\d+)\s+mac\s+(?P<mac_address>([0-9a-f]{2}[:-]){5}[0-9a-f]{2}),"
                          "(\s+vlan\s+(?P<vlan>\d+),)?"
                          "(\s+spoof checking\s+(?P<spoof_checking>\w+),)?"
                          "(\s+link-state\s+(?P<link_state>\w+),)?"
                          "(\s+trust\s+(?P<trust>\w+))?")

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def get(self, parent_id):
        host_id = parent_id.replace('-vedges', '')

        network_agents = self.inv.find({"environment": self.get_env(),
                                        "type": "network_agent",
                                        "agent_type": "NIC Switch agent",
                                        "host": host_id})

        vedges = []
        for agent in network_agents:
            vedge = {
                "id": "{}-SRIOV".format(host_id),
                "host": host_id,
                "vedge_type": "SRIOV",
                "parent_type": "vedges_folder",
                "parent_id": "{}-vedges".format(host_id),
                "ports": [],
            }

            for field in ("agent_type", "description", "heartbeat_timestamp", "show_in_tree", "load",
                          "admin_state_up", "topic", "configurations", "availability_zone", "binary",
                          "resource_versions"):
                vedge[field] = agent.get(field)

            for port_id, mapping in agent.get("configurations", {}).get("device_mappings", {}).items():
                port = {
                    "id": port_id,
                    "name": mapping[0] if mapping else None,
                    "internal": False,
                    "VFs": []
                }

                if not mapping:
                    continue

                ip_link_output = self.run_fetch_lines("ip -d link show {}".format(mapping[0]), host_id)
                for line in ip_link_output:
                    vf_match = self.VF_REGEX.match(line.strip().lower())
                    if not vf_match:
                        continue

                    port["VFs"].append(vf_match.groupdict())

                vedge["ports"].append(port)

            vedges.append(vedge)

        return vedges





