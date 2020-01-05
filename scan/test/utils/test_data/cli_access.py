###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
COMPUTE_HOST_ID = "node-5.cisco.com"
COMMAND = "virsh list --all"
NON_GATEWAY_CACHED_COMMAND = \
    '{},ssh -q -o StrictHostKeyChecking=no {} \'sudo {}\'' \
    .format(COMPUTE_HOST_ID, COMPUTE_HOST_ID, COMMAND)
GATEWAY_CACHED_COMMAND = '{},sudo {}'.format(COMPUTE_HOST_ID, COMMAND)
CACHED_COMMAND_RESULT = " Id  Name  State\n---\n 2 instance-00000003 running"
RUN_RESULT = " Id  Name  State\n---\n 2 instance-00000002 running"
FETCH_LINES_RESULT = [
    " Id  Name  State",
    "---",
    " 2 instance-00000002 running"
]

LINES_FOR_FIX = [
    "br-ex\t\t8000.005056acc9a2\tno\t\teno33554952",
    "\t\t\t\t\t\t\tp_ff798dba-0",
    "\t\t\t\t\t\t\tv_public",
    "\t\t\t\t\t\t\tv_vrouter_pub",
    "br-fw-admin\t\t8000.005056ace897\tno\t\teno16777728"
]

FIXED_LINES = [
    "br-ex\t\t8000.005056acc9a2\tno\t\teno33554952,"
    "p_ff798dba-0,v_public,v_vrouter_pub",
    "br-fw-admin\t\t8000.005056ace897\tno\t\teno16777728"
]

PARSED_CMD_RESULT = [
    {
        "bridge_id": "8000.005056acc9a2",
        "bridge_name": "br-ex",
        "interfaces": "eno33554952,p_ff798dba-0,v_public,v_vrouter_pub",
        "stp_enabled": "no"
    },
    {
        "bridge_id": "8000.005056ace897",
        "bridge_name": "br-fw-admin",
        "interfaces": "eno16777728",
        "stp_enabled": "no"
    }
]

LINE_FOR_PARSE = "br-ex\t\t8000.005056acc9a2\tno\t\teno33554952," \
    "p_ff798dba-0,v_public,v_vrouter_pub"
PARSED_LINE = {
    "bridge_id": "8000.005056acc9a2",
    "bridge_name": "br-ex",
    "interfaces": "eno33554952,p_ff798dba-0,v_public,v_vrouter_pub",
    "stp_enabled": "no"
}
HEADERS = ["bridge_name", "bridge_id", "stp_enabled", "interfaces"]
