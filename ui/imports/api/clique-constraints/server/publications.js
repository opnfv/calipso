/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { Meteor } from 'meteor/meteor';

import { CliqueConstraints } from '../clique-constraints.js';

Meteor.publish('clique_constraints', function () {
  console.log('server subscribtion: clique_constraints');

  //let that = this;

  let query = {};
  return CliqueConstraints.find(query); 
});

Meteor.publish('clique_constraints?_id', function (_id) {
  console.log('server subscribtion: clique_constraints?_id');
  console.log(_id);

  //let that = this;

  let query = { _id: _id };
  return CliqueConstraints.find(query); 
});
