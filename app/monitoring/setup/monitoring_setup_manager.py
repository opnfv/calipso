###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
# handle adding of monitoring setup as needed

from monitoring.setup.monitoring_handler import MonitoringHandler
from monitoring.setup.monitoring_host import MonitoringHost
from monitoring.setup.monitoring_link_vnic_vconnector \
    import MonitoringLinkVnicVconnector
from monitoring.setup.monitoring_pnic import MonitoringPnic
from monitoring.setup.monitoring_otep import MonitoringOtep
from monitoring.setup.monitoring_vedge import MonitoringVedge
from monitoring.setup.monitoring_vnic import MonitoringVnic
from monitoring.setup.monitoring_vservice import MonitoringVservice


class MonitoringSetupManager(MonitoringHandler):

    object_handlers = None

    def __init__(self, env):
        super().__init__(env)
        self.object_handlers = {
            "host": MonitoringHost(env),
            "otep": MonitoringOtep(env),
            "vedge": MonitoringVedge(env),
            "pnic": MonitoringPnic(env),
            "vnic": MonitoringVnic(env),
            "vservice": MonitoringVservice(env),
            "vnic-vconnector": MonitoringLinkVnicVconnector(env)}

    # add monitoring setup to Sensu server
    def server_setup(self):
        if self.provision == self.provision_levels['none']:
            self.log.debug('Monitoring config setup skipped')
            return
        sensu_server_files = [
            'transport.json',
            'client.json',
            'rabbitmq.json',
            'handlers.json',
            'redis.json',
            'api.json'
        ]
        conf = self.env_monitoring_config
        is_container = bool(conf.get('ssh_user', ''))
        server_host = conf['server_ip']
        sub_dir = 'server'
        self.replacements.update(conf)
        for file_name in sensu_server_files:
            content = self.prepare_config_file(file_name, {'side': 'server'})
            self.write_config_file(file_name, sub_dir, server_host, content,
                                   is_container=is_container, is_server=True)
        # restart sensu server and Uchiwa services
        # so it takes the new setup
        self.restart_service(host=server_host, service='sensu-server',
                             is_server=True,
                             msg='restart sensu-server on {}'
                             .format(server_host))
        self.restart_service(host=server_host, service='uchiwa',
                             is_server=True,
                             msg='restart uchiwa on {}'
                             .format(server_host))
        self.configuration.update_env({'monitoring_setup_done': True})

    # add setup for inventory object
    def create_setup(self, o):
        if self.provision == self.provision_levels['none']:
            self.log.debug('Monitoring config setup skipped')
            return
        type_attribute = 'type' if 'type' in o else 'link_type'
        type_value = o[type_attribute]
        object_handler = self.object_handlers.get(type_value)
        if object_handler:
            object_handler.create_setup(o)

    def simulate_track_changes(self):
        self.add_changes_for_all_clients()
