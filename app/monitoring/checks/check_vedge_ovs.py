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
"""
Check OVS vEdge health

Run command: 
ps -aux | grep "\(ovs-vswitchd\|ovsdb-server\)"

OK if for both ovs-vswitchd AND ovsdb-server processes we see '(healthy)'
otherwise CRITICAL

return full text output of the command
"""

import subprocess

from binary_converter import binary2str


rc = 0
cmd = 'ps aux | grep "\(ovs-vswitchd\|ovsdb-server\): monitoring" | ' + \
      'grep -v grep'

try:
    out = subprocess.check_output([cmd], stderr=subprocess.STDOUT, shell=True)
    out = binary2str(out)
    lines = out.splitlines()
    matching_lines = [l for l in lines if '(healthy)']
    rc = 0 if len(matching_lines) == 2 else 2
    print(out)
except subprocess.CalledProcessError as e:
    print("Error finding expected output: {}".format(binary2str(e.output)))
    rc = 2

exit(rc)
