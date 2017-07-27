import re

from discover.fetchers.aci.aci_access import AciAccess, aci_config_required
from utils.inventory_mgr import InventoryMgr
from utils.util import encode_aci_dn, get_object_path_part


class AciFetchSwitchPnic(AciAccess):

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def fetch_pnics_by_mac_address(self, mac_address):
        mac_filter = "eq(epmMacEp.addr,\"{}\")".format(mac_address)
        pnic_filter = "wcard(epmMacEp.ifId, \"eth\")"
        query_filter = "and({},{})".format(mac_filter, pnic_filter)

        pnics = self.fetch_objects_by_class("epmMacEp",
                                            {"query-target-filter": query_filter})

        return [pnic["attributes"] for pnic in pnics]

    def fetch_switch_by_id(self, switch_id):
        dn = "/".join((switch_id, "sys"))
        response = self.fetch_mo_data(dn)
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

        switch_pnics = self.fetch_pnics_by_mac_address(mac_address)
        if not switch_pnics:
            return []
        switch_pnic = switch_pnics[0]

        # Prepare and save switch data in inventory
        aci_id_match = re.match("topology/(.+)/sys", switch_pnic["dn"])
        if not aci_id_match:
            raise ValueError("Failed to fetch switch id from pnic dn: {}"
                             .format(switch_pnic["dn"]))

        aci_switch_id = aci_id_match.group(1)
        db_switch_id = encode_aci_dn(aci_switch_id)
        if not self.inv.get_by_id(environment, db_switch_id):
            switch_data = self.fetch_switch_by_id(aci_switch_id)
            if not switch_data:
                self.log.warning("No switch found for switch pnic dn: {}"
                                 .format(switch_pnic["dn"]))
                return []

            switch_json = {
                "id": db_switch_id,
                "ip_address": switch_data["address"],
                "type": "switch",
                "aci_document": switch_data
            }
            # Region name is the same as region id
            region_id = get_object_path_part(pnic["name_path"], "Regions")
            region = self.inv.get_by_id(environment, region_id)
            self.inv.save_inventory_object(o=switch_json, parent=region, environment=environment)

        db_pnic_id = "-".join((db_switch_id,
                               encode_aci_dn(switch_pnic["ifId"]),
                               mac_address))
        pnic_json = {
            "id": db_pnic_id,
            "type": "pnic",
            "pnic_type": "switch",
            "mac_address": mac_address,
            "aci_document": switch_pnic
        }
        return [pnic_json]

