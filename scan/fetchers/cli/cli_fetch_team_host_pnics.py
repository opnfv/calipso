###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import json
from json import JSONDecodeError

import re

from base.utils.inventory_mgr import InventoryMgr
from scan.fetchers.cli.cli_fetcher import CliFetcher


class CliFetchTeamHostPnics(CliFetcher):
    LIST_TEAMS_CMD = "systemctl list-units teamd@*"
    TEAM_DETAILS_CMD = "teamdctl {} state dump"

    TEAM_NAME_REGEX = re.compile("teamd@(.*)[.]service")

    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()

    def get(self, parent_id):
        self.log.info('{}: checking under {}'.format(self.__class__.__name__, parent_id))
        host_id = parent_id[:parent_id.rindex('-')]
        host = self.inv.get_by_id(self.get_env(), host_id)
        if not host:
            self.log.error('{}: host not found: {}'.format(self.__class__.__name__,  host_id))
            return []

        teams = self.list_teams(host_id)
        for team in teams:
            self.update_team_details(team, host_id)
            self.update_team_members(team, host_id)
        return teams

    def list_teams(self, host_id):
        lines = self.run_fetch_lines(self.LIST_TEAMS_CMD, host_id)
        teams = []
        for line in lines:
            columns = line.split(None, 4)  # Expected 5 columns (4 separators)
            if len(columns) < 4:
                continue
            team_name_match = self.TEAM_NAME_REGEX.match(columns[0])
            if not team_name_match:
                continue

            team_name = team_name_match.group(1)
            teams.append({
                "name": team_name,
                "local_name": team_name,
                "host": host_id,
                "Link detected": "{}, {}".format(columns[2], columns[3]),
                "EtherChannel": True,
                "EtherChannel Master": "",
                "members": []
            })

        return teams

    def update_team_details(self, team, host_id):
        cmd_output = self.run(self.TEAM_DETAILS_CMD.format(team['name']), host_id)
        try:
            cmd_output_json = json.loads(cmd_output)
        except JSONDecodeError as e:
            self.log.error('{}: Failed to parse json from team details output\n{}'
                           .format(self.__class__.__name__,  e))
            return

        mac_address = cmd_output_json.get('team_device', {}).get('ifinfo', {}).get('dev_addr')
        if not mac_address:
            self.log.error('{}: Mac address not found for interface: {}'
                           .format(self.__class__.__name__,  team['name']))

        team.update({
            'id': "{}-{}".format(team['name'], mac_address),
            'mac_address': mac_address,
            'team_device': cmd_output_json.get('team_device'),
            'EtherChannel Config': cmd_output_json.get('setup'),
            'EtherChannel Runtime': cmd_output_json.get('runner'),
            'members': [{"name": name, **data} for name, data in cmd_output_json.get('ports', {}).items()]
        })

        for member_data in team['members']:
            member_mac = member_data.get('ifinfo', {}).get('dev_addr')
            member_data.update({
                'id': '{}-{}'.format(member_data['name'], member_mac),
                'mac_address': member_mac
            })

    def update_team_members(self, team, host_id):
        for member_data in team['members']:
            member_doc = self.inv.find_one({
                'environment': self.get_env(),
                'host': host_id,
                'type': 'host_pnic',
                'name': member_data['name']
            })
            if not member_doc:
                self.log.error('unable to find member pNIC {} under team {}'
                               .format(member_data['name'], team['name']))
                continue

            member_doc.update({
                'EtherChannel': True,
                'EtherChannel Master': team['id']
            })
            self.inv.set(member_doc)
