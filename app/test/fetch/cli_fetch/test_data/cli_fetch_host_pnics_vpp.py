ID = "node-4.cisco.com-VPP-folders"
VEDGES = [
    { 
    "agent_type": "Open vSwitch agent", 
    "binary": "neutron-openvswitch-agent", 
    "configurations" : {
        "tunneling_ip": "192.168.2.3", 
        "arp_responder_enabled" : True, 
        "extensions" : [

        ], 
        "l2_population" : True, 
        "enable_distributed_routing" : False, 
        "bridge_mappings" : {
            "physnet1": "br-floating"
        }, 
        "log_agent_heartbeats" : False, 
        "tunnel_types" : [
            "vxlan"
        ], 
        "in_distributed_mode" : False
    }, 
    "description" : None, 
    "environment": "Mirantis-Liberty-Xiaocong", 
    "host": "node-6.cisco.com", 
    "id": "1764430c-c09e-4717-86fa-c04350b1fcbb", 
    "id_path": "/Mirantis-Liberty-Xiaocong/Mirantis-Liberty-Xiaocong-regions/RegionOne/RegionOne-availability_zones/internal/node-6.cisco.com/node-6.cisco.com-vedges/1764430c-c09e-4717-86fa-c04350b1fcbb", 
    "name": "node-6.cisco.com-OVS", 
    "name_path": "/Mirantis-Liberty-Xiaocong/Regions/RegionOne/Availability Zones/internal/node-6.cisco.com/vEdges/node-6.cisco.com-OVS", 
    "object_name": "node-6.cisco.com-OVS", 
    "parent_id": "node-6.cisco.com-vedges", 
    "parent_type": "vedges_folder", 
    "ports" : {
        "TenGigabitEthernet-g-63489f34-af" : {
            "id": "8", 
            "name": "qg-63489f34-af", 
            "internal" : True, 
            "tag": "2",
            "host": "node-4.cisco.com",
            "state": "up"
        }, 
        "qr-3ff411a2-54" : {
            "id": "7", 
            "name": "qr-3ff411a2-54", 
            "internal" : True, 
            "tag": "5"
        }, 
        "tap31c19fbe-5d" : {
            "id": "19", 
            "name": "tap31c19fbe-5d", 
            "internal" : True, 
            "tag": "117"
        }, 
        "br-int" : {
            "id": "3", 
            "name": "br-int", 
            "internal" : True
        }, 
        "qr-18f029db-77" : {
            "id": "17", 
            "name": "qr-18f029db-77", 
            "internal" : True, 
            "tag": "105"
        }, 
        "br-tun" : {
            "id": "13", 
            "name": "br-tun", 
            "internal" : True
        }, 
        "tap82d4992f-4d" : {
            "id": "9", 
            "name": "tap82d4992f-4d", 
            "internal" : True, 
            "tag": "5"
        }, 
        "tap16620a58-c4" : {
            "id": "16", 
            "name": "tap16620a58-c4", 
            "internal" : True, 
            "tag": "6"
        }, 
        "p_ff798dba-0" : {
            "id": "15", 
            "name": "p_ff798dba-0", 
            "internal" : True
        }, 
        "tapee8e5dbb-03" : {
            "id": "6", 
            "name": "tapee8e5dbb-03", 
            "internal" : True, 
            "tag": "1"
        }, 
        "tap702e9683-0c" : {
            "id": "20", 
            "name": "tap702e9683-0c", 
            "internal" : True, 
            "tag": "118"
        }, 
        "tapaf69959f-ef" : {
            "id": "18", 
            "name": "tapaf69959f-ef", 
            "internal" : True, 
            "tag": "105"
        }, 
        "tap5f22f397-d8" : {
            "id": "11", 
            "name": "tap5f22f397-d8", 
            "internal" : True, 
            "tag": "3"
        }, 
        "qr-bb9b8340-72" : {
            "id": "1", 
            "name": "qr-bb9b8340-72", 
            "internal" : True, 
            "tag": "3"
        }, 
        "qr-8733cc5d-b3" : {
            "id": "2", 
            "name": "qr-8733cc5d-b3", 
            "internal" : True, 
            "tag": "4"
        }, 
        "ovs-system" : {
            "id": "0", 
            "name": "ovs-system", 
            "internal" : True
        }, 
        "br-floating" : {
            "id": "14", 
            "name": "br-floating", 
            "internal" : True
        }, 
        "qg-57e65d34-3d" : {
            "id": "10", 
            "name": "qg-57e65d34-3d", 
            "internal" : True, 
            "tag": "2"
        }, 
        "qr-f7b44150-99" : {
            "id": "4", 
            "name": "qr-f7b44150-99", 
            "internal" : True, 
            "tag": "1"
        }, 
        "tapbf16c3ab-56" : {
            "id": "5", 
            "name": "tapbf16c3ab-56", 
            "internal" : True, 
            "tag": "4"
        }
    }, 
    "show_in_tree" : True, 
    "topic": "N/A", 
    "tunnel_ports" : {
        "br-tun" : {
            "name": "br-tun", 
            "interface": "br-tun", 
            "type": "internal"
        }, 
        "vxlan-c0a80201" : {
            "name": "vxlan-c0a80201", 
            "options" : {
                "local_ip": "192.168.2.3", 
                "out_key": "flow", 
                "in_key": "flow", 
                "df_default": "True", 
                "remote_ip": "192.168.2.1"
            }, 
            "interface": "vxlan-c0a80201", 
            "type": "vxlan"
        }, 
        "vxlan-c0a80202" : {
            "name": "vxlan-c0a80202", 
            "options" : {
                "local_ip": "192.168.2.3", 
                "out_key": "flow", 
                "in_key": "flow", 
                "df_default": "True", 
                "remote_ip": "192.168.2.2"
            }, 
            "interface": "vxlan-c0a80202", 
            "type": "vxlan"
        }, 
        "patch-int" : {
            "name": "patch-int", 
            "options" : {
                "peer": "patch-tun"
            }, 
            "interface": "patch-int", 
            "type": "patch"
        }
    }, 
    "type": "vedge"
}
    ]