###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re

from discover.fetchers.aci.aci_access import AciAccess, aci_config_required
from utils.inventory_mgr import InventoryMgr
from utils.util import encode_aci_dn, get_object_path_part


# Fetches and adds to database:
# 1. ACI Switch
#
# Returns:
# 1. ACI Switch pnic that belongs to the ACI Switch (mentioned above)
# and is connected to Calipso host pnic.
class AciFetchSwitchPnic(AciAccess):

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def fetch_pnics_by_mac_address(self, mac_address):
        mac_filter = "eq(epmMacEp.addr,\"{}\")".format(mac_address)
        # We are only interested in Ethernet interfaces
        pnic_filter = "wcard(epmMacEp.ifId, \"eth\")"
        query_filter = "and({},{})".format(mac_filter, pnic_filter)

        pnics = self.fetch_objects_by_class("epmMacEp",
                                            {"query-target-filter": query_filter})

        return [pnic["attributes"] for pnic in pnics]

    def fetch_switch_by_id(self, switch_id):
        dn = "/".join((switch_id, "sys"))
        response = self.fetch_mo_data(dn)
        # Unwrap switches
        switch_data = self.get_objects_by_field_names(response, "topSystem", "attributes")
        return switch_data[0] if switch_data else None

    @aci_config_required(default=[])
    def get(self, pnic_id):
        environment = self.get_env()
        pnic = self.inv.get_by_id(environment=environment, item_id=pnic_id)
        if not pnic:
            return []
        mac_address = pnic.get("mac_address")
        if not mac_address:
            return []

        # Query ACI for related switch pnic
        leaf_pnics = self.fetch_pnics_by_mac_address(mac_address)
        if not leaf_pnics:
            return []
        leaf_pnic = leaf_pnics[0]

        # Prepare and save switch data in inventory
        leaf_id_match = re.match("topology/(.+)/sys", leaf_pnic["dn"])
        if not leaf_id_match:
            raise ValueError("Failed to fetch leaf switch id from pnic dn: {}"
                             .format(leaf_pnic["dn"]))

        aci_leaf_id = leaf_id_match.group(1)
        leaf_data = self.fetch_switch_by_id(aci_leaf_id)
        if not leaf_data:
            self.log.warning("No switch found for switch pnic dn: {}"
                             .format(leaf_pnic["dn"]))
            return []

        db_leaf_id = "-".join(("switch", encode_aci_dn(aci_leaf_id), leaf_data["role"]))
        if not self.inv.get_by_id(environment, db_leaf_id):
            leaf_json = {
                "id": db_leaf_id,
                "ip_address": leaf_data["address"],
                "type": "switch",
                "host": db_leaf_id,
                "aci_document": leaf_data
            }
            # Region name is the same as region id
            region_id = get_object_path_part(pnic["name_path"], "Regions")
            region = self.inv.get_by_id(environment, region_id)
            self.inv.save_inventory_object(o=leaf_json, parent=region, environment=environment)

        # Prepare pnic json for results list
        db_pnic_id = "-".join((db_leaf_id,
                               encode_aci_dn(leaf_pnic["ifId"]),
                               mac_address))
        pnic_json = {
            "id": db_pnic_id,
            "type": "pnic",
            "pnic_type": "switch",
            "mac_address": mac_address,
            "host": db_leaf_id,
            "aci_document": leaf_pnic
        }
        return [pnic_json]

