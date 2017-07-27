/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: EnvNfvInfo 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
//import { ReactiveDict } from 'meteor/reactive-dict';
import * as R from 'ramda';
        
import { createInputArgs } from '/imports/ui/lib/input-model';

import './env-nfv-info.html';     
    
/*  
 * Lifecycles
 */   
  
Template.EnvNfvInfo.onCreated(function() {
});  

/*
Template.EnvNfvInfo.rendered = function() {
};  
*/

/*
 * Events
 */

Template.EnvNfvInfo.events({
  'click .sm-next-button': function () {
    let instance = Template.instance();
    instance.data.onNextRequested(); 
  }
});
   
/*  
 * Helpers
 */

Template.EnvNfvInfo.helpers({    
  createInputArgs: createInputArgs,

  markIfDisabled: function () {
    let instance = Template.instance();
    let attrs = {};
    if (instance.data.disabled) {
      attrs = R.assoc('disabled', true, attrs);
    }

    return attrs;
  }
});


