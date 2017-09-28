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
import { ReactiveDict } from 'meteor/reactive-dict';

import { UserSettings } from '/imports/api/user-settings/user-settings';

import './alarm-icons.html';     

/*
 * Lifecycle
 */
 
Template.alarmIcons.onCreated(function () {
  let instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    msgsViewBackDelta: 1
  });

  instance.autorun(function () {
    instance.subscribe('user_settings?user');
    UserSettings.find({user_id: Meteor.userId()}).forEach((userSettings) => {
      instance.state.set('msgsViewBackDelta', userSettings.messages_view_backward_delta); 
    });
  });

  instance.autorun(function () {
    let msgsViewBackDelta = instance.state.get('msgsViewBackDelta');

    instance.subscribe('messages/count?backDelta&level', msgsViewBackDelta, 'info');
    instance.subscribe('messages/count?backDelta&level', msgsViewBackDelta, 'warning');
    instance.subscribe('messages/count?backDelta&level', msgsViewBackDelta, 'error');
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

  msgCounterName: function (level) {
    let instance = Template.instance();
    let msgsViewBackDelta = instance.state.get('msgsViewBackDelta');
    let counterName = `messages/count?backDelta=${msgsViewBackDelta}&level=${level}`;

    return counterName;
  }
});
