###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from collections import defaultdict

import re

from base.utils.vpp_utils import parse_hw_interfaces
from scan.fetchers.cli.cli_fetch_vconnectors import CliFetchVconnectors


class CliFetchVconnectorsVpp(CliFetchVconnectors):
    def __init__(self):
        super().__init__()
        self.vconnectors = None
        self.interfaces = defaultdict(dict)
        self.interfaces_names = defaultdict(list)

    # (Regex, matching group ids)
    INTERFACE_MAPPINGS = (
        (re.compile('^(.*)\.[0-9]+$'), [0]),
    )

    @classmethod
    def clean_interface(cls, name):
        for mapping in cls.INTERFACE_MAPPINGS:
            match = re.match(mapping[0], name)
            if match:
                return ''.join(match.groups()[g] for g in mapping[1])
        return name

    def get_vconnectors(self, host):
        self.vconnectors = {}
        lines = self.run_fetch_lines("vppctl show mode", host['id'])
        is_kubernetes = self.ENV_TYPE_KUBERNETES == \
            self.configuration.environment.get('environment_type')
        self.interfaces = defaultdict(dict)
        self.interfaces_names = defaultdict(list)
        for l in lines:
            is_l2_bridge = l.startswith('l2 bridge')
            if not is_kubernetes and not is_l2_bridge:
                continue
            line_parts = l.strip().split(' ')
            name = line_parts[2 if is_l2_bridge else 1]
            bd_id = line_parts[4] if is_l2_bridge else ''
            self.add_vconnector(host=host, bd_id=bd_id)
            interface = self.get_interface_details(host, name)
            if interface:
                interface['name'] = name  # Avoid bond interface name substitution
                self.interfaces[bd_id][name] = interface
                self.interfaces_names[bd_id].append(name)

        for vconnector in self.vconnectors.values():
            vconnector['interfaces'] = list(self.interfaces[vconnector['bd_id']].values())
            vconnector['interfaces_names'] = self.interfaces_names[vconnector['bd_id']]

        return list(self.vconnectors.values())

    def add_vconnector(self, host: dict = None, bd_id: str = ''):
        if not bd_id or bd_id in self.vconnectors:
            return
        self.vconnectors[bd_id] = dict(
            host=host['id'],
            id='{}-vconnector-{}'.format(host['id'], bd_id),
            bd_id=bd_id,
            name='bridge-domain-{}'.format(bd_id),
            object_name='{}-VPP-bridge-domain-{}'.format(host['id'], bd_id),
        )

    def get_interface_details(self, host, name):
        # find vconnector interfaces
        cmd = "vppctl show hardware-interfaces {}".format(self.clean_interface(name))
        interface_lines = self.run_fetch_lines(cmd, host['id'])
        interfaces = parse_hw_interfaces(interface_lines)
        return interfaces[0] if interfaces else None
