///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import { Mongo } from 'meteor/mongo';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';

export const Constants = new Mongo.Collection('constants', { idGeneration: 'MONGO' });

let schema = {
  _id: { type: { _str: { type: String, regEx: SimpleSchema.RegEx.Id } } },
  name: { type: String },
  data: { type: [Object], blackbox: true },
};

Constants.schema = schema;
Constants.attachSchema(schema);

Constants.getByName = function(name) {
    return R.ifElse(R.isNil, R.always([]), R.prop('data'))(
        Constants.findOne({ name: name })
    );
};

Constants.validateValue = function(name, context) {
    let values = Constants.findOne({ name: name }).data;

    if (context.value !== context.definition.defaultValue
        && R.isNil(R.find(R.propEq('value', context.value), values))) {
        return 'notAllowed';
    }
};
