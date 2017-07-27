#!/usr/bin/env python3
###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

# find status of vnic-vconnector link
# vconnector object name defines name of bridge
# use "brctl showmacs <bridge>", then look for the MAC address

import re
import sys
import subprocess

from binary_converter import binary2str


if len(sys.argv) < 3:
    print('usage: ' + sys.argv[0] + ' <bridge> <mac_address>')
    exit(2)
bridge_name = str(sys.argv[1])
mac_address = str(sys.argv[2])

rc = 0

try:
    out = subprocess.check_output(["brctl showmacs " + bridge_name],
                                  stderr=subprocess.STDOUT,
                                  shell=True)
    out = binary2str(out)
    lines = out.splitlines()
    line_number = 1
    line = ''
    found = False
    while line_number < len(lines):
        line = lines[line_number]
        if mac_address in line:
            found = True
            break
        line_number += 1
    state_match = re.match('^\W+([A-Z]+)', line)
    if not found:
        rc = 2
        print('Error: failed to find MAC {}:\n{}\n'
              .format(mac_address, out))
    else:
        # grab "is local?" and "ageing timer" values
        line_parts = line.split()  # port, mac address, is local?, ageing timer
        is_local = line_parts[2]
        ageing_timer = line_parts[3]
        msg_format =\
            'vConnector bridge name: {}\n'\
            'vNIC MAC address: {}\n'\
            'is local: {}\n'\
            'ageing timer: {}\n'\
            'vNIC MAC address: {}\n'\
            'command: brctl showmacs {}\n'\
            'output:\n{}'
        msg = msg_format.format(bridge_name, mac_address, is_local,
                                ageing_timer, mac_address, bridge_name, out)
        print(msg)
except subprocess.CalledProcessError as e:
    print("Error finding MAC {}: {}\n"
          .format(mac_address, binary2str(e.output)))
    rc = 2

exit(rc)
