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

Template.EnvMonitoringInfo.helpers({    
  createInputArgs: createInputArgs,

  createSelectArgs: createSelectArgs,

  envTypeOptions: function () {
    return Constants.getByName('env_types');
  },

  monitoringTypeOptions: function () {
    return Constants.getByName('environment_monitoring_types');
  },

  provisionOptions: function () {
    return Constants.getByName('environment_provision_types');
  },
});


