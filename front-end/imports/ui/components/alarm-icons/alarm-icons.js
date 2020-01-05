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
 * Template Component: alarmIcons
 */

import * as R from 'ramda';
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
    msgsViewBackDelta: 1,
    envName: null,
  });

  instance.autorun(function () {
    instance.subscribe('user_settings?user');
    UserSettings.find({ user_id: Meteor.userId() }).forEach((userSettings) => {
      instance.state.set('msgsViewBackDelta', userSettings.messages_view_backward_delta);
    });

    let envObj = Template.currentData();

    if (!R.isNil(envObj)) {
      if (!R.isNil(R.prop('envName', envObj))) {
        let envName = R.prop('envName', envObj);
        instance.state.set('envName', envName);
      }
    }
  });

  instance.autorun(function () {
    let msgsViewBackDelta = instance.state.get('msgsViewBackDelta');
    let envName = instance.state.get('envName');

    if (!R.isNil(envName)) {
      console.log("CURRENT ENV:");
      console.log(envName);
      instance.subscribe('messages/count?level&env', 'info', envName);
      instance.subscribe('messages/count?level&env', 'warning', envName);
      instance.subscribe('messages/count?level&env', 'error', envName);
    }
    else {
      
      instance.subscribe('messages/count?level', 'info');
      instance.subscribe('messages/count?level', 'warning');
      instance.subscribe('messages/count?level', 'error');
    }
  });
});

/*
 * Helpers
 */
Template.alarmIcons.helpers({
  isAdmin: function () {
    return Roles.userIsInRole(Meteor.userId(), 'manage-users', Roles.GLOBAL_GROUP);
  },

  infosCount: function () {
    return Messages.find({ level: 'info' }).count();
  },

  warningsCount: function () {
    return Messages.find({ level: 'warning' }).count();
  },

  errorsCount: function () {
    return Messages.find({ level: 'error' }).count();
  },

  msgCounterName: function (level) {
    let instance = Template.instance();
    let msgsViewBackDelta = instance.state.get('msgsViewBackDelta');
    let envName = instance.state.get('envName');
    let counterName = `messages/count?level=${level}`;
    // let counterName = `messages/count?backDelta=${msgsViewBackDelta}&level=${level}`;

    if (!R.isNil(envName)) {
      counterName = R.concat(counterName, `&env=${envName}`);
    }

    return counterName;
  }
});