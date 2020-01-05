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
import { ConnectionTests } from '../connection-tests.js';

Meteor.publish('connection_tests?_id', function (_id) {
  console.log('server subscribtion to: connection_tests?_id');
  console.log('-_id: ', R.toString(_id));

  let query = {
    _id: _id,
  };
  return ConnectionTests.find(query);
});
