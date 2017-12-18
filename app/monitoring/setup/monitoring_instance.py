###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from monitoring.setup.monitoring_simple_object import MonitoringSimpleObject


class MonitoringInstance(MonitoringSimpleObject):

    def __init__(self, env):
        super().__init__(env)

    # monitoring setup for instance can only be done after vNIC is found
    # and network for vNIC is set, so the first call will not do anything
    def create_setup(self, instance: dict):
        vnics = self.inv.find_items({
            'environment': self.get_env(),
            'type': 'vnic',
            'vnic_type': 'instance_vnic',
            'id_path': {'$regex': '^{}/'.format(instance['id_path'])}
        })
        for vnic in vnics:
            self.add_instance_communication_monitoring(instance, vnic)

    # for instance we keep list of instance vNICs and services to use in call
    # to check_instance_communications.py
    # add this vNIC to the list with the corresponding
    def add_instance_communication_monitoring(self, instance: dict, vnic: dict):
        service = self.get_service_for_vnic(vnic)
        if not service:
            return
        check = self.get_check_from_db(instance)
        services_and_vnics = check.get('command', '')
        if services_and_vnics:
            services_and_vnics = \
                services_and_vnics[services_and_vnics.index('.py')+4:]
        services_and_vnics_list = \
            services_and_vnics.split(';') if services_and_vnics \
            else []
        service_and_vnic = '{},{}'.format(service.get('local_service_id', ''),
                                          vnic.get('id'))
        if service_and_vnic in services_and_vnics_list:
            return  # we already have this tuple define
        services_and_vnics_list.append(service_and_vnic)
        values = {
            'objtype': 'instance',
            'objid': self.encode_special_characters(instance['id']),
            'host': service['host'],
            'services_and_vnics': ';'.join(services_and_vnics_list)
        }
        self.create_monitoring_for_object(instance, values)

    def get_service_for_vnic(self, vnic: dict) -> dict:
        services = self.inv.find_items({'environment': self.get_env(),
                                        'type': 'vservice',
                                        'network': vnic.get('network', '')})
        if not services:
            return {}
        dhcp = next(s for s in services if s.get('service_type') == 'dhcp')
        if dhcp:
            return dhcp  # If we have both DHCP and router, return the DHCP
        return services[0]  # currently only DHCP and router services
