/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: GeneralNodeDashboard 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { ReactiveDict } from 'meteor/reactive-dict';
import { Inventory } from '/imports/api/inventories/inventories';

import '/imports/ui/components/detailed-node-info-box/detailed-node-info-box';
        
import './general-node-dashboard.html';     
    
/*  
 * Lifecycles
 */   
  
Template.GeneralNodeDashboard.onCreated(function() {
  var instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    id: null,
    node: null,
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

    instance.subscribe('inventory?_id', _id);
    Inventory.find({ _id: _id }).forEach((node) => {
      instance.state.set('node', node);
    });
  });
});  

/*
Template.GeneralNodeDashboard.rendered = function() {
};  
*/

/*
 * Events
 */

Template.GeneralNodeDashboard.events({
});
   
/*  
 * Helpers
 */

Template.GeneralNodeDashboard.helpers({    
  getNode: function () {
    let instance = Template.instance();
    return instance.state.get('node');
  },

  argsGenNodeInfoBox: function (node) {
    return {
      node: node,
    };
  }
});


