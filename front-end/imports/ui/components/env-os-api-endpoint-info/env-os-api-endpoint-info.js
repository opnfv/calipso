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
 * Template Component: EnvOsApiEndpointInfo 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
//import { ReactiveDict } from 'meteor/reactive-dict';
        
import { createInputArgs } from '/imports/ui/lib/input-model';

import './env-os-api-endpoint-info.html';     
    
/*  
 * Lifecycles
 */   
  
Template.EnvOsApiEndpointInfo.onCreated(function() {
});  

/*
Template.EnvOsApiEndpointInfo.rendered = function() {
};  
*/

/*
 * Events
 */

Template.EnvOsApiEndpointInfo.events({
  'click .sm-next-button': function () {
    let instance = Template.instance();
    instance.data.onNextRequested(); 
  },

  'click .js-test-connection' : function (e, instance) {
    instance.data.onTestConnection();
  },
});
   
/*  
 * Helpers
 */

Template.EnvOsApiEndpointInfo.helpers({    
  createInputArgs: createInputArgs
});


