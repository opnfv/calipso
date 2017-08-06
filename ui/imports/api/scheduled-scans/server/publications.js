import { Meteor } from 'meteor/meteor';
import * as R from 'ramda';
import { Counts } from 'meteor/tmeasday:publish-counts';

import { ScheduledScans,
  subsScheduledScansPageAmountSorted,
  subsScheduledScansPageAmountSortedCounter,
  subsScheduledScansId,
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
