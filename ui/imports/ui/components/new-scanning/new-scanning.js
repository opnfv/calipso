/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: NewScanning 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { ReactiveDict } from 'meteor/reactive-dict';
        
import './new-scanning.html';     
    
/*  
 * Lifecycles
 */   
  
Template.NewScanning.onCreated(function() {
  let instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    env: null,
  });

  instance.autorun(function (env) {
    let data = Template.currentData();
    new SimpleSchema({
      env: { type: String, optional: true },
    }).validate(data);

    instance.state.set('env', env);
  });
});  

/*
Template.NewScanning.rendered = function() {
};  
*/

/*
 * Events
 */

Template.NewScanning.events({
});
   
/*  
 * Helpers
 */

Template.NewScanning.helpers({    
  argsScanningRequest: function (env) {
    return {
      action: 'insert',
      env: env,
    };
  },

  argsScheduledScan: function (env) {
    return {
      action: 'insert',
      env: env,
    };
  },
}); // end: helpers


