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
import { Messages } from '/imports/api/messages/messages';
import { isNullOrEmpty } from "../../../lib/utilities";

Meteor.methods({
  'messages/get?level&env&page&amountPerPage&sortField&sortDirection': function (
    level, env, page, amountPerPage, sortField, sortDirection) {

    logMethodCall('messages/get?level&env&page&amountPerPage&sortField&sortDirection',
      { level, env, page, amountPerPage });

    this.unblock();

    let skip = (page - 1) * amountPerPage;

    let query = {};
    let sortParams = {};

    query = R.ifElse(R.isNil, R.always(query), R.assoc('environment', R.__, query))(env);
    query = R.ifElse(R.isNil, R.always(query), R.assoc('level', R.__, query))(level);

    sortParams = R.ifElse(R.isNil, R.always(sortParams),
      R.assoc(R.__, sortDirection, sortParams))(sortField);

    console.log('sort params:', sortParams);

    let qParams = {
      limit: amountPerPage,
      skip: skip,
      sort: sortParams,
    };

    return Messages.find(query, qParams).fetch();
  },
  'messages/get?backDelta&level&env&page&amountPerPage&sortField&sortDirection': function (
    backDelta, level, env, page, amountPerPage, sortField, sortDirection) {

    logMethodCall('messages/get?backDelta&level&env&page&amountPerPage&sortField&sortDirection',
      { backDelta, level, env, page, amountPerPage });

    this.unblock();

    let skip = (page - 1) * amountPerPage;

    let begining = moment().subtract(backDelta);
    let query = {
      timestamp: { $gte: begining.toDate() }
    };
    let sortParams = {};

    query = R.ifElse(R.isNil, R.always(query), R.assoc('environment', R.__, query))(env);
    query = R.ifElse(R.isNil, R.always(query), R.assoc('level', R.__, query))(level);

    sortParams = R.ifElse(R.isNil, R.always(sortParams),
      R.assoc(R.__, sortDirection, sortParams))(sortField);

    console.log('sort params:', sortParams);

    let qParams = {
      limit: amountPerPage,
      skip: skip,
      sort: sortParams,
    };

    return Messages.find(query, qParams).fetch();
  },
  'messages.clearEnvMessages?env'({ env }) {
    let deletedRows = 0;
    if (R.equals('All', env)) {
      deletedRows = Messages.remove({});
    }
    else if (!isNullOrEmpty(env)) {
      deletedRows = Messages.remove({ environment: env });
    }

    return deletedRows;
  }
});

function logMethodCall(name, args) {
  console.log(`method call: ${name}`);
  R.forEachObjIndexed((value, key) => {
    console.log(`${key}: ${R.toString(value)}`);
  }, args);
}