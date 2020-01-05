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
import { Counts } from 'meteor/tmeasday:publish-counts';

import { 
  ScheduledScans,
  subsScheduledScansPageAmountSorted,
  subsScheduledScansPageAmountSortedCounter,
  subsScheduledScansId,
  subsScheduledScansEnv,
} from '../scheduled-scans.js';

Meteor.publish(subsScheduledScansPageAmountSorted, function (
  page, amountPerPage, sortField, sortDirection) {

  console.log(`server subscribtion: ${subsScheduledScansPageAmountSorted}`);
  console.log('page: ', page);
  console.log('amount: ', amountPerPage);
  console.log('sortField: ', sortField, R.isNil(sortField));
  console.log('sortDirection: ', sortDirection);

  let skip = (page - 1) * amountPerPage;

  let query = {};
  console.log('-query: ', query);
  let sortParams = {};

  sortParams = R.ifElse(R.isNil, R.always(sortParams), 
    R.assoc(R.__, sortDirection, sortParams))(sortField);

  console.log('sort params:', sortParams);

  let qParams = {
    limit: amountPerPage,
    skip: skip,
    sort: sortParams,
  };

  Counts.publish(this, subsScheduledScansPageAmountSortedCounter, ScheduledScans.find(query), {
    noReady: true
  });

  return ScheduledScans.find(query, qParams); 
});

Meteor.publish(subsScheduledScansId, function (_id) {
  console.log(`server subscribtion: ${subsScheduledScansId}`);
  console.log('-id: ', _id);

  //let that = this;

  let query = { _id: _id };
  return ScheduledScans.find(query); 
});

Meteor.publish(subsScheduledScansEnv, function (env) {
  console.log(`server subscribtion: ${subsScheduledScansEnv}`);
  console.log('-env: ', env);

  //let that = this;

  let query = { environment: env };
  return ScheduledScans.find(query); 
});
