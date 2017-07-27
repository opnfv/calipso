/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: GeneralFolderNodeDashboard 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { ReactiveDict } from 'meteor/reactive-dict';
import * as R from 'ramda';
import { store } from '/imports/ui/store/store';
import { InventoryTreeNodeBehavior } from '/imports/ui/lib/inventory-tree-node-behavior';
import { Inventory } from '/imports/api/inventories/inventories';
import { Icon } from '/imports/lib/icon';
        
import '/imports/ui/components/data-cubic/data-cubic';
import '/imports/ui/components/general-node-info-box/general-node-info-box';

import './general-folder-node-dashboard.html';     
    
/*  
 * Lifecycles
 */   
  
Template.GeneralFolderNodeDashboard.onCreated(function() {
  let instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    _id: null,
    node: null,
    childrenCount: 0,
  });

  instance.autorun(function () {
    let data = Template.currentData();
    new SimpleSchema({
      _id: { type: { _str: { type: String, regEx: SimpleSchema.RegEx.Id } } },
      onNodeSelected: { type: Function },
    }).validate(data);

    instance.state.set('_id', data._id);
  });

  instance.autorun(function () {
    let _id = instance.state.get('_id');
    if (R.isNil(_id)) { return; }

    Inventory.find({ _id: _id}).forEach((node) => {
      InventoryTreeNodeBehavior.subscribeGetChildrenFn(instance, node);
      let childrenCount = InventoryTreeNodeBehavior.getChildrenFn(node).count();
      instance.state.set('childrenCount', childrenCount);
      instance.state.set('node', node);
    });
  });
});  

/*
Template.GeneralFolderNodeDashboard.rendered = function() {
};  
*/

/*
 * Events
 */

Template.GeneralFolderNodeDashboard.events({
});
   
/*  
 * Helpers
 */

Template.GeneralFolderNodeDashboard.helpers({    
  argsMainCubic: function (childrenCount) {
    return {
      header: R.path(['components', 'generalFolderNodeDashboard', 'mainCubic', 'header']
        )(store.getState().api.i18n),
      dataInfo: R.toString(childrenCount), 
      icon: new Icon({ type: 'fa', name: 'desktop' }),
    };
  },

  argsGeneralNodeInfoBox: function (node) {
    return {
      objectName: node.object_name,
      type: node.type,
      lastScanned: node.last_scanned,
      description: node.description,
    };
  },

  childrenCount: function () {
    let instance = Template.instance();
    return instance.state.get('childrenCount');
  },

  children: function () {
    let instance = Template.instance();
    let node = instance.state.get('node');
    return InventoryTreeNodeBehavior.getChildrenFn(node);
  }
}); // end: helpers


