///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import { check } from 'meteor/check';
import * as R from 'ramda';
import { ScheduledScans } from '../scheduled-scans';

Meteor.methods({
  'scheduledScansFind?env': function (env) {
    console.log('method server: scheduledScansFind?env', R.toString(env));

    check(env, String);
    this.unblock();

    let query = { environment: env };
    let scheduledScan = ScheduledScans.findOne(query, {});

    return {
      item: scheduledScan
    };
  }
});
