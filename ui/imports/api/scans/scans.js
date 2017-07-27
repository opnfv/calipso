/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { Mongo } from 'meteor/mongo';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';

import { Constants } from '/imports/api/constants/constants';
import { StatusesInOperation } from '/imports/api/constants/data/scans-statuses';

export const Scans = new Mongo.Collection('scans', { idGeneration: 'MONGO' });

Scans.schemaRelated = {
  environment: {
    label: 'Environment',
    description: 'Name of environment to scan',
    disabled: true,
  },
  status: {
    label: 'Status',
    description: 'Scan lifecycle status',
    subtype: 'select',
    options: 'scans_statuses',
    disabled: true,
  },
  object_id: {
    label: 'Scan specific object',
    description: 'Object ID',
  },
  log_level: {
    label: 'Log level',
    description: 'logging level',
    subtype: 'select',
    options: 'log_levels',
  },
  clear: {
    label: 'Clear data',
    description: 'clear all data prior to scanning',
  },
  scan_only_inventory: {
    label: 'Scan only inventory',
    description: 'do only scan to inventory',
  },
  scan_only_links: {
    label: 'Scan only links',
    description: 'do only links creation',
  },
  scan_only_cliques: {
    label: 'Scan only cliques',
    description: 'do only cliques creation',
  },
};

Scans.scansOnlyFields = ['scan_only_inventory', 'scan_only_links', 'scan_only_cliques'];

let schema = {
  _id: { type: { _str: { type: String, regEx: SimpleSchema.RegEx.Id } } },
  environment: { 
    type: String 
  }, 
  status: {
    type: String, 
    defaultValue: 'draft', 
    custom: function () {
      let that = this;
      let statuses = Constants.findOne({ name: 'scans_statuses' }).data;

      if (R.isNil(R.find(R.propEq('value', that.value), statuses))) {
        return 'notAllowed';
      }
    },
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
    defaultValue: false,
  },
  scan_only_links: {
    type: Boolean,
    defaultValue: false,
  },
  scan_only_cliques: {
    type: Boolean,
    defaultValue: false,
  },
  submit_timestamp: {
    type: Date,
    defaultValue: null
  },

};

Scans.schema = new SimpleSchema(schema);
Scans.schema.addValidator(function () {
  let that = this;
  let env = that.field('environment').value;

  let currentScansCount = Scans.find({
    environment: env,
    status: { $in: StatusesInOperation }
  }).count();

  if (currentScansCount > 0) {
    throw {
      isError: true,
      type: 'notUinque',
      data: [],
      message: 'There is already a scan in progress.'
    };
  }

  let scanOnlyFields = R.filter( f => that.field(f).value, Scans.scansOnlyFields);

  if(scanOnlyFields.length > 1) {
    throw {
      isError: true,
      type: 'conflict',
      data: scanOnlyFields,
      message: 'Only one of the scan only fields can be selected'
    };
  }

});

Scans.attachSchema(Scans.schema);

Scans.schemaRelated = R.mapObjIndexed((relatedItem, key) => {
  return R.merge(relatedItem, {
    type: schema[key].type 
  });

}, Scans.schemaRelated);

export const subsScansEnvPageAmountSorted = 'scans?env*&page&amount&sortField&sortDirection';
export const subsScansEnvPageAmountSortedCounter = `${subsScansEnvPageAmountSorted}!counter`;
