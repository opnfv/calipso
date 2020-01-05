///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import { Roles } from 'meteor/alanning:roles';

import { ReactiveDict } from 'meteor/reactive-dict';

import { UserSettings } from '/imports/api/user-settings/user-settings';

import './settings-list.html';
import {handleLoginMenu} from "../top-navbar-menu/top-navbar-menu";


Template.settingsList.onCreated(function () {
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

Template.settingsList.events({
    'click': function (e) {
      handleLoginMenu(e);
    }
});

Template.settingsList.helpers({
  isAdmin: function () {
    return Roles.userIsInRole(Meteor.userId(), 'manage-users', Roles.GLOBAL_GROUP); 
  },
});