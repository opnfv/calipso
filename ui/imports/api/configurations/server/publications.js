/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { Meteor } from 'meteor/meteor';

import { Configurations } from '../configurations.js';

Meteor.publish('configurations?user', function () {
  console.log('server subscribtion: configurations?user');

  let userId = this.userId;

  let query = { user_id: userId };
  console.log('-query: ', query);
  return Configurations.find(query); 
});
