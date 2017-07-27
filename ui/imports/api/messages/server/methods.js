/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import * as R from 'ramda';
import { Messages } from '/imports/api/messages/messages';

Meteor.methods({
  'messages/get?level&env&page&amountPerPage&sortField&sortDirection': function (
      level, env, page, amountPerPage, sortField, sortDirection) {

    logMethodCall('messages/get?level&env&page&amountPerPage&sortField&sortDirection', 
      {level, env, page, amountPerPage});

    this.unblock();

    let skip = (page - 1) * amountPerPage;

    let query = {};
    let sortParams = {};

    query = R.ifElse(R.isNil, R.always(query),R.assoc('environment', R.__, query))(env);
    query = R.ifElse(R.isNil, R.always(query),R.assoc('level', R.__, query))(level);

    sortParams = R.ifElse(R.isNil, R.always(sortParams), 
        R.assoc(R.__, sortDirection, sortParams))(sortField);

    console.log('sort params:', sortParams);

    let qParams = {
      limit: amountPerPage,
      skip: skip,
      sort: sortParams,
    };

    return Messages.find(query, qParams).fetch();
  }
});

function logMethodCall(name, args) {
  console.log(`method call: ${name}`);
  R.forEachObjIndexed((value, key) => {
    console.log(`${key}: ${R.toString(value)}`);
  }, args);
}
