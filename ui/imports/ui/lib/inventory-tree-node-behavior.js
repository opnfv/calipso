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
