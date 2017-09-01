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
from discover.fetchers.api.api_fetch_host_instances import ApiFetchHostInstances
from discover.fetchers.cli.cli_fetch_instance_vnics import CliFetchInstanceVnics
from discover.fetchers.cli.cli_fetch_instance_vnics_vpp import \
    CliFetchInstanceVnicsVpp
from discover.fetchers.cli.cli_fetch_vservice_vnics import CliFetchVserviceVnics
from discover.link_finders.find_links_for_instance_vnics import \
    FindLinksForInstanceVnics
from discover.link_finders.find_links_for_vedges import FindLinksForVedges
from discover.scanner import Scanner


class EventPortAdd(EventBase):

    def get_name_by_id(self, object_id):
        item = self.inv.get_by_id(self.env, object_id)
        if item:
            return item['name']
        return None

    def add_port_document(self, env, project_name, project_id, network_name, network_id, port):
        # add other data for port document
        port['type'] = 'port'
        port['environment'] = env

        port['parent_id'] = port['network_id'] + '-ports'
        port['parent_text'] = 'Ports'
        port['parent_type'] = 'ports_folder'

        port['name'] = port['mac_address']
        port['object'] = port['name']
        port['project'] = project_name

        port['id_path'] = "{}/{}-projects/{}/{}-networks/{}/{}-ports/{}" \
                          .format(env, env,
                                  project_id, project_id,
                                  network_id, network_id, port['id'])
        port['name_path'] = "/{}/Projects/{}/Networks/{}/Ports/{}" \
                            .format(env, project_name, network_name, port['id'])

        port['show_in_tree'] = True
        port['last_scanned'] = datetime.datetime.utcnow()
        self.inv.set(port)
        self.log.info("add port document for port: {}".format(port['id']))

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
            'id_path': "{}/{}-projects/{}/{}-networks/{}/{}-ports/"
                       .format(env, env, project_id, project_id,
                               network_id, network_id),
            'name_path': "/{}/Projects/{}/Networks/{}/Ports"
                       .format(env, project_id, network_name),
            "show_in_tree": True,
            "last_scanned": datetime.datetime.utcnow(),
            "object_name": "Ports",
        }
        self.inv.set(port_folder)
        self.log.info("add ports_folder document for network: {}.".format(network_id))

    def add_network_services_folder(self, env, project_id, network_id, network_name):
        network_services_folder = {
            "create_object": True,
            "environment": env,
            "id": network_id + "-network_services",
            "id_path": "{}/{}-projects/{}/{}-networks/{}/{}-network_services/"
                       .format(env, env, project_id, project_id,
                               network_id, network_id),
            "last_scanned": datetime.datetime.utcnow(),
            "name": "Network vServices",
            "name_path": "/{}/Projects/{}/Networks/{}/Network vServices"
                         .format(env, project_id, network_name),
            "object_name": "Network vServices",
            "parent_id": network_id,
            "parent_type": "network",
            "show_in_tree": True,
            "text": "Network vServices",
            "type": "network_services_folder"
        }
        self.inv.set(network_services_folder)
        self.log.info("add network services folder for network:{}".format(network_id))

    def add_dhcp_document(self, env, host, network_id, network_name):
        dhcp_document = {
            "environment": env,
            "host": host['id'],
            "id": "qdhcp-" + network_id,
            "id_path": "{}/{}-vservices/{}-vservices-dhcps/qdhcp-{}"
                       .format(host['id_path'], host['id'],
                               host['id'], network_id),
            "last_scanned": datetime.datetime.utcnow(),
            "local_service_id": "qdhcp-" + network_id,
            "name": "dhcp-" + network_name,
            "name_path": host['name_path'] + "/Vservices/DHCP servers/dhcp-" + network_name,
            "network": [network_id],
            "object_name": "dhcp-" + network_name,
            "parent_id": host['id'] + "-vservices-dhcps",
            "parent_text": "DHCP servers",
            "parent_type": "vservice_dhcps_folder",
            "service_type": "dhcp",
            "show_in_tree": True,
            "type": "vservice"
        }
        self.inv.set(dhcp_document)
        self.log.info("add DHCP document for network: {}.".format(network_id))

    # This method has dynamic usages, take caution when changing its signature
    def add_vnics_folder(self,
                         env, host,
                         object_id, network_name='',
                         object_type="dhcp", router_name=''):
        # when vservice is DHCP, id = network_id,
        # when vservice is router, id = router_id
        type_map = {"dhcp": ('DHCP servers', 'dhcp-' + network_name),
                    "router": ('Gateways', router_name)}

        vnics_folder = {
            "environment": env,
            "id": "q{}-{}-vnics".format(object_type, object_id),
            "id_path": "{}/{}-vservices/{}-vservices-{}s/q{}-{}/q{}-{}-vnics"
                       .format(host['id_path'], host['id'], host['id'],
                               object_type, object_type, object_id,
                               object_type, object_id),
            "last_scanned": datetime.datetime.utcnow(),
            "name": "q{}-{}-vnics".format(object_type, object_id),
            "name_path": "{}/Vservices/{}/{}/vNICs"
                         .format(host['name_path'],
                                 type_map[object_type][0],
                                 type_map[object_type][1]),
            "object_name": "vNICs",
            "parent_id": "q{}-{}".format(object_type, object_id),
            "parent_type": "vservice",
            "show_in_tree": True,
            "text": "vNICs",
            "type": "vnics_folder"
        }
        self.inv.set(vnics_folder)
        self.log.info("add vnics_folder document for q{}-{}-vnics"
                      .format(object_type, object_id))

    # This method has dynamic usages, take caution when changing its signature
    def add_vnic_document(self,
                          env, host,
                          object_id, network_name='',
                          object_type='dhcp', router_name='',
                          mac_address=None):
        # when vservice is DHCP, id = network_id,
        # when vservice is router, id = router_id
        type_map = {"dhcp": ('DHCP servers', 'dhcp-' + network_name),
                    "router": ('Gateways', router_name)}

        fetcher = CliFetchVserviceVnics()
        fetcher.set_env(env)
        namespace = 'q{}-{}'.format(object_type, object_id)
        vnic_documents = fetcher.handle_service(host['id'], namespace, enable_cache=False)
        if not vnic_documents:
            self.log.info("Vnic document not found in namespace.")
            return False

        if mac_address is not None:
            for doc in vnic_documents:
                if doc['mac_address'] == mac_address:
                    # add a specific vnic document.
                    doc["environment"] = env
                    doc["id_path"] = "{}/{}-vservices/{}-vservices-{}s/{}/{}-vnics/{}"\
                                     .format(host['id_path'], host['id'],
                                             host['id'], object_type, namespace,
                                             namespace, doc["id"])
                    doc["name_path"] = "{}/Vservices/{}/{}/vNICs/{}" \
                                       .format(host['name_path'],
                                               type_map[object_type][0],
                                               type_map[object_type][1],
                                               doc["id"])
                    self.inv.set(doc)
                    self.log.info("add vnic document with mac_address: {}."
                                  .format(mac_address))
                    return True

            self.log.info("Can not find vnic document by mac_address: {}"
                          .format(mac_address))
            return False
        else:
            for doc in vnic_documents:
                # add all vnic documents.
                doc["environment"] = env
                doc["id_path"] = "{}/{}-vservices/{}-vservices-{}s/{}/{}-vnics/{}" \
                                 .format(host['id_path'], host['id'],
                                         host['id'], object_type,
                                         namespace, namespace, doc["id"])
                doc["name_path"] = "{}/Vservices/{}/{}/vNICs/{}" \
                                   .format(host['name_path'],
                                           type_map[object_type][0],
                                           type_map[object_type][1],
                                           doc["id"])
                self.inv.set(doc)
                self.log.info("add vnic document with mac_address: {}."
                              .format(doc["mac_address"]))
            return True

    def handle_dhcp_device(self, env, notification, network_id, network_name, mac_address=None):
        # add dhcp vservice document.
        host_id = notification["publisher_id"].replace("network.", "", 1)
        host = self.inv.get_by_id(env, host_id)

        self.add_dhcp_document(env, host, network_id, network_name)

        # add vnics folder.
        self.add_vnics_folder(env, host, network_id, network_name)

        # add vnic document.
        self.add_vnic_document(env, host, network_id, network_name, mac_address=mac_address)

    def handle(self, env, notification):
        project = notification['_context_project_name']
        project_id = notification['_context_project_id']
        payload = notification['payload']
        port = payload['port']
        network_id = port['network_id']
        network_name = self.get_name_by_id(network_id)
        mac_address = port['mac_address']

        # check ports folder document.
        ports_folder = self.inv.get_by_id(env, network_id + '-ports')
        if not ports_folder:
            self.log.info("ports folder not found, add ports folder first.")
            self.add_ports_folder(env, project_id, network_id, network_name)
        self.add_port_document(env, project, project_id, network_name, network_id, port)

        # update the port related documents.
        if 'compute' in port['device_owner']:
            # update the instance related document.
            host_id = port['binding:host_id']
            instance_id = port['device_id']
            old_instance_doc = self.inv.get_by_id(env, instance_id)
            instances_root_id = host_id + '-instances'
            instances_root = self.inv.get_by_id(env, instances_root_id)
            if not instances_root:
                self.log.info('instance document not found, aborting port adding')
                return EventResult(result=False, retry=True)

            # update instance
            instance_fetcher = ApiFetchHostInstances()
            instance_fetcher.set_env(env)
            instance_docs = instance_fetcher.get(host_id + '-')
            instance = next(filter(lambda i: i['id'] == instance_id, instance_docs), None)

            if instance:
                old_instance_doc['network_info'] = instance['network_info']
                old_instance_doc['network'] = instance['network']
                if old_instance_doc.get('mac_address') is None:
                    old_instance_doc['mac_address'] = mac_address

                self.inv.set(old_instance_doc)
                self.log.info("update instance document")

            # add vnic document.
            if port['binding:vif_type'] == 'vpp':
                vnic_fetcher = CliFetchInstanceVnicsVpp()
            else:
                # set ovs as default type.
                vnic_fetcher = CliFetchInstanceVnics()

            vnic_fetcher.set_env(env)
            vnic_docs = vnic_fetcher.get(instance_id + '-')
            vnic = next(filter(lambda vnic: vnic['mac_address'] == mac_address, vnic_docs), None)

            if vnic:
                vnic['environment'] = env
                vnic['type'] = 'vnic'
                vnic['name_path'] = old_instance_doc['name_path'] + '/vNICs/' + vnic['name']
                vnic['id_path'] = '{}/{}/{}'.format(old_instance_doc['id_path'],
                                                    old_instance_doc['id'],
                                                    vnic['name'])
                self.inv.set(vnic)
                self.log.info("add instance-vnic document, mac_address: {}"
                              .format(mac_address))

            self.log.info("scanning for links")
            fetchers_implementing_add_links = [FindLinksForInstanceVnics(), FindLinksForVedges()]
            for fetcher in fetchers_implementing_add_links:
                fetcher.add_links()
            scanner = Scanner()
            scanner.set_env(env)
            scanner.scan_cliques()

        port_document = self.inv.get_by_id(env, port['id'])
        if not port_document:
            self.log.error("Port {} failed to add".format(port['id']))
            return EventResult(result=False, retry=True)

        return EventResult(result=True,
                           related_object=port['id'],
                           display_context=network_id)
