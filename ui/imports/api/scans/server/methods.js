/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { check } from 'meteor/check';
import * as R from 'ramda';
import { Scans } from '../scans';
import { Environments } from '/imports/api/environments/environments';

Meteor.methods({
  'scansFind?start-timestamp-before': function (startTimestamp) {
    console.log('method server: scanFind?start-timestamp-before', 
      R.toString(startTimestamp));

    check(startTimestamp, Date);
    this.unblock();

    let query = { start_timestamp: { $lt: startTimestamp }};
    let scan = Scans.findOne(query, {
      sort: { start_timestamp: -1 }
    });

    let environment = R.ifElse(
      R.isNil,
      R.always(null),
      (scan) => {
        console.log('finding environment:', scan.environment);
        let env = Environments.findOne({ name: scan.environment });
        console.log('found env:', env);
        return env;
      })(scan); 

    console.log('found scan', scan);

    return {
      environment: environment,
      scan: scan,
    };
  },
});
