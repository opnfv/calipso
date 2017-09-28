###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import time
from functools import partial

from discover.events.event_base import EventBase, EventResult
from discover.events.event_port_add import EventPortAdd
from discover.events.event_subnet_add import EventSubnetAdd
from discover.fetchers.api.api_access import ApiAccess
from discover.fetchers.api.api_fetch_regions import ApiFetchRegions
from discover.fetchers.cli.cli_fetch_host_vservice import CliFetchHostVservice
from discover.link_finders.find_links_for_vservice_vnics import \
    FindLinksForVserviceVnics
from discover.scanner import Scanner
from utils.util import decode_router_id, encode_router_id


class EventInterfaceAdd(EventBase):

    def __init__(self):
        super().__init__()
        self.delay = 2

    def add_gateway_port(self, env, project, network_name, router_doc, host_id):
        fetcher = CliFetchHostVservice()
        fetcher.set_env(env)
        router_id = router_doc['id']
        router = fetcher.get_vservice(host_id, router_id)
        device_id = decode_router_id(router_id)
        router_doc['gw_port_id'] = router['gw_port_id']

        # add gateway port documents.
        port_doc = EventSubnetAdd().add_port_document(env,
                                                      router_doc['gw_port_id'],
                                                      project_name=project)

        mac_address = port_doc['mac_address'] if port_doc else None

        # add vnic document
        host = self.inv.get_by_id(env, host_id)

        add_vnic_document = partial(EventPortAdd().add_vnic_document,
                                    env=env,
                                    host=host,
                                    object_id=device_id,
                                    object_type='router',
                                    network_name=network_name,
                                    router_name=router_doc['name'],
                                    mac_address=mac_address)

        ret = add_vnic_document()
        if not ret:
            time.sleep(self.delay)
            self.log.info("Wait %s second, and then fetch vnic document again." % self.delay)
            add_vnic_document()

    def update_router(self, env, project, network_id, network_name, router_doc, host_id):
        if router_doc:
            if 'network' in router_doc:
                if network_id not in router_doc['network']:
                    router_doc['network'].append(network_id)
            else:
                router_doc['network'] = [network_id]

            # if gw_port_id is None, add gateway port first.
            if not router_doc.get('gw_port_id'):
                self.add_gateway_port(env, project, network_name, router_doc, host_id)
            else:
                # check the gateway port document, add it if document does not exist.
                port = self.inv.get_by_id(env, router_doc['gw_port_id'])
                if not port:
                    self.add_gateway_port(env, project, network_name, router_doc, host_id)
            self.inv.set(router_doc)
        else:
            self.log.info("router document not found, aborting interface adding")

    def handle(self, env, values):
        interface = values['payload']['router_interface']
        project_id = values['_context_project_id']
        project = values['_context_project_name']
        host_id = values["publisher_id"].replace("network.", "", 1)
        port_id = interface['port_id']
        subnet_id = interface['subnet_id']
        router_id = encode_router_id(interface['id'])

        network_document = self.inv.get_by_field(env, "network", "subnet_ids",
                                                 subnet_id, get_single=True)
        if not network_document:
            self.log.info("network document not found, aborting interface adding")
            return EventResult(result=False, retry=True)
        network_name = network_document['name']
        network_id = network_document['id']

        # add router-interface port document.
        if not ApiAccess.regions:
            fetcher = ApiFetchRegions()
            fetcher.set_env(env)
            fetcher.get(project_id)
        port_doc = EventSubnetAdd().add_port_document(env, port_id,
                                                      network_name=network_name)

        mac_address = port_doc['mac_address'] if port_doc else None

        # add vnic document
        host = self.inv.get_by_id(env, host_id)
        router_doc = self.inv.get_by_id(env, router_id)

        add_vnic_document = partial(EventPortAdd().add_vnic_document,
                                    env=env,
                                    host=host,
                                    object_id=interface['id'],
                                    object_type='router',
                                    network_name=network_name,
                                    router_name=router_doc['name'],
                                    mac_address=mac_address)

        ret = add_vnic_document()
        if ret is False:
            # try it again to fetch vnic document, vnic will be created a little bit late before CLI fetch.
            time.sleep(self.delay)
            self.log.info("Wait {} seconds, and then fetch vnic document again.".format(self.delay))
            add_vnic_document()

        # update the router document: gw_port_id, network.
        self.update_router(env, project, network_id, network_name, router_doc, host_id)

        # update vservice-vnic, vnic-network,
        FindLinksForVserviceVnics().add_links(search={"parent_id": router_id})
        scanner = Scanner()
        scanner.set_env(env)

        scanner.scan_cliques()
        self.log.info("Finished router-interface added.")

        return EventResult(result=True,
                           related_object=interface['id'],
                           display_context=network_id)
