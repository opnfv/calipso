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
"""
sudo vppctl show hardware-interfaces:

take only the virtual interfaces, e.g. "VirtualEthernet0/0/0"
Status: "OK" if "up" is detected in the interface line, CRITICAL otherwise

return full text of "vppctl show hardware-interfaces"
"""

import subprocess

import re

from .binary_converter import binary2str

rc = 0
search_pattern = re.compile("^Virtual")

try:
    out = subprocess.check_output(["sudo vppctl show hardware-interfaces"],
                                  stderr=subprocess.STDOUT,
                                  shell=True)
    out = binary2str(out)
    lines = out.splitlines()
    matching_lines = [l for l in lines if search_pattern.match(l)]
    matching_line = matching_lines[0] if matching_lines else None
    if matching_line and "up" in matching_line.split():
        print('output of "vppctl show hardware-interfaces":\n{}'
              .format(out))
    else:
        rc = 2
        print('Error: failed to find status in output of '
              '"vppctl show hardware-interfaces": {}'.format(out))
except subprocess.CalledProcessError as e:
    print("Error finding 'vppctl show hardware-interfaces': {}"
          .format(binary2str(e.output)))
    rc = 2

exit(rc)
