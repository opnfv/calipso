///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: GeneralNodeInfoBox 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
        
import './general-node-info-box.html';     
    
/*  
 * Lifecycles
 */   
  
Template.GeneralNodeInfoBox.onCreated(function() {
  let instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
  });

  instance.autorun(function () {
    let data = Template.currentData();
    new SimpleSchema({
      objectName: { type: String },
      type: { type: String },
      lastScanned: { type: Date, optional: true },
      description: { type: String, optional: true },
    }).validate(data);

  });

});  

/*
Template.GeneralNodeInfoBox.rendered = function() {
};  
*/

/*
 * Events
 */

Template.GeneralNodeInfoBox.events({
});
   
/*  
 * Helpers
 */

Template.GeneralNodeInfoBox.helpers({    
});


