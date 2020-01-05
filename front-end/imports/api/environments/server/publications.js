///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import { Meteor } from 'meteor/meteor';
import * as R from 'ramda';
import { Roles } from 'meteor/alanning:roles';

import { Environments } from '../environments.js';

Meteor.publish('environments_config', function () {
  console.log('server subscribtion to: environments_config');
  let userId = this.userId;

  let query = {
    type: 'environment',
  };

  if (! Roles.userIsInRole(userId, 'view-env', null)) {
    query = R.merge(query, {
      'auth.view-env': {
        $in: [ userId ]
      }
    });
  }

  console.log('-query: ', R.toString(query));
  return Environments.find(query);
});

const subsEnvViewEnvUserId = 'environments.view-env&userId';
Meteor.publish(subsEnvViewEnvUserId, function (userId) {
  console.log(`subscription - ${subsEnvViewEnvUserId} `);
  console.log(`-userId: ${R.toString(userId)}`);

  let query = {};

  let currentUser = this.userId;
  if (! Roles.userIsInRole(currentUser, 'manage-users', Roles.GLOBAL_GROUP)) {
    console.log(`* error: unauth`);
    console.log(`- currentUser: ${R.toString(currentUser)}`);
    this.error('unauthorized for this subscription');
    return;
  }

  query = R.merge(query, {
    'auth.view-env': {
      $in: [ userId ]
    }
  });

  console.log(`* query: ${R.toString(query)}`);
  return Environments.find(query);
});

const subsEnvEditEnvUserId = 'environments.edit-env&userId';
Meteor.publish(subsEnvEditEnvUserId, function (userId) {
  console.log(`subscription - ${subsEnvEditEnvUserId} `);
  console.log(`-userId: ${R.toString(userId)}`);
  let query = {};

  let currentUser = this.userId;
  if (! Roles.userIsInRole(currentUser, 'manage-users', Roles.GLOBAL_GROUP)) {
    console.log(`* error: unauth`);
    console.log(`- currentUser: ${R.toString(currentUser)}`);
    this.error('unauthorized for this subscription');
    return;
  }

  query = R.merge(query, {
    'auth.edit-env': {
      $in: [ userId ]
    }
  });

  console.log(`* query: ${R.toString(query)}`);
  return Environments.find(query);
});

Meteor.publish('environments?name', function (name) {
  console.log('server subscribtion to: environments?name=' + name.toString());
  let query = {
    name: name,
    user: this.userId
  };
  return Environments.find(query);
});

Meteor.publish('environments?_id', function (_id) {
  console.log('server subscribtion to: environments?_id');
  console.log('-_id: ', R.toString(_id));

  let query = {
    _id: _id,
    user: this.userId
  };
  return Environments.find(query);
});
