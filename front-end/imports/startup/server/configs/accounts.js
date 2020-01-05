///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
Accounts.validateNewUser((_user) => {
  let loggedInUser = Meteor.user();
  if (Roles.userIsInRole(loggedInUser, 'manage-users', Roles.GLOBAL_GROUP)) {
    return true;
  }

  throw new Meteor.Error(403, 'NotAuthorized to create new users');
});
