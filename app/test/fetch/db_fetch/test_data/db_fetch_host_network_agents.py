CONFIG_WITH_MECHANISM_DRIVERS = {
    'mechanism_drivers': [
        "OVS"
    ]
}

CONFIG_WITHOUT_MECHANISM_DRIVERS = {
    'mechanism_drivers': [

    ]
}

NETWORK_AGENT_FOLDER_ID = 'node-6.cisco.com-network_agents'

NETWORK_AGENT = [
    {
        'configurations': '{}',
        'id': '1764430c-c09e-4717-86fa-c04350b1fcbb',
        'binary': 'neutron-openvswitch-agent',
    },
    {
        'configurations': '{}',
        'id': '2c2ddfee-91f9-47da-bd65-aceecd998b7c',
        'binary': 'neutron-dhcp-agent',
    }
]

NETWORK_AGENT_WITH_MECHANISM_DRIVERS_IN_CONFIG_RESULTS = [
    {
        'configurations': {},
        'id': 'OVS-1764430c-c09e-4717-86fa-c04350b1fcbb',
        'binary': 'neutron-openvswitch-agent',
        'name': 'neutron-openvswitch-agent'
    },
    {
        'configurations': {},
        'id': 'OVS-2c2ddfee-91f9-47da-bd65-aceecd998b7c',
        'binary': 'neutron-dhcp-agent',
        'name': 'neutron-dhcp-agent'
    }
]

NETWORK_AGENT_WITHOUT_MECHANISM_DRIVERS_IN_CONFIG_RESULTS = [
    {
        'configurations': {},
        'id': 'network_agent-1764430c-c09e-4717-86fa-c04350b1fcbb',
        'binary': 'neutron-openvswitch-agent',
        'name': 'neutron-openvswitch-agent'
    },
    {
        'configurations': {},
        'id': 'network_agent-2c2ddfee-91f9-47da-bd65-aceecd998b7c',
        'binary': 'neutron-dhcp-agent',
        'name': 'neutron-dhcp-agent'
    }
]
