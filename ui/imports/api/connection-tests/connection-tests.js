/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { Mongo } from 'meteor/mongo';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
//import * as R from 'ramda';

export const ConnectionTests = new Mongo.Collection('connection_tests', { idGeneration: 'MONGO' });

let simpleSchema = new SimpleSchema({
  _id: { type: { _str: { type: String, regEx: SimpleSchema.RegEx.Id } } },
  environment: {
    type: String,
  },
  
  test_targets: {
    type: [String],
  },

  test_configurations: {
    type: [Object],
    blackbox: true
  },

  submit_timestamp: {
    type: String,
  },

  status: {
    type: String,
    defaultValue: 'request'
  }
});

ConnectionTests.schema = simpleSchema;
ConnectionTests.attachSchema(ConnectionTests.schema);
