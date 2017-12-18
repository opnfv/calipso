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

# find status of vconnector
# vconnector object name defines name of bridge
# use "brctl showmacs <bridge>", return ERROR if 'No such device' is returned

import sys
import subprocess

from binary_converter import binary2str


if len(sys.argv) < 2:
    print('usage: ' + sys.argv[0] + ' <bridge>')
    exit(1)
bridge_name = str(sys.argv[1])

rc = 0

cmd = None
out = ''
try:
    cmd = "brctl showmacs {}".format(bridge_name)
    out = subprocess.check_output([cmd],
                                  stderr=subprocess.STDOUT,
                                  shell=True)
    out = binary2str(out)
    lines = out.splitlines()
    if not lines or lines[0].endswith('No such device'):
        rc = 2
    else:
        print(out)
except subprocess.CalledProcessError as e:
    rc = 2
    out = str(e)

if rc != 0:
    print('Failed to find vConnector {}:\n{}\n'
          .format(bridge_name, out))

exit(rc)
