/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import * as R from 'ramda';
import { Roles } from 'meteor/alanning:roles';

let users = [
  {
    username: 'admin',
    name: 'admin',
    email: 'admin@example.com',
    password: '123456',
    roles: [
      { role: 'manage-users', group: Roles.GLOBAL_GROUP },
      { role: 'manage-link-types', group: Roles.GLOBAL_GROUP },
      { role: 'manage-clique-types', group: Roles.GLOBAL_GROUP },
      { role: 'manage-clique-constraints', group: Roles.GLOBAL_GROUP },
      { role: 'view-env', group: Roles.GLOBAL_GROUP },
      { role: 'edit-env', group: Roles.GLOBAL_GROUP },
    ]
  }
];

R.forEach((user) => {
  let id;
  let userDb = Meteor.users.findOne({ username: user.username });
  if (R.isNil(userDb)) {
    console.log('creating user', user);
    id = Accounts.createUser({
      username: user.username,
      email: user.email,
      password: user.password,
      profile: { name: user.name }
    });
  } else {
    id = userDb._id;
  }

  if (user.roles.length > 0) {
    console.log('adding roles to user', user, user.roles);

    R.forEach((roleItem) => {
      Roles.addUsersToRoles(id, roleItem.role, roleItem.group);
    }, user.roles);
  }
}, users);
