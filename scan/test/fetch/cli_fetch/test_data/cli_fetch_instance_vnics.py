###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
VNICS_FOLDER = {
    "create_object": True,
    "environment": "Mirantis-Liberty-Xiaocong",
    "id": "bf0cb914-b316-486c-a4ce-f22deb453c52-vnics",
    "id_path": "/Mirantis-Liberty-Xiaocong/Mirantis-Liberty-Xiaocong-regions/RegionOne/RegionOne-availability_zones/osdna-zone/node-5.cisco.com/node-5.cisco.com-instances/bf0cb914-b316-486c-a4ce-f22deb453c52/bf0cb914-b316-486c-a4ce-f22deb453c52-vnics",
    "name": "vNICs",
    "name_path": "/Mirantis-Liberty-Xiaocong/Regions/RegionOne/Availability Zones/osdna-zone/node-5.cisco.com/Instances/test/vNICs",
    "object_name": "vNICs",
    "parent_id": "bf0cb914-b316-486c-a4ce-f22deb453c52",
    "parent_type": "instance",
    "show_in_tree": True,
    "text": "vNICs",
    "type": "vnics_folder"
}

INSATNCE = {
    "_id": "5806817e4a0a8a3fbe3bee8b",
    "children_url": "/osdna_dev/discover.py?type=tree&id=bf0cb914-b316-486c-a4ce-f22deb453c52", 
    "environment": "Mirantis-Liberty-Xiaocong", 
    "host": "node-5.cisco.com", 
    "id": "bf0cb914-b316-486c-a4ce-f22deb453c52", 
    "id_path": "/Mirantis-Liberty-Xiaocong/Mirantis-Liberty-Xiaocong-regions/RegionOne/RegionOne-availability_zones/osdna-zone/node-5.cisco.com/node-5.cisco.com-instances/bf0cb914-b316-486c-a4ce-f22deb453c52", 
    "ip_address": "192.168.0.4", 
    "local_name": "instance-00000026",
    "mac_address": "fa:16:3e:e8:7f:04", 
    "name": "test", 
    "name_path": "/Mirantis-Liberty-Xiaocong/Regions/RegionOne/Availability Zones/osdna-zone/node-5.cisco.com/Instances/test", 
    "network": [
        "2e3b85f4-756c-49d9-b34c-f3db13212dbc"
    ], 
    "network_info": [
        {
            "devname": "tap1f72bd15-8a", 
            "id": "1f72bd15-8ab2-43cb-94d7-e823dd845255", 
            "profile": {

            }, 
            "vnic_type": "normal", 
            "type": "ovs", 
            "address": "fa:16:3e:e8:7f:04", 
            "qbg_params": None,
            "network": {
                "bridge": "br-int", 
                "label": "123456", 
                "subnets": [
                    {
                        "cidr": "172.16.13.0/24", 
                        "version": 4,
                        "gateway": {
                            "version": 4,
                            "meta": {

                            }, 
                            "address": "172.16.13.1", 
                            "type": "gateway"
                        }, 
                        "routes": [

                        ], 
                        "dns": [

                        ], 
                        "ips": [
                            {
                                "meta": {

                                }, 
                                "version": 4,
                                "type": "fixed", 
                                "address": "172.16.13.4", 
                                "floating_ips": [

                                ]
                            }
                        ], 
                        "meta": {
                            "dhcp_server": "172.16.13.2"
                        }
                    }
                ], 
                "meta": {
                    "tenant_id": "75c0eb79ff4a42b0ae4973c8375ddf40", 
                    "injected": False
                }, 
                "id": "2e3b85f4-756c-49d9-b34c-f3db13212dbc"
            }, 
            "active": True,
            "meta": {

            }, 
            "details": {
                "port_filter": True,
                "ovs_hybrid_plug": True
            }, 
            "preserve_on_delete": False,
            "qbh_params": None,
            "ovs_interfaceid": "1f72bd15-8ab2-43cb-94d7-e823dd845255"
        }
    ], 
    "object_name": "test", 
    "parent_id": "node-5.cisco.com-instances", 
    "parent_type": "instances_folder", 
    "project_id": "75c0eb79ff4a42b0ae4973c8375ddf40", 
    "projects": [
        "OSDNA-project"
    ], 
    "show_in_tree": True,
    "type": "instance", 
    "uuid": "bf0cb914-b316-486c-a4ce-f22deb453c52"
}


COMPUTE_HOST = {
    "environment": "Mirantis-Liberty-Xiaocong",
    "host": "node-5.cisco.com",
    "host_type": [
        "Compute"
    ],
    "id": "node-5.cisco.com",
    "id_path": "/Mirantis-Liberty-Xiaocong/Mirantis-Liberty-Xiaocong-regions/RegionOne/RegionOne-availability_zones/osdna-zone/node-5.cisco.com",
    "ip_address": "192.168.0.4",
    "name": "node-5.cisco.com",
    "name_path": "/Mirantis-Liberty-Xiaocong/Regions/RegionOne/Availability Zones/osdna-zone/node-5.cisco.com",
    "object_name": "node-5.cisco.com",
    "os_id": "1",
    "parent_id": "osdna-zone",
    "parent_type": "availability_zone",
    "services": {
        "nova-compute": {
            "active": True,
            "available": True,
            "updated_at": "2016-10-21T18:01:42.000000"
        }
    },
    "show_in_tree": True,
    "type": "host",
    "zone": "osdna-zone"
}

NETWORK_HOST = {
    "config": {
        "interfaces": 4,
        "log_agent_heartbeats": False,
        "gateway_external_network_id": "",
        "router_id": "",
        "interface_driver": "neutron.agent.linux.interface.OVSInterfaceDriver",
        "ex_gw_ports": 2,
        "routers": 2,
        "handle_internal_only_routers": True,
        "floating_ips": 1,
        "external_network_bridge": "",
        "use_namespaces": True,
        "agent_mode": "legacy"
    },
    "environment": "Mirantis-Liberty-Xiaocong",
    "host": "node-6.cisco.com",
    "host_type": [
        "Controller",
        "Network"
    ],
    "id": "node-6.cisco.com",
    "id_path": "/Mirantis-Liberty-Xiaocong/Mirantis-Liberty-Xiaocong-regions/RegionOne/RegionOne-availability_zones/internal/node-6.cisco.com",
    "name": "node-6.cisco.com",
    "name_path": "/Mirantis-Liberty-Xiaocong/Regions/RegionOne/Availability Zones/internal/node-6.cisco.com",
    "object_name": "node-6.cisco.com",
    "parent_id": "internal",
    "parent_type": "availability_zone",
    "services": {
        "nova-scheduler": {
            "active": True,
            "available": True,
            "updated_at": "2016-10-21T18:01:10.000000"
        },
        "nova-consoleauth": {
            "active": True,
            "available": True,
            "updated_at": "2016-10-21T18:01:54.000000"
        },
        "nova-conductor": {
            "active": True,
            "available": True,
            "updated_at": "2016-10-21T18:01:45.000000"
        },
        "nova-cert": {
            "active": True,
            "available": True,
            "updated_at": "2016-10-21T18:01:56.000000"
        }
    },
    "show_in_tree": True,
    "type": "host",
    "zone": "internal"
}

DUMPXML = "<domain type='qemu' id='38'>\n  <name>instance-00000026</name>\n  <uuid>bf0cb914-b316-486c-a4ce-f22deb453c52</uuid>\n  <metadata>\n    <nova:instance xmlns:nova=\"http://openstack.org/xmlns/libvirt/nova/1.0\">\n      <nova:package version=\"12.0.0\"/>\n      <nova:name>test</nova:name>\n      <nova:creationTime>2016-10-17 22:37:43</nova:creationTime>\n      <nova:flavor name=\"m1.micro\">\n        <nova:memory>64</nova:memory>\n        <nova:disk>0</nova:disk>\n        <nova:swap>0</nova:swap>\n        <nova:ephemeral>0</nova:ephemeral>\n        <nova:vcpus>1</nova:vcpus>\n      </nova:flavor>\n      <nova:owner>\n        <nova:user uuid=\"13baa553aae44adca6615e711fd2f6d9\">admin</nova:user>\n        <nova:project uuid=\"75c0eb79ff4a42b0ae4973c8375ddf40\">OSDNA-project</nova:project>\n      </nova:owner>\n      <nova:root type=\"image\" uuid=\"c6f490c4-3656-43c6-8d03-b4e66bd249f9\"/>\n    </nova:instance>\n  </metadata>\n  <memory unit='KiB'>65536</memory>\n  <currentMemory unit='KiB'>65536</currentMemory>\n  <vcpu placement='static'>1</vcpu>\n  <cputune>\n    <shares>1024</shares>\n  </cputune>\n    <sysinfo type='smbios'>\n      <system>\n        <entry name='manufacturer'>OpenStack Foundation</entry>\n        <entry name='product'>OpenStack Nova</entry>\n        <entry name='version'>12.0.0</entry>\n        <entry name='serial'>9cf57bfd-7477-4671-b2d3-3dfeebfefb1d</entry>\n        <entry name='uuid'>bf0cb914-b316-486c-a4ce-f22deb453c52</entry>\n        <entry name='family'>Virtual Machine</entry>\n      </system>\n    </sysinfo>\n  <os>\n    <type arch='x86_64' machine='pc-i440fx-trusty'>hvm</type>\n    <boot dev='hd'/>\n    <smbios mode='sysinfo'/>\n  </os>\n  <features>\n    <acpi/>\n    <apic/>\n  </features>\n  <cpu>\n    <topology sockets='1' cores='1' threads='1'/>\n  </cpu>\n  <clock offset='utc'/>\n  <on_poweroff>destroy</on_poweroff>\n  <on_reboot>restart</on_reboot>\n  <on_crash>destroy</on_crash>\n  <devices>\n    <emulator>/usr/bin/qemu-system-x86_64</emulator>\n    <disk type='file' device='disk'>\n      <driver name='qemu' type='qcow2' cache='directsync'/>\n      <source file='/var/lib/nova/instances/bf0cb914-b316-486c-a4ce-f22deb453c52/disk'/>\n      <backingStore type='file' index='1'>\n        <format type='raw'/>\n        <source file='/var/lib/nova/instances/_base/44881e4441fbd821d0d6240f90742fc97e52f83e'/>\n        <backingStore/>\n      </backingStore>\n      <target dev='vda' bus='virtio'/>\n      <alias name='virtio-disk0'/>\n      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>\n    </disk>\n    <controller type='usb' index='0'>\n      <alias name='usb0'/>\n      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x2'/>\n    </controller>\n    <controller type='pci' index='0' model='pci-root'>\n      <alias name='pci.0'/>\n    </controller>\n    <interface type='bridge'>\n      <mac address='fa:16:3e:e8:7f:04'/>\n      <source bridge='qbr1f72bd15-8a'/>\n      <target dev='tap1f72bd15-8a'/>\n      <model type='virtio'/>\n      <driver name='qemu'/>\n      <alias name='net0'/>\n      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>\n    </interface>\n    <serial type='file'>\n      <source path='/var/lib/nova/instances/bf0cb914-b316-486c-a4ce-f22deb453c52/console.log'/>\n      <target port='0'/>\n      <alias name='serial0'/>\n    </serial>\n    <serial type='pty'>\n      <source path='/dev/pts/8'/>\n      <target port='1'/>\n      <alias name='serial1'/>\n    </serial>\n    <console type='file'>\n      <source path='/var/lib/nova/instances/bf0cb914-b316-486c-a4ce-f22deb453c52/console.log'/>\n      <target type='serial' port='0'/>\n      <alias name='serial0'/>\n    </console>\n    <input type='tablet' bus='usb'>\n      <alias name='input0'/>\n    </input>\n    <input type='mouse' bus='ps2'/>\n    <input type='keyboard' bus='ps2'/>\n    <graphics type='vnc' port='5902' autoport='yes' listen='0.0.0.0' keymap='en-us'>\n      <listen type='address' address='0.0.0.0'/>\n    </graphics>\n    <video>\n      <model type='cirrus' vram='9216' heads='1'/>\n      <alias name='video0'/>\n      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>\n    </video>\n    <memballoon model='virtio'>\n      <alias name='balloon0'/>\n      <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>\n      <stats period='10'/>\n    </memballoon>\n  </devices>\n  <seclabel type='dynamic' model='apparmor' relabel='yes'>\n    <label>libvirt-bf0cb914-b316-486c-a4ce-f22deb453c52</label>\n    <imagelabel>libvirt-bf0cb914-b316-486c-a4ce-f22deb453c52</imagelabel>\n  </seclabel>\n</domain>\n\n"
WRONG_DUMPXML = "<domain type='qemu' id='38'><uuid>wrong_instance</uuid></domain>"
INSTANCES_LIST = [
    ' Id    Name                           State',
    '----------------------------------------------------',
    ' 2     instance-00000002              running',
    ' 27    instance-0000001c              running',
    ' 38    instance-00000026              running',
    ' 39    instance-00000028              running',
    ''
]

VNIC = {
    "@type": "bridge",
    "address": {
        "@bus": "0x00",
        "@domain": "0x0000",
        "@function": "0x0",
        "@slot": "0x03",
        "@type": "pci"
    },
    "alias": {
        "@name": "net0"
    },
    "driver": {
        "@name": "qemu"
    },
    "mac": {
        "@address": "fa:16:3e:e8:7f:04"
    },
    "model": {
        "@type": "virtio"
    },
    "source": {
        "@bridge": "qbr1f72bd15-8a"
    },
    "target": {
        "@dev": "tap1f72bd15-8a"
    }
}

ID = "38"

VNICS_FROM_DUMP_XML = [
    {
        "@type": "bridge",
        "address": {
            "@bus": "0x00",
            "@domain": "0x0000",
            "@function": "0x0",
            "@slot": "0x03",
            "@type": "pci"
        },
        "alias": {
            "@name": "net0"
        },
        "driver": {
            "@name": "qemu"
        },
        "host": "node-5.cisco.com",
        "id": "tap1f72bd15-8a",
        "instance_db_id": "5806817e4a0a8a3fbe3bee8b",
        "instance_id": "bf0cb914-b316-486c-a4ce-f22deb453c52",
        "mac": {
            "@address": "fa:16:3e:e8:7f:04"
        },
        "mac_address": "fa:16:3e:e8:7f:04",
        "model": {
            "@type": "virtio"
        },
        "name": "tap1f72bd15-8a",
        "source": {
            "@bridge": "qbr1f72bd15-8a"
        },
        "source_bridge": "qbr1f72bd15-8a",
        "target": {
            "@dev": "tap1f72bd15-8a"
        },
        "vnic_type": "instance_vnic"
    }
]


# functional test
INPUT = "bf0cb914-b316-486c-a4ce-f22deb453c52-vnics"