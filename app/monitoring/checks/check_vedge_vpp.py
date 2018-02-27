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
"""
sudo vppctl show runtime:

test 1: was the return value not null?
test 2: is startup-config-process = done?
1 and 2 = vedge status ok
1 and not 2 = vedge status warning
not 1 = vedge status critical

return full text of "vppctl show runtime"
"""

import re
import subprocess

from binary_converter import binary2str


rc = 0
search_pattern = re.compile("^startup-config-process ")

try:
    out = subprocess.check_output(["sudo vppctl show runtime"],
                                  stderr=subprocess.STDOUT,
                                  shell=True)
    out = binary2str(out)
    lines = out.splitlines()
    matching_lines = [l for l in lines if search_pattern.match(l)]
    matching_line = matching_lines[0] if matching_lines else None
    if matching_line and "done" in matching_line.split():
        print(out)
    else:
        rc = 1
        print('Error: failed to find status in ifconfig output: ' + out)
except subprocess.CalledProcessError as e:
    print("Error finding 'vppctl show runtime': {}"
          .format(binary2str(e.output)))
    rc = 2

exit(rc)
