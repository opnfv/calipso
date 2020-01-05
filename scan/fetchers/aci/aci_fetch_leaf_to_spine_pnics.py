###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re

from base.utils.inventory_mgr import InventoryMgr
from base.utils.util import decode_aci_dn, encode_aci_dn
from scan.fetchers.aci.aci_access import aci_config_required
from scan.fetchers.aci.aci_base_fetch_switch import AciBaseFetchSwitch


# Fetches and adds to database:
# 1. ACI Switches with role "spine"
#
# Returns:
# 1. ACI Switch uplink pnics that belong to the "leaf" switch
# 2. ACI Switch downlink pnics that belong to "spine" switches mentioned above
# and are connected to the "leaf" switch
class AciFetchLeafToSpinePnics(AciBaseFetchSwitch):

    def __init__(self, config=None):
        super().__init__(config=config)
        self.inv = InventoryMgr()
        self.spines = {}  # Persist spines data for the duration of scan

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
        if leaf_id in self.spines:
            self.log.info("Reusing cached spines for leaf: {}".format(leaf_id))
            return self.spines[leaf_id]

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

        self.spines[leaf_id] = spines
        return spines

    @aci_config_required(default=[])
    def get(self, db_leaf_pnic_id):
        environment = self.get_env()
        leaf_pnic = self.inv.get_by_id(environment=environment,
                                       item_id=db_leaf_pnic_id)
        leaf_switch_id = leaf_pnic['switch']

        # Decode aci leaf switch id from initial_data format
        aci_leaf_pnic_id = decode_aci_dn(db_leaf_pnic_id)
        aci_leaf_id = re.match("switch-(.+?)-leaf", aci_leaf_pnic_id).group(1)

        # Fetch all leaf-to-spine connectivity data
        spines_with_pnics = self.fetch_spines_and_pnics_by_leaf_id(aci_leaf_id)
        pnics = []
        for spine_with_pnic in spines_with_pnics:
            spine = spine_with_pnic["device"]
            downlink_pnic_id = spine_with_pnic["downlink_pnic"]
            uplink_pnic_id = spine_with_pnic["uplink_pnic"]

            # Add spine switch to initial_data if it's not there yet
            spine_id_match = re.match("topology/(.+)", spine["dn"])
            if not spine_id_match:
                raise ValueError("Failed to fetch spine switch id "
                                 "from switch dn: {}".format(spine["dn"]))

            # Add parent switch to initial_data.
            # A dedicated fetcher for the switch is not feasible
            # because it is discovered through pnic-to-pnic links,
            # but has to be set in initial_data BEFORE the related pnic.
            aci_spine_id = spine_id_match.group(1)
            db_spine_id = "-".join(("switch", encode_aci_dn(aci_spine_id),
                                    spine["role"]))
            if not self.inv.get_by_id(environment, db_spine_id):
                spine_json = {
                    "id": db_spine_id,
                    "type": "switch",
                    "switch": db_spine_id,
                    "aci_document": spine
                }
                self.set_folder_parent(spine_json, object_type='switch',
                                       master_parent_type='environment',
                                       master_parent_id=self.env)
                self.inv.save_inventory_object(o=spine_json,
                                               parent={'environment': self.env,
                                                       'id': self.env},
                                               environment=environment)

            # Add downlink and uplink pnics to results list,
            # including their mutual connection data
            # (see "connected_to" field).
            db_downlink_pnic_id = "-".join((db_spine_id,
                                            encode_aci_dn(downlink_pnic_id)))
            db_uplink_pnic_id = "-".join((leaf_pnic["switch"],
                                          encode_aci_dn(uplink_pnic_id)))

            downlink_pnic_json = {
                "id": db_downlink_pnic_id,
                "object_name": downlink_pnic_id,
                "type": "switch_pnic",
                "role": "downlink",
                "connected_to": db_uplink_pnic_id,
                "switch": db_spine_id,
                "parent_id": db_spine_id,
                "parent_type": "switch",
                "aci_switch_id": aci_spine_id,
                "aci_document": self.fetch_pnic_interface(switch_id=aci_spine_id,
                                                          pnic_id=downlink_pnic_id)
            }

            uplink_pnic_json = {
                "id": db_uplink_pnic_id,
                "object_name": uplink_pnic_id,
                "type": "switch_pnic",
                "role": "uplink",
                "connected_to": db_downlink_pnic_id,
                "switch": leaf_switch_id,
                "parent_id": leaf_switch_id,
                "parent_type": "switch",
                "aci_switch_id": aci_leaf_id,
                "aci_document": self.fetch_pnic_interface(switch_id=aci_leaf_id,
                                                          pnic_id=uplink_pnic_id)
            }

            pnics.extend([downlink_pnic_json, uplink_pnic_json])

        return pnics
