import { Mongo } from 'meteor/mongo';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { Constants } from '/imports/api/constants/constants';
import * as R from 'ramda';

export const ScheduledScans = new Mongo.Collection('scheduled_scans', { idGeneration: 'MONGO' });

export const scansOnlyFields = ['scan_only_inventory', 'scan_only_links', 'scan_only_cliques'];

let schema = new SimpleSchema({
  _id: { type: { _str: { type: String, regEx: SimpleSchema.RegEx.Id } } },
  environment: { 
    type: String 
  }, 
  object_id: {
    type: String,
    optional: true,
  },
  log_level: {
    type: String,
    defaultValue: 'warning', 
    custom: function () {
      let that = this;
      let logLevels = Constants.findOne({ name: 'log_levels' }).data;

      if (R.isNil(R.find(R.propEq('value', that.value), logLevels))) {
        return 'notAllowed';
      }
    },
  },
  clear: {
    type: Boolean,
    defaultValue: true, 
  },
  scan_only_inventory: {
    type: Boolean,
    defaultValue: true,
  },
  scan_only_links: {
    type: Boolean,
    defaultValue: false,
  },
  scan_only_cliques: {
    type: Boolean,
    defaultValue: false,
  },
  freq: {
    type: String,
    defaultValue: 'WEEKLY',
  },
  submit_timestamp: {
    type: Date,
    defaultValue: null
  },
  scheduled_timestamp: {
    type: Date,
    defaultValue: null,
    optional: true,
  }
});

schema.addValidator(function () {
  let that = this;
  let currentScansOnlyFields = 
    R.reject( f => that.field(f).value == false, scansOnlyFields);

  if(currentScansOnlyFields.length > 1) {
    throw {
      isError: true,
      type: 'conflict',
      data: currentScansOnlyFields,
      message: `Only one of the scan only fields can be selected. ${R.toString(currentScansOnlyFields)}`
    };
  }
});

ScheduledScans.schema = schema;
ScheduledScans.attachSchema(ScheduledScans.schema);

export const subsScheduledScansPageAmountSorted = 'scheduled_scans?page&amount&sortField&sortDirection';
export const subsScheduledScansPageAmountSortedCounter = `${subsScheduledScansPageAmountSorted}!counter`;

export const subsScheduledScansId = 'scheduled_scans?_id';
