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
//import * as R from 'ramda';

export let InventoryTreeNodeBehavior = {
  subscribeGetChildrenFn: function (instance, parent) {
    instance.subscribe('inventory.children',
      parent.id, parent.type, parent.name, parent.environment);
  },

  subscribeGetFirstChildFn: function (instance, parent) {
    instance.subscribe('inventory.first-child', 
      parent.id, parent.type, parent.name, parent.environment);
  },

  getChildrenFn: function (parent) {
    let query = {
      $or: [{
        parent_id: parent.id,
        parent_type: parent.type,
        environment: parent.environment,
        show_in_tree: true
      }]
    };

    /*
    if (R.equals('host_ref', parent.type)) {
      let realParent = Inventory.findOne({ 
        name: parent.name,
        environment: parent.environment,
        type: 'host'
      });

      if (! R.isNil(realParent)) {
        query = R.merge(query, {
          $or: R.append({
            environment: parent.environment,
            parent_id: realParent.id
          }, query.$or)
        });
      }
    }
    */

    return Inventory.find(query);
  },

  hasChildrenFn: function (parent) {
    let query = {
      $or: [
        {
          parent_id: parent._id
        }
      ]
    };

    return Inventory.find(query).count() > 0;
  }
};
