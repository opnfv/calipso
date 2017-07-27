/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { Meteor } from 'meteor/meteor';
//import * as R from 'ramda';
//import { Environments } from '/imports/api/environments/environments';
//import { Roles } from 'meteor/alanning:roles';

Meteor.publish('users', function () {
  console.log('server subscribtion to: users');
  /*
  let that = this;

  let query = {};

  if (! Roles.userIsInRole(that.userId, 'manage-users', 'default-group')) {
    query = {
      _id: that.userId
    };
  }
  */

  return Meteor.users.find({});
});
