/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: alarmIcons
 */

import '/imports/ui/components/breadcrumb/breadcrumb';
import { Messages } from '/imports/api/messages/messages';
import { Roles } from 'meteor/alanning:roles';

import './alarm-icons.html';     

/*
 * Lifecycle
 */
 
Template.alarmIcons.onCreated(function () {
  let instance = this;

  instance.autorun(function () {
    instance.subscribe('messages/count?level', 'info');
    instance.subscribe('messages/count?level', 'warning');
    instance.subscribe('messages/count?level', 'error');
  });
});

/*
 * Helpers
 */  

Template.alarmIcons.helpers({
  isAdmin: function () {
    return Roles.userIsInRole(Meteor.userId(), 'manage-users', Roles.GLOBAL_GROUP); 
  },

  infosCount: function(){
    return Messages.find({level:'info'}).count();
  },

  warningsCount: function(){
    return Messages.find({level:'warning'}).count();
  },

  errorsCount: function(){
    return Messages.find({level:'error'}).count();
  },
});
