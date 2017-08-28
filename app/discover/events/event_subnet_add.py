###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import datetime

from discover.events.event_base import EventBase, EventResult
from discover.events.event_port_add import EventPortAdd
from discover.fetchers.api.api_access import ApiAccess
from discover.fetchers.api.api_fetch_port import ApiFetchPort
from discover.fetchers.api.api_fetch_regions import ApiFetchRegions
from discover.fetchers.db.db_fetch_port import DbFetchPort
from discover.find_links_for_pnics import FindLinksForPnics
from discover.find_links_for_vservice_vnics import FindLinksForVserviceVnics
from discover.scanner import Scanner


class EventSubnetAdd(EventBase):

    def add_port_document(self, env, port_id, network_name=None, project_name=''):
        # when add router-interface port, network_name need to be given to enhance efficiency.
        # when add gateway port, project_name need to be specified, cause this type of port
        # document does not has project attribute. In this case, network_name should not be provided.

        fetcher = ApiFetchPort()
        fetcher.set_env(env)
        ports = fetcher.get(port_id)

        if ports:
            port = ports[0]
            project_id = port['tenant_id']
            network_id = port['network_id']

            if not network_name:
                network = self.inv.get_by_id(env, network_id)
                network_name = network['name']

            port['type'] = "port"
            port['environment'] = env
            port_id = port['id']
            port['id_path'] = "%s/%s-projects/%s/%s-networks/%s/%s-ports/%s" % \
                              (env, env, project_id, project_id, network_id, network_id, port_id)
            port['last_scanned'] = datetime.datetime.utcnow()
            if 'project' in port:
                project_name = port['project']
            port['name_path'] = "/%s/Projects/%s/Networks/%s/Ports/%s" % \
                                (env, project_name, network_name, port_id)
            self.inv.set(port)
            self.log.info("add port document for port:%s" % port_id)
            return port
        return False

    def add_ports_folder(self, env, project_id, network_id, network_name):
        port_folder = {
            "id": network_id + "-ports",
            "create_object": True,
            "name": "Ports",
            "text": "Ports",
            "type": "ports_folder",
            "parent_id": network_id,
            "parent_type": "network",
            'environment': env,
            'id_path': "%s/%s-projects/%s/%s-networks/%s/%s-ports/" % (env, env, project_id, project_id,
                                                                       network_id, network_id),
            'name_path': "/%s/Projects/%s/Networks/%s/Ports" % (env, project_id, network_name),
            "show_in_tree": True,
            "last_scanned": datetime.datetime.utcnow(),
            "object_name": "Ports",
        }

        self.inv.set(port_folder)

    def add_children_documents(self, env, project_id, network_id, network_name, host_id):
        # generate port folder data.
        self.add_ports_folder(env, project_id, network_id, network_name)

        # get ports ID.
        port_id = DbFetchPort().get_id(network_id)

        # add specific ports documents.
        self.add_port_document(env, port_id, network_name=network_name)

        port_handler = EventPortAdd()

        # add network_services_folder document.
        port_handler.add_network_services_folder(env, project_id, network_id, network_name)

        # add dhcp vservice document.
        host = self.inv.get_by_id(env, host_id)

        port_handler.add_dhcp_document(env, host, network_id, network_name)

        # add vnics folder.
        port_handler.add_vnics_folder(env, host, network_id, network_name)

        # add vnic docuemnt.
        port_handler.add_vnic_document(env, host, network_id, network_name)

    def handle(self, env, notification):
        # check for network document.
        subnet = notification['payload']['subnet']
        project_id = subnet['tenant_id']
        network_id = subnet['network_id']
        if 'id' not in subnet:
            self.log.info('Subnet payload doesn\'t have id, aborting subnet add')
            return EventResult(result=False, retry=False)

        network_document = self.inv.get_by_id(env, network_id)
        if not network_document:
            self.log.info('network document does not exist, aborting subnet add')
            return EventResult(result=False, retry=True)
        network_name = network_document['name']

        # build subnet document for adding network
        if subnet['cidr'] not in network_document['cidrs']:
            network_document['cidrs'].append(subnet['cidr'])
        if not network_document.get('subnets'):
            network_document['subnets'] = {}

        network_document['subnets'][subnet['name']] = subnet
        if subnet['id'] not in network_document['subnet_ids']:
            network_document['subnet_ids'].append(subnet['id'])
        self.inv.set(network_document)

        # Check DHCP enable, if true, scan network.
        if subnet['enable_dhcp'] is True:
            # update network
            if len(ApiAccess.regions) == 0:
                fetcher = ApiFetchRegions()
                fetcher.set_env(env)
                fetcher.get(None)

            self.log.info("add new subnet.")
            host_id = notification["publisher_id"].replace("network.", "", 1)
            self.add_children_documents(env, project_id, network_id, network_name, host_id)

        # scan links and cliques
        self.log.info("scanning for links")
        FindLinksForPnics().add_links()
        FindLinksForVserviceVnics().add_links(search={"parent_id": "qdhcp-%s-vnics" % network_id})

        scanner = Scanner()
        scanner.set_env(env)
        scanner.scan_cliques()
        self.log.info("Finished subnet added.")
        return EventResult(result=True,
                           related_object=subnet['id'],
                           display_context=network_id)
