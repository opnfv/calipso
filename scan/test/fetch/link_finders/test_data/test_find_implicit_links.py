###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
ENV = 'env1'
CLIQUE_CONSTRAINTS = [
    {
        'focal_point_type': 'instance',
        'constraints': ['network']
    },
    {
        'focal_point_type': 'dummy1',
        'constraints': []
    },
    {
        'focal_point_type': 'dummy2',
        'constraints': ['network', 'dummy_constraint']
    },
    {
        'focal_point_type': 'dummy3',
        'constraints': ['dummy_constraint2']
    }
]
CONSTRAINTS = ['network', 'dummy_constraint', 'dummy_constraint2']

LINK_ATTRIBUTES_NONE = {}
LINK_ATTRIBUTES_NONE_2 = {}
LINK_ATTRIBUTES_EMPTY = {'attributes': []}
LINK_ATTR_V1 = {'attributes': {'network': 'v1'}}
LINK_ATTR_V1_2 = {'attributes': {'network': 'v1'}}
LINK_ATTR_V2 = {'attributes': {'network': 'v2'}}
LINK_ATTR_V1_AND_A2V2 = {'attributes': {'network': 'v1', 'attr2': 'v2'}}

LINK_TYPE_1 = {
    'link_type': 'instance-vnic',
    'source_id': 'instance1',
    'target_id': 'vnic1'
}
LINK_TYPE_1_REVERSED = {
    'link_type': 'instance-vnic',
    'source_id': 'vnic1',
    'target_id': 'instance1'
}
LINK_TYPE_1_2 = {
    'link_type': 'instance-vnic',
    'source_id': 'instance1',
    'target_id': 'vnic2'
}
LINK_TYPE_2 = {
    'link_type': 'vnic-vconnector',
    'source_id': 'vnic1',
    'target_id': 'vconnector1'
}
LINK_TYPE_3 = {
    'implicit': True,
    'link_type': 'instance-vconnector',
    'source_id': 'instance1',
    'target_id': 'vconnector1'
}
LINK_TYPE_4_NET1 = {
    'environment': ENV,
    'implicit': True,
    'link_type': 'instance-host_pnic',
    'source': 'instance1_dbid',
    'source_id': 'instance1',
    'target': 'host_pnic1_dbid',
    'target_id': 'host_pnic1',
    'host': 'host1',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID1'}
}
LINK_TYPE_5_NET2 = {
    'environment': ENV,
    'link_type': 'host_pnic-switch',
    'source_id': 'host_pnic1',
    'target': 'switch1_dbid',
    'target_id': 'switch1',
    'host': 'host2',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID2'}
}
LINK_TYPE_6_NET1 = {
    'environment': ENV,
    'link_type': 'host_pnic-switch',
    'source': 'host_pnic1_dbid',
    'source_id': 'host_pnic1',
    'target': 'switch2_dbid',
    'target_id': 'switch2',
    'host': 'host1',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID1'}
}
LINK_TYPE_7_NET1 = {
    'environment': ENV,
    'implicit': True,
    'link_type': 'instance-switch',
    'source': 'instance1_dbid',
    'source_id': 'instance1',
    'target': 'switch2_dbid',
    'target_id': 'switch2',
    'host': 'host1',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID1'}
}

LINK_FULL_A2B_EXPLICIT = {
    'environment': ENV,
    'link_type': 'instance-vnic',
    'source': 'instance1_dbid',
    'source_id': 'instance1',
    'target': 'vnic1_dbid',
    'target_id': 'vnic1',
    'host': 'host1',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID1'}
}
LINK_FULL_B2C_EXPLICIT = {
    'environment': ENV,
    'link_type': 'vnic-vconnector',
    'source': 'vnic1_dbid',
    'source_id': 'vnic1',
    'target': 'vconnector1_dbid',
    'target_id': 'vconnector1',
    'host': 'host1',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID1'}
}
LINK_FULL_C2D_EXPLICIT = {
    'environment': ENV,
    'link_type': 'vconnector-vedge',
    'source': 'vconnector1_dbid',
    'source_id': 'vconnector1',
    'target': 'vedge1_dbid',
    'target_id': 'vedge1',
    'host': 'host1',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID1'}
}
LINK_FULL_D2E_EXPLICIT = {
    'environment': ENV,
    'link_type': 'vedge-otep',
    'source': 'vedge1_dbid',
    'source_id': 'vedge1',
    'target': 'otep1_dbid',
    'target_id': 'otep1',
    'host': 'host1',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID1'}
}
LINK_FULL_C2E_EXPLICIT = {
    'environment': ENV,
    'link_type': 'vconnector-otep',
    'source': 'vconnector1_dbid',
    'source_id': 'vconnector1',
    'target': 'otep1_dbid',
    'target_id': 'otep1',
    'host': 'host1',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID1'}
}
LINK_FULL_A2C = {
    'environment': ENV,
    'implicit': True,
    'link_type': 'instance-vconnector',
    'source': 'instance1_dbid',
    'source_id': 'instance1',
    'target': 'vconnector1_dbid',
    'target_id': 'vconnector1',
    'host': 'host1',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID1'}
}
LINK_FULL_B2D = {
    'environment': ENV,
    'implicit': True,
    'link_type': 'vnic-vedge',
    'source': 'vnic1_dbid',
    'source_id': 'vnic1',
    'target': 'vedge1_dbid',
    'target_id': 'vedge1',
    'host': 'host1',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID1'}
}
LINK_FULL_A2D = {
    'environment': ENV,
    'implicit': True,
    'link_type': 'instance-vedge',
    'source': 'instance1_dbid',
    'source_id': 'instance1',
    'target': 'vedge1_dbid',
    'target_id': 'vedge1',
    'host': 'host1',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID1'}
}
LINK_FULL_B2E = {
    'environment': ENV,
    'implicit': True,
    'link_type': 'vnic-otep',
    'source': 'vnic1_dbid',
    'source_id': 'vnic1',
    'target': 'otep1_dbid',
    'target_id': 'otep1',
    'host': 'host1',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID1'}
}
LINK_FULL_A2E = {
    'environment': ENV,
    'implicit': True,
    'link_type': 'instance-otep',
    'source': 'instance1_dbid',
    'source_id': 'instance1',
    'target': 'otep1_dbid',
    'target_id': 'otep1',
    'host': 'host1',
    'link_name': '',
    'state': 'up',
    'source_label': '',
    'target_label': '',
    'link_weight': 0,
    'attributes': {'network': 'netID1'}
}
BASE_LINKS = [
    {'pass': 0, 'link': LINK_FULL_A2B_EXPLICIT},
    {'pass': 0, 'link': LINK_FULL_B2C_EXPLICIT},
    {'pass': 0, 'link': LINK_FULL_C2D_EXPLICIT},
    {'pass': 0, 'link': LINK_FULL_D2E_EXPLICIT},
    # this one tests that existing explicit links are not overwritten if
    # they are also achievable implicitly
    {'pass': 0, 'link': LINK_FULL_C2E_EXPLICIT},
]
IMPLICIT_LINKS = [
    {'pass': 1, 'link': LINK_FULL_A2C},
    {'pass': 1, 'link': LINK_FULL_B2D},
    {'pass': 1, 'link': LINK_FULL_B2E},
    {'pass': 2, 'link': LINK_FULL_A2D},
    {'pass': 2, 'link': LINK_FULL_A2E},
]
