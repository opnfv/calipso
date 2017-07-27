###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re

from discover.fetchers.cli.cli_fetch_vconnectors import CliFetchVconnectors


class CliFetchVconnectorsOvs(CliFetchVconnectors):
    def __init__(self):
        super().__init__()

    def get_vconnectors(self, host):
        host_id = host['id']
        lines = self.run_fetch_lines("brctl show", host_id)
        headers = ["bridge_name", "bridge_id", "stp_enabled", "interfaces"]
        headers_count = len(headers)
        # since we hard-coded the headers list, remove the headers line
        del lines[:1]

        # intefaces can spill to next line - need to detect that and add
        # them to the end of the previous line for our procesing
        fixed_lines = self.merge_ws_spillover_lines(lines)

        results = self.parse_cmd_result_with_whitespace(fixed_lines, headers, False)
        ret = []
        for doc in results:
            doc["name"] = doc.pop("bridge_name")
            doc["id"] = doc["name"] + "-" +  doc.pop("bridge_id")
            doc["host"] = host_id
            doc["connector_type"] = "bridge"
            if "interfaces" in doc:
                interfaces = {}
                interface_names = doc["interfaces"].split(",")
                for interface_name in interface_names:
                    # find MAC address for this interface from ports list
                    port_id_prefix = interface_name[3:]
                    port = self.inv.find_items({
                        "environment": self.get_env(),
                        "type": "port",
                        "binding:host_id": host_id,
                        "id": {"$regex": r"^" + re.escape(port_id_prefix)}
                    }, get_single=True)
                    mac_address = '' if not port else port['mac_address']
                    interface = {'name': interface_name, 'mac_address': mac_address}
                    interfaces[interface_name] = interface
                doc["interfaces"] = interfaces
                doc['interfaces_names'] = list(interfaces.keys())
                ret.append(doc)
        return ret
