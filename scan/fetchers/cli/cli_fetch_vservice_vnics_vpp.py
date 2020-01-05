###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.utils.origins import Origin
from base.utils.vpp_utils import parse_hw_interfaces
from scan.fetchers.cli.cli_fetch_vservice_vnics import CliFetchVserviceVnics


class CliFetchVserviceVnicsVpp(CliFetchVserviceVnics):

    def __init__(self):
        super().__init__()
        self.vpp_interfaces = None

    def setup(self, env, origin: Origin = None):
        super().setup(env, origin)
        self.vpp_interfaces = {}

    def get(self, host_id):
        if host_id not in self.vpp_interfaces:
            vpp_show_lines = self.run_fetch_lines("vppctl show hardware-interfaces", host_id)
            self.vpp_interfaces[host_id] = parse_hw_interfaces(vpp_show_lines)
        return super().get(host_id)

    def set_vnic_names(self, vnic):
        interface_name = next((
            i["name"] for i in self.vpp_interfaces[vnic["host"]]
            if i.get("mac_address") == vnic["mac_address"]
        ), None)

        if not interface_name:
            self.log.warning("vnic with mac_address '{}' is not attached to any VPP interface".format(vnic["mac_address"]))
            interface_name = "unattached-{}".format(vnic["mac_address"])

        vnic["interface_name"] = "|".join((interface_name, vnic["object_name"].split("@")[0]))
        vnic["id"] = "|".join((vnic["host"], interface_name))
        vnic["name"] = "|".join((vnic["id"], vnic["object_name"]))
