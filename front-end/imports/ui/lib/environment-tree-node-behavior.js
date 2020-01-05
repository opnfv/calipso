///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import { Inventory } from '/imports/api/inventories/inventories';

export let EnvironmentTreeNodeBehavior = {
  subscribeGetChildrenFn: function (instance, env) {
    instance.subscribe('inventory.children',
      env.name, env.type, null, env.name);
  },

  subscribeGetFirstChildFn: function (instance, env) {
    instance.subscribe('inventory.first-child', 
      env.name, env.type, null, env.name);
  },

  getChildrenFn: function (env) {
    let query = {
      $or: [{
        parent_id: env.name,
        parent_type: env.type,
        environment: env.name,
        show_in_tree: true
      }]
    };

    return Inventory.find(query);
  },

  hasChildrenFn: function (env) {
    let query = {
      $or: [
        {
          parent_id: env.name
        }
      ]
    };

    return Inventory.find(query).count() > 0;
  }
};
