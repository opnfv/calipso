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
from utils.util import decode_aci_dn, encode_aci_dn, get_object_path_part


# Fetches and adds to database:
# 1. ACI Switches with role "spine"
#
# Returns:
# 1. ACI Switch uplink pnics that belong to the "leaf" switch
# 2. ACI Switch downlink pnics that belong to "spine" switches mentioned above
# and are connected to the "leaf" switch
class AciFetchLeafToSpinePnics(AciAccess):

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def fetch_switches_by_role(self, role_name):
        query_filter = {"query-target-filter":
                        "eq(fabricNode.role, \"{}\")".format(role_name)}
        switches = self.fetch_objects_by_class("fabricNode", query_filter)
        return [switch["attributes"] for switch in switches]

    def fetch_adjacent_connections(self, device_id):
        dn = "/".join((device_id, "sys"))

        response = self.fetch_mo_data(dn,
                                      {"query-target": "subtree",
                                       "target-subtree-class": "lldpAdjEp"})

        connections = self.get_objects_by_field_names(response,
                                                      "lldpAdjEp", "attributes")
        return connections

    # Returns:
    # List of:
    # 1. Switches with role "spine"
    # 2. Downlink pnic id for spine switch
    # 3. Uplink pnic id for leaf switch
    def fetch_spines_and_pnics_by_leaf_id(self, leaf_id):
        spine_switches = self.fetch_switches_by_role("spine")
        adjacent_devices = self.fetch_adjacent_connections(leaf_id)
        spines = []
        for spine in spine_switches:
            # Check if spine switch is connected to current leaf switch
            connection = next((d for d in adjacent_devices
                               if spine["name"] == d["sysName"]),
                              None)
            if connection:
                try:
                    # Extract pnics from adjacency data
                    uplink_pnic = re.match(".*\[(.+?)\].*",
                                           connection["dn"]).group(1)
                    downlink_pnic = re.match(".*\[(.+?)\].*",
                                             connection["portDesc"]).group(1)
                    spines.append({
                        "device": spine,
                        "downlink_pnic": downlink_pnic,
                        "uplink_pnic": uplink_pnic
                    })
                except AttributeError:
                    continue  # TODO: probably raise an exception

        return spines

    @aci_config_required(default=[])
    def get(self, db_leaf_pnic_id):
        environment = self.get_env()
        pnic = self.inv.get_by_id(environment=environment,
                                  item_id=db_leaf_pnic_id)

        # Decode aci leaf switch id from db format
        aci_leaf_pnic_id = decode_aci_dn(db_leaf_pnic_id)
        aci_leaf_id = re.match("switch-(.+?)-leaf", aci_leaf_pnic_id).group(1)

        # Fetch all leaf-to-spine connectivity data
        spines_with_pnics = self.fetch_spines_and_pnics_by_leaf_id(aci_leaf_id)
        pnics = []
        for spine_with_pnic in spines_with_pnics:
            spine = spine_with_pnic["device"]
            downlink_pnic_id = spine_with_pnic["downlink_pnic"]
            uplink_pnic_id = spine_with_pnic["uplink_pnic"]

            # Add spine switch to db if it's not there yet
            spine_id_match = re.match("topology/(.+)", spine["dn"])
            if not spine_id_match:
                raise ValueError("Failed to fetch spine switch id "
                                 "from switch dn: {}".format(spine["dn"]))

            aci_spine_id = spine_id_match.group(1)
            db_spine_id = "-".join(("switch", encode_aci_dn(aci_spine_id),
                                    spine["role"]))
            if not self.inv.get_by_id(environment, db_spine_id):
                spine_json = {
                    "id": db_spine_id,
                    "type": "switch",
                    "aci_document": spine
                }
                # Region name is the same as region id
                region_id = get_object_path_part(pnic["name_path"], "Regions")
                region = self.inv.get_by_id(environment, region_id)
                self.inv.save_inventory_object(o=spine_json, parent=region,
                                               environment=environment)

            # Add downlink and uplink pnics to results list,
            # including their mutual connection data
            # (see "connected_to" field).
            db_downlink_pnic_id = "-".join((db_spine_id,
                                            encode_aci_dn(downlink_pnic_id)))
            db_uplink_pnic_id = "-".join((pnic["host"],  # host == switch
                                          encode_aci_dn(uplink_pnic_id)))

            downlink_pnic_json = {
                "id": db_downlink_pnic_id,
                "type": "pnic",
                "role": "downlink",
                "pnic_type": "switch",
                "connected_to": db_uplink_pnic_id,
                "switch": db_spine_id,
                "aci_document": {}  # TODO: what can we add here?
            }

            uplink_pnic_json = {
                "id": db_uplink_pnic_id,
                "type": "pnic",
                "role": "uplink",
                "pnic_type": "switch",
                "connected_to": db_downlink_pnic_id,
                "switch": db_spine_id,
                "aci_document": {}  # TODO: what can we add here?
            }

            pnics.extend([downlink_pnic_json, uplink_pnic_json])

        return pnics
