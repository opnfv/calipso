#!/usr/bin/env python
###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

import subprocess
import sys

from .binary_converter import binary2str


def nic_not_found(name, output):
    print("Error finding NIC {}{}{}\n".format(name, ': ' if output else '',
                                              output))
    return 2

if len(sys.argv) < 2:
    print('name of interface must be specified')
    exit(2)
nic_name = str(sys.argv[1])

rc = 0

try:
    cmd = 'ip link show | grep -A1 "^[0-9]\+: {}:"'.format(nic_name)
    out = subprocess.check_output([cmd], stderr=subprocess.STDOUT, shell=True)
    out = binary2str(out)
    lines = out.splitlines()
    if not lines:
        rc = nic_not_found(nic_name, '')
    else:
        line = lines[0]
        if ' state UP ' not in line:
            rc = 2
        print(out)
except subprocess.CalledProcessError as e:
    rc = nic_not_found(nic_name, binary2str(e.output))

exit(rc)
