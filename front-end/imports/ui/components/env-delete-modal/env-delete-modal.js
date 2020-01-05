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
 * Template Component: EnvDeleteModal 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
//import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
        
import './env-delete-modal.html';     
    
/*  
 * Lifecycles
 */   
  
Template.EnvDeleteModal.onCreated(function() {
  this.autorun(() => {
    new SimpleSchema({
      onDeleteReq: { type: Function },
    }).validate(Template.currentData());
  });
});  

/*
Template.EnvDeleteModal.rendered = function() {
};  
*/

/*
 * Events
 */

Template.EnvDeleteModal.events({
  'click .sm-button-delete': function (_event, _instance) {
    let onDeleteReq = Template.currentData().onDeleteReq;
    onDeleteReq();
  }
});
   
/*  
 * Helpers
 */

Template.EnvDeleteModal.helpers({    
});


