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

export const Configurations = new Mongo.Collection('configurations', { idGeneration: 'MONGO' });

let schema = {
  _id: { type: { _str: { type: String, regEx: SimpleSchema.RegEx.Id } } },
  user_id: {
    type: String,
  },
  messages_view_backward_delta: {
    type: Number,
    minCount: 1,
    defaultValue: '1209600000', // 14 days
  }
};

let simpleSchema = new SimpleSchema(schema);
Configurations.schema = simpleSchema;
Configurations.attachSchema(Configurations.schema);
