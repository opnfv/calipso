###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.events.event_base import EventBase, EventResult
from discover.events.event_port_delete import EventPortDelete
from discover.events.event_router_add import EventRouterAdd
from discover.fetchers.cli.cli_fetch_host_vservice import CliFetchHostVservice
from discover.link_finders.find_links_for_vservice_vnics import FindLinksForVserviceVnics
from discover.scanner import Scanner
from utils.util import encode_router_id


class EventRouterUpdate(EventBase):

    def handle(self, env, values):
        payload = values['payload']
        router = payload['router']

        project_id = values['_context_project_id']
        host_id = values["publisher_id"].replace("network.", "", 1)
        router_id = payload['id'] if 'id' in payload else router['id']

        router_full_id = encode_router_id(router_id)
        router_doc = self.inv.get_by_id(env, router_full_id)
        if not router_doc:
            self.log.info("Router document not found, aborting router updating")
            return EventResult(result=False, retry=True)

        router_doc['admin_state_up'] = router['admin_state_up']
        router_doc['name'] = router['name']
        gateway_info = router.get('external_gateway_info')
        if gateway_info is None:
            # when delete gateway, need to delete the port relate document.
            port_doc = {}
            if router_doc.get('gw_port_id'):
                port_doc = self.inv.get_by_id(env, router_doc['gw_port_id'])
                EventPortDelete().delete_port(env, router_doc['gw_port_id'])

            if router_doc.get('network'):
                if port_doc:
                    router_doc['network'].remove(port_doc['network_id'])
                router_doc['gw_port_id'] = None

                # remove related links
                self.inv.delete('links', {'source_id': router_full_id})
        else:
            if 'network' in router_doc:
                if gateway_info['network_id'] not in router_doc['network']:
                    router_doc['network'].append(gateway_info['network_id'])
            else:
                router_doc['network'] = [gateway_info['network_id']]
            # update static route
            router_doc['routes'] = router['routes']

            # add gw_port_id info and port document.
            fetcher = CliFetchHostVservice()
            fetcher.set_env(env)
            router_vservice = fetcher.get_vservice(host_id, router_full_id)
            if router_vservice.get('gw_port_id'):
                router_doc['gw_port_id'] = router_vservice['gw_port_id']

            host = self.inv.get_by_id(env, host_id)
            EventRouterAdd().add_children_documents(env, project_id, gateway_info['network_id'], host, router_doc)

            # rescan the vnic links.
            FindLinksForVserviceVnics().add_links(search={'parent_id': router_full_id + '-vnics'})
        self.inv.set(router_doc)

        # update the cliques.
        scanner = Scanner()
        scanner.set_env(env)
        scanner.scan_cliques()
        self.log.info("Finished router update.")
        return EventResult(result=True,
                           related_object=router_full_id,
                           display_context=router_full_id)
