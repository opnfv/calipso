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
