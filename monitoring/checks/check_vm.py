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
    Checks vm status using "virsh domstate".
    Status: OK if domstate is "running", Warning if "shut off", Error otherwise
"""

import subprocess
import sys

from .binary_converter import binary2str

CMD = "virsh domstate {}"

STATUSES = {
    'running': 0,
    'shut off': 1,
}


def something_wrong(vm_name, lines=None):  # TODO
    print("Error while running check for vm: '{}'".format(vm_name))
    if lines:
        print("Output:\n{}".format("\n".join(lines)))
    return 2


def run():
    if len(sys.argv) < 2:
        print("Instance name should be specified")
        return 2
    vm_name = str(sys.argv[1])

    try:
        cmd = CMD.format(vm_name)
        out = subprocess.check_output([cmd], stderr=subprocess.STDOUT,
                                      shell=True)
        out = binary2str(out)
        lines = out.splitlines()
        if not lines or lines[0].startswith('error'):
            return something_wrong(vm_name, lines)
        print(lines[0].strip().replace("\n", ""))

        return STATUSES.get(lines[0].strip().lower(), 2)
    except subprocess.CalledProcessError as e:
        print(e)
        return something_wrong(vm_name)

exit(run())
