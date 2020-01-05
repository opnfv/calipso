###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from scan.fetchers.aci.aci_access import AciAccess


class AciBaseFetchSwitch(AciAccess):

    def fetch_pnic_interface(self, switch_id, pnic_id):
        dn = "/".join((switch_id, "sys", "phys-[{}]".format(pnic_id)))
        response = self.fetch_mo_data(dn)
        interface_data = self.get_objects_by_field_names(response, "l1PhysIf",
                                                                   "attributes")
        return interface_data[0] if interface_data else None
