#!/usr/bin/env python
###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

# find status of instance network
# For each instance vNIC - take the MAC address
# For each vService in the same network as the instance,
# use local_service_id attribute in the following command in the network node:
# "ip netns exec <local_service_id> arp -n"
# look for the instance vNIC's mac_address to appear in the response
# for each mac_address:
# - if Flag 'C' = 'Complete' - mark result OK for that instance,
# - 'I' = 'Incomplete' - mark as 'warn',
# - no mac_address mark as 'error'

import sys
import subprocess

from binary_converter import binary2str


arp_headers = ['Address', 'HWtype', 'HWaddress', 'Flags', 'Mask', 'Iface']
arp_mac_pos = arp_headers.index('HWaddress')
arp_flags_pos = arp_headers.index('Flags')


def check_vnic_tuple(vnic_and_service):
    tuple_parts = vnic_and_service.split(',')
    local_service_id = tuple_parts[0]
    mac_address = tuple_parts[1]
    check_output = None
    try:
        netns_cmd = 'ip netns exec {} arp -n'.format(local_service_id)
        check_output = 'MAC={}, local_service_id={}\n'\
            .format(mac_address, local_service_id)
        netns_out = subprocess.check_output([netns_cmd],
                                            stderr=subprocess.STDOUT,
                                            shell=True)
        netns_out = binary2str(netns_out)
        check_output += '{}\n'.format(netns_out)
        netns_lines = netns_out.splitlines()
        if not netns_lines or \
                netns_lines[0].endswith('No such file or directory'):
            check_rc = 2
        else:
            mac_found = False
            flags = None
            for l in netns_lines:
                line_parts = l.split()
                line_mac = line_parts[arp_mac_pos]
                if len(line_parts) > arp_mac_pos and line_mac == mac_address:
                    mac_found = True
                    flags = line_parts[arp_flags_pos]
                    break
            if mac_found:
                check_rc = 1 if flags == 'I' else 0
            else:
                check_rc = 2
    except subprocess.CalledProcessError as e:
        check_output = str(e)
        check_rc = 2
    return check_rc, check_output


if len(sys.argv) < 2:
    print('usage: ' + sys.argv[0] +
          ' <vService local_service_id>,<MAC>[;<>,<>]...')
    exit(1)

rc = 0
output = ''
vnics = str(sys.argv[1]).split(';')
for vnic_tuple in vnics:
    tuple_ret, out = check_vnic_tuple(vnic_tuple)
    rc = min(rc, tuple_ret)
    output += out
print(output)
exit(rc)
