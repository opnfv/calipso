###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.utils.special_char_converter import SpecialCharConverter
from monitoring.setup.monitoring_handler import MonitoringHandler


class MonitoringCheckHandler(MonitoringHandler, SpecialCharConverter):

    def __init__(self, env):
        super().__init__(env)

    # add monitoring setup on remote host for given object
    def create_monitoring_for_object(self, o, values):
        self.replacements.update(self.env_monitoring_config)
        self.replacements.update(values)
        if 'host' in o:
            host = self.inv.get_by_id(self.env, o['host'])
            if host and 'ip_address' in host:
                self.replacements['client_ip'] = host['ip_address']
        type_str = values['check_type'] if 'check_type' in values else \
            (o['type'] if 'type' in o else 'link_' + o['link_type'])
        file_type = 'client_check_' + type_str + '.json'
        content = self.prepare_config_file(
            file_type,
            {'side': 'client', 'type': file_type})
        # need to put this content inside client.json file
        host = values['host'] if 'host' in values \
            else o['host'] if 'host' in o else ''
        sub_dir = '/host/' + host
        client_file = 'client.json'
        client_file_content = self.get_config_from_db(host, client_file)
        # merge checks attribute from current content into client.json
        checks = client_file_content['config']['checks'] \
            if (client_file_content and
                'checks' in client_file_content['config']) \
            else {}
        checks.update(content.get('config', {}).get('checks', {}))
        if client_file_content:
            client_file_content['config']['checks'] = checks
        else:
            client_file_content = {
                'config': {
                    'checks': checks
                }
            }
        content = client_file_content
        self.write_config_file(client_file, sub_dir, host, content)

    def get_check_from_db(self, o, postfix=''):
        client_config = self.get_config_from_db(o. get('host', ''),
                                                'client.json')
        if not client_config:
            return {}
        checks = client_config.get('config', {}).get('checks', {})
        objid = self.encode_special_characters(o.get('id', ''))
        object_check_id = '{}_{}{}'.format(o.get('type'), objid, postfix)
        check = checks.get(object_check_id, {})
        return check
