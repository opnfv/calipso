###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
ENVIRONMENT = {
    'name': 'test-env',
    'environment_type': 'OpenStack',
    'distribution': 'Mirantis',
    'distribution_version': '9.0',
    'mechanism_drivers': ['OVS'],
    'type_drivers': 'vxlan'
}

MATCH_CLIQUE_TYPE = ENVIRONMENT.copy()
MATCH_CLIQUE_TYPE['environment'] = MATCH_CLIQUE_TYPE['name']
MATCH_CLIQUE_TYPE['mechanism_drivers'] = MATCH_CLIQUE_TYPE['mechanism_drivers'][0]
del MATCH_CLIQUE_TYPE['name']

MISMATCH_CLIQUE_TYPE = {
    'environment': 'test-env-2',
    'environment_type': 'Kubernetes',
    'distribution': 'Kubernetes',
    'distribution_version': '1.9',
    'mechanism_drivers': 'Flannel',
    'type_drivers': 'vlan'
}


def get_configuration(matches=None, mismatches=None):
    clique_type = {'link_types': []}
    if matches:
        clique_type.update({
            key: MATCH_CLIQUE_TYPE[key]
            for key in matches
            if key in MATCH_CLIQUE_TYPE
        })
    if mismatches:
        clique_type.update({
            key: MISMATCH_CLIQUE_TYPE[key]
            for key in mismatches
            if key in MISMATCH_CLIQUE_TYPE
        })
    return clique_type


CLIQUE_TYPES = [
    {
        'name': 'environment match',
        'clique_type': get_configuration(matches=['environment']),
        'score': 2**6
    },
    {
        'name': 'distribution and version match',
        'clique_type': get_configuration(matches=['environment_type',
                                                  'distribution',
                                                  'distribution_version']),
        'score': 2**5 + 2**4
    },
    {
        'name': 'distribution match',
        'clique_type': get_configuration(matches=['environment_type',
                                                  'distribution']),
        'score': 2**5
    },
    {
        'name': 'mechanism drivers match',
        'clique_type': get_configuration(matches=['environment_type',
                                                  'mechanism_drivers']),
        'score': 2**3
    },
    {
        'name': 'type drivers match',
        'clique_type': get_configuration(matches=['environment_type',
                                                  'type_drivers']),
        'score': 2**2
    },
    {
        'name': 'ANY fallback',
        'clique_type': {
            'environment': 'ANY',
            'link_types': []
        },
        'score': 2**0
    },
    {
        'name': 'Full configuration match',
        'clique_type': get_configuration(matches=['environment_type',
                                                  'distribution',
                                                  'distribution_version',
                                                  'mechanism_drivers',
                                                  'type_drivers']),
        'score': 2**5 + 2**4 + 2**3 + 2**2
    },
    {
        'name': 'Partial configuration match (drivers)',
        'clique_type': get_configuration(matches=['environment_type',
                                                  'mechanism_drivers',
                                                  'type_drivers']),
        'score': 2**3 + 2**2
    },
    {
        'name': 'No environment name match',
        'clique_type': get_configuration(mismatches=['environment']),
        'score': 0
    },
    {
        'name': 'No configuration match',
        'clique_type': get_configuration(mismatches=['distribution',
                                                     'distribution_version',
                                                     'mechanism_drivers',
                                                     'type_drivers']),
        'score': 0
    },
    {
        'name': 'No environment type match',
        'clique_type': get_configuration(mismatches=['environment_type',
                                                     'distribution',
                                                     'distribution_version',
                                                     'mechanism_drivers',
                                                     'type_drivers']),
        'score': 0
    },
    {
        'name': 'Distribution mismatch',
        'clique_type': get_configuration(matches=['environment_type',
                                                  'distribution_version',
                                                  'mechanism_drivers',
                                                  'type_drivers'],
                                         mismatches=['distribution']),
        'score': 0
    },
    {
        'name': 'Distribution version mismatch',
        'clique_type': get_configuration(matches=['environment_type',
                                                  'distribution',
                                                  'mechanism_drivers',
                                                  'type_drivers'],
                                         mismatches=['distribution_version']),
        'score': 0
    },
    {
        'name': 'Mechanism drivers mismatch',
        'clique_type': get_configuration(matches=['environment_type',
                                                  'distribution_version',
                                                  'distribution',
                                                  'type_drivers'],
                                         mismatches=['mechanism_drivers']),
        'score': 0
    },
    {
        'name': 'Type drivers mismatch',
        'clique_type': get_configuration(matches=['environment_type',
                                                  'distribution_version',
                                                  'distribution',
                                                  'mechanism_drivers'],
                                         mismatches=['type_drivers']),
        'score': 0
    },
]
