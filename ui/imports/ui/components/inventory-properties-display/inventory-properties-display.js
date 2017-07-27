/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: InventoryPropertiesDisplay 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { ReactiveDict } from 'meteor/reactive-dict';
import * as R from 'ramda';
import { Inventory } from '/imports/api/inventories/inventories';
        
import './inventory-properties-display.html';     
    
/*  
 * Lifecycles
 */   
  
Template.InventoryPropertiesDisplay.onCreated(function() {
  let instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    data: null,
    env: null,
    nodeId: null,
  });

  instance.autorun(function () {
    let data = Template.currentData();

    try {
      new SimpleSchema({
        env: { type: String },
        nodeId: { type: String },
        displayFn: { type: Function },
      }).validate(data);
    } catch (e) { 
      // meteor sometimes does not show the validation error and throws unclear view error. 
      console.error(`error in validate ${e}`); 
      throw e;
    }

    instance.state.set('env', data.env);
    instance.state.set('nodeId', data.nodeId);
  });

  instance.autorun(function () {
    let env = instance.state.get('env'); 
    let nodeId = instance.state.get('nodeId'); 
    if (R.any(R.isNil)([env, nodeId])) { return; }

    instance.subscribe('inventory?env&id', env, nodeId);

    Inventory.find({ environment: env, id: nodeId }).forEach((node) => {
      instance.state.set('node', node);
    });
  });
});  

/*
Template.InventoryPropertiesDisplay.rendered = function() {
};  
*/

/*
 * Events
 */

Template.InventoryPropertiesDisplay.events({
});
   
/*  
 * Helpers
 */

Template.InventoryPropertiesDisplay.helpers({    
  getNode: function () {
    let instance = Template.instance();
    return instance.state.get('node');
  }
});


