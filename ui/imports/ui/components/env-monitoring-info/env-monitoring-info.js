/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: EnvMonitoringInfo 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
//import { ReactiveDict } from 'meteor/reactive-dict';
import * as R from 'ramda';
        
import { createInputArgs } from '/imports/ui/lib/input-model';
import { createSelectArgs } from '/imports/ui/lib/select-model';
import { Constants } from '/imports/api/constants/constants';

import './env-monitoring-info.html';     
    
/*  
 * Lifecycles
 */   
  
Template.EnvMonitoringInfo.onCreated(function() {
  let instance = this;

  instance.autorun(function () {
    instance.subscribe('constants');
  });
});  

/*
Template.EnvMonitoringInfo.rendered = function() {
};  
*/

/*
 * Events
 */

Template.EnvMonitoringInfo.events({
});
   
/*  
 * Helpers
 */

Template.EnvMonitoringInfo.helpers({    
  createInputArgs: createInputArgs,

  createSelectArgs: createSelectArgs,

  envTypeOptions: function () {
    let item = Constants.findOne({ name: 'env_types' });
    if (R.isNil(item)) { return []; }
    return item.data;
  },

  monitoringTypeOptions: function () {
    let item = Constants.findOne({ name: 'environment_monitoring_types' });
    if (R.isNil(item)) { return []; }
    return item.data;
  },

  provisionOptions: function () {
    let item = Constants.findOne({ name: 'environment_provision_types' });
    if (R.isNil(item)) { return []; }
    return item.data;
  },
});


