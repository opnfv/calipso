###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.events.event_base import EventResult
from discover.events.event_delete_base import EventDeleteBase
from discover.events.event_port_delete import EventPortDelete
from utils.util import encode_router_id


class EventInterfaceDelete(EventDeleteBase):

    def handle(self, env, values):
        interface = values['payload']['router_interface']
        port_id = interface['port_id']
        host_id = values["publisher_id"].replace("network.", "", 1)
        router_id = encode_router_id(host_id, interface['id'])

        # update router document
        port_doc = self.inv.get_by_id(env, port_id)
        if not port_doc:
            self.log.info("Interface deleting handler: port document not found.")
            return EventResult(result=False, retry=False)
        network_id = port_doc['network_id']

        router_doc = self.inv.get_by_id(env, router_id)
        if router_doc and network_id in router_doc.get('network', []):
            router_doc['network'].remove(network_id)
            self.inv.set(router_doc)

        # delete port document
        result = EventPortDelete().delete_port(env, port_id)
        result.related_object = interface['id']
        result.display_context = network_id
        return result
