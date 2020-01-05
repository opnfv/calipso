###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.utils.inventory_mgr import InventoryMgr


def update_resource_version(inv: InventoryMgr,
                            env: str,
                            method: str,
                            resource_version):
    env_config = inv.get_env_config(env)

    listener_kwargs = env_config.get('listener_kwargs', {})
    resource_versions = listener_kwargs.get('resource_versions', {})
    resource_versions[method] = int(resource_version)
    listener_kwargs['resource_versions'] = resource_versions
    env_config['listener_kwargs'] = listener_kwargs

    inv.set(item=env_config,
            collection='environments_config')