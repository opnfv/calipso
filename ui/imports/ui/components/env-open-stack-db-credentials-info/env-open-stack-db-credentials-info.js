/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: EnvOpenStackDbCredentialsInfo 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
//import { ReactiveDict } from 'meteor/reactive-dict';
        
import { createInputArgs } from '/imports/ui/lib/input-model';

import './env-open-stack-db-credentials-info.html';     
    
/*  
 * Lifecycles
 */   
  
Template.EnvOpenStackDbCredentialsInfo.onCreated(function() {
});  

/*
Template.EnvOpenStackDbCredentialsInfo.rendered = function() {
};  
*/

/*
 * Events
 */

Template.EnvOpenStackDbCredentialsInfo.events({
  'click .sm-next-button': function () {
    let instance = Template.instance();
    instance.data.onNextRequested(); 
  }
});
   
/*  
 * Helpers
 */

Template.EnvOpenStackDbCredentialsInfo.helpers({    
  createInputArgs: createInputArgs
});


