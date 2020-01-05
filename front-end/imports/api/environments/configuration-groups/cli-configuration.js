///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import * as R from 'ramda';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { pathRegEx, getEmptyRegEx } from '/imports/lib/general-regex';

export const CLISchema = new SimpleSchema({
  name: { type: String, autoValue: function () { return 'CLI'; } },
  host: { 
    type: String,
    defaultValue: '10.0.0.1'
  },
  key: { 
    type: String,
    regEx: getEmptyRegEx(pathRegEx),
    optional: true
  },
  user: { 
    type: String,
    defaultValue: 'sshuser'
  },
  pwd: { 
    type: String,
    optional: true
  },
});

CLISchema.addValidator(function () {
  let that = this;

  let conf = {};
  if (isConfEmpty(conf)) {
    return;
  }

  let validationResult = R.find((validationFn) => {
    return validationFn(that).isError;
  }, [ keyPasswordValidation ]);

  if (R.isNil(validationResult)) { return; }

  throw validationResult(that);
});

function keyPasswordValidation(schemaItem) {
  let password = schemaItem.field('pwd');
  let key = schemaItem.field('key');

  if (key.value || password.value) { return { isError: false }; }

  return {
    isError: true,
    type: 'subGroupError',
    data: [],
    message: 'Master Host Group: At least one required: key or password'
  }; 
}

function isConfEmpty(conf) {
  return R.find((key) => {
    return !(R.isNil(conf[key]));
  }, R.keys(conf));
}
