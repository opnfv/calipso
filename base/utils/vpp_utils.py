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

VPPCTL_IF_HEADER_REGEX = re.compile("^(\S+)\s+(\d+)\s+(up|down)\s+(\S+)$")


def parse_hw_interfaces(vppctl_lines):
    interfaces = []
    current = {}
    for line in vppctl_lines:
        line_parts = [lp.strip() for lp in line.split()]
        if not line_parts:
            continue

        header_match = re.match(VPPCTL_IF_HEADER_REGEX, line)
        if header_match:
            if current.get('name'):
                interfaces.append(current)

            groups = header_match.groups()
            current = {
                'name': groups[0],
                'id': groups[1],
                'state': groups[2],
                'hardware': groups[3]
            }

        if len(line_parts) > 2 and line_parts[0] == "Ethernet" and line_parts[1] == "address":
            current["mac_address"] = line_parts[2]

    if current:
        interfaces.append(current)

    return interfaces
