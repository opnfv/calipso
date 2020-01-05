###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.utils.vpp_utils import parse_hw_interfaces
from scan.fetchers.cli.cli_fetch_instance_vnics_base import CliFetchInstanceVnicsBase


class CliFetchInstanceVnicsVpp(CliFetchInstanceVnicsBase):

    def set_vnic_names(self, v, instance):
        v["object_name"] = "|".join((instance["name"], v["mac_address"]))
        v["id"] = instance["host"]
        interface_name = v.get("interface_name", "").replace("/", ".")
        if interface_name:
            v["id"] = "|".join((v["id"], interface_name))
            v["name"] = "|".join((v["id"], v["object_name"]))
        else:
            v["interface_name"] = v["object_name"]  # SRIOV interfaces
            v["id"] = "|".join((v["id"], v["object_name"]))
            v["name"] = v["id"]

    def get_vpp_interfaces(self, host):
        vpp_show_lines = self.run_fetch_lines("vppctl show hardware-interfaces", host)
        return parse_hw_interfaces(vpp_show_lines)

    def get_vnics_data(self, name, instance):
        vnics = super().get_vnics_data(name, instance)
        vpp_interfaces = self.get_vpp_interfaces(instance["host"])

        for vnic in vnics:
            interface = next((i for i in vpp_interfaces if i.get("mac_address") == vnic["mac_address"]), None)
            if interface:
                vnic["interface_name"] = interface["name"]
            else:  # Mismatched mac address between libvirt and vpp
                uuid = vnic.get("uuid")
                if uuid:
                    vnic["interface_name"] = "undefined-{}".format(uuid)
                else:
                    continue

            self.set_vnic_names(vnic, instance)

        return vnics
