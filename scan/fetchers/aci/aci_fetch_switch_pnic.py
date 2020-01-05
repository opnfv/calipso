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

from base.utils.origins import Origin

from base.utils.inventory_mgr import InventoryMgr
from base.utils.util import encode_aci_dn
from scan.fetchers.aci.aci_access import aci_config_required
from scan.fetchers.aci.aci_base_fetch_switch import AciBaseFetchSwitch


# Fetches and adds to database:
# 1. ACI Switch
#
# Returns:
# 1. ACI Switch pnic that belongs to the ACI Switch (mentioned above)
# and is connected to Calipso host pnic.
class AciFetchSwitchPnic(AciBaseFetchSwitch):

    def __init__(self, config=None):
        super().__init__(config=config)
        self.inv = InventoryMgr()
        self.discovered_macs = []  # Persist MACs that were already used for switch pNICs discovery

    def fetch_pnics_by_mac_address(self, mac_address):
        mac_filter = "eq(epmMacEp.addr,\"{}\")".format(mac_address)
        # We are only interested in Ethernet interfaces
        pnic_filter = "wcard(epmMacEp.ifId, \"eth|po\")"
        query_filter = {"query-target-filter":
                        "and({},{})".format(mac_filter, pnic_filter)}

        pnics = self.fetch_objects_by_class("epmMacEp", query_filter)

        return [pnic["attributes"] for pnic in pnics if 'ip' in pnic['attributes']['flags']]

    def fetch_switch_by_id(self, switch_id):
        dn = "/".join((switch_id, "sys"))
        response = self.fetch_mo_data(dn)
        # Unwrap switches
        switch_data = self.get_objects_by_field_names(response, "topSystem",
                                                      "attributes")
        return switch_data[0] if switch_data else None

    def fetch_client_endpoints(self, mac_address):
        mac_filter = "eq(fvCEp.mac,\"{}\")".format(mac_address)
        query_params = {
            "rsp-subtree": "children",
            "query-target-filter": mac_filter
        }

        endpoints = self.fetch_objects_by_class("fvCEp", query_params)

        results = []
        for endpoint in endpoints:
            result = endpoint["attributes"]
            result["fvRsCEpToPathEp"] = []
            for path in filter(lambda child: "fvRsCEpToPathEp" in child,
                               endpoint.get("children", [])):
                result["fvRsCEpToPathEp"].append(path["fvRsCEpToPathEp"]["attributes"])
            results.append(result)

        return results

    def fetch_switch_pnics_by_mac_address(self, mac_address):
        # Query ACI for related switch pnic
        leaf_pnics = self.fetch_pnics_by_mac_address(mac_address)
        if not leaf_pnics:
            return []

        results = []
        for leaf_pnic in leaf_pnics:
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

            # Add parent switch to initial_data.
            # A dedicated fetcher for the switch is not feasible
            # because it is discovered through pnic-to-pnic links,
            # but has to be set in initial_data BEFORE the related pnic.
            db_leaf_id = "-".join(("switch", encode_aci_dn(aci_leaf_id),
                                   leaf_data["role"]))
            environment = self.get_env()
            if not self.inv.get_by_id(environment, db_leaf_id):
                leaf_json = {
                    "id": db_leaf_id,
                    "ip_address": leaf_data["address"],
                    "type": "switch",
                    "switch": db_leaf_id,
                    "aci_document": leaf_data
                }
                self.set_folder_parent(leaf_json, object_type='switch',
                                       master_parent_type='environment',
                                       master_parent_id=self.env)
                self.inv.save_inventory_object(o=leaf_json,
                                               parent={'environment': self.env,
                                                       'id': self.env},
                                               environment=environment)

            # Prepare pnic json for results list
            fvCEp = self.fetch_client_endpoints(mac_address)

            aci_pnic_id = leaf_pnic["ifId"]
            db_pnic_id = "-".join([db_leaf_id,
                                   encode_aci_dn(aci_pnic_id),
                                   mac_address])

            interface_data = self.fetch_pnic_interface(switch_id=aci_leaf_id,
                                                       pnic_id=aci_pnic_id)
            pnic_json = {
                "id": db_pnic_id,
                "object_name": leaf_pnic["ifId"],
                "type": "switch_pnic",
                "role": "hostlink",
                "parent_id": db_leaf_id,
                "parent_type": "switch",
                "mac_address": mac_address,
                "switch": db_leaf_id,
                "aci_switch_id": aci_leaf_id,
                "aci_document": interface_data,
                "fvCEp": fvCEp
            }

            results.append(pnic_json)
        return results

    @aci_config_required(default=[])
    def get(self, pnic_id):
        environment = self.get_env()
        pnic = self.inv.get_by_id(environment=environment, item_id=pnic_id)
        if not pnic:
            return []
        mac_address = pnic.get("mac_address")
        if not mac_address:
            return []
        if mac_address in self.discovered_macs:
            self.log.info("Reusing cached switch pNICs for MAC address: {}".format(mac_address))
            return []

        self.discovered_macs.append(mac_address)
        return self.fetch_switch_pnics_by_mac_address(mac_address)
