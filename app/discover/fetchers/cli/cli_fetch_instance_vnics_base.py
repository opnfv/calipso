###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import xmltodict

from discover.fetchers.cli.cli_access import CliAccess
from utils.inventory_mgr import InventoryMgr


class CliFetchInstanceVnicsBase(CliAccess):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def get(self, id):
        instance_uuid = id[:id.rindex('-')]
        instance = self.inv.get_by_id(self.get_env(), instance_uuid)
        if not instance:
            return []
        host = self.inv.get_by_id(self.get_env(), instance["host"])
        if not host or "Compute" not in host["host_type"]:
            return []
        lines = self.run_fetch_lines("virsh list", instance["host"])
        del lines[:2]  # remove header
        virsh_ids = [l.split()[0] for l in lines if l > ""]
        results = []
        # Note: there are 2 ids here of instances with local names, which are
        # not connected to the data we have thus far for the instance
        # therefore, we will decide whether the instance is the correct one
        # based on comparison of the uuid in the dumpxml output
        for id in virsh_ids:
            results.extend(self.get_vnics_from_dumpxml(id, instance))
        return results

    def get_vnics_from_dumpxml(self, id, instance):
        xml_string = self.run("virsh dumpxml " + id, instance["host"])
        if not xml_string.strip():
            return []
        response = xmltodict.parse(xml_string)
        if instance["uuid"] != response["domain"]["uuid"]:
            # this is the wrong instance - skip it
            return []
        try:
            vnics = response["domain"]["devices"]["interface"]
        except KeyError:
            return []
        if isinstance(vnics, dict):
            vnics = [vnics]
        for v in vnics:
            self.set_vnic_properties(v, instance)
        return vnics

    def set_vnic_properties(self, v, instance):
        v["name"] = self.get_vnic_name(v, instance)
        v["id"] = v["name"]
        v["vnic_type"] = "instance_vnic"
        v["host"] = instance["host"]
        v["instance_id"] = instance["id"]
        v["instance_db_id"] = instance["_id"]
        v["mac_address"] = v["mac"]["@address"]
        instance["mac_address"] = v["mac_address"]
        self.inv.set(instance)
