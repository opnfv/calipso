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
import { Environments } from '/imports/api/environments/environments';
import { LinkTypes } from '/imports/api/link-types/link-types';

export const CliqueTypes = new Mongo.Collection(
  'clique_types', { idGeneration: 'MONGO' });

let schema = {
  _id: { type: { _str: { type: String, regEx: SimpleSchema.RegEx.Id } } },

  environment: {
    type: String,
    custom: function () {
      let that = this;
      let env = Environments.findOne({ name: that.value });

      if (R.isNil(env)) {
        return 'notAllowed';
      }
    }
  },

  focal_point_type: {
    type: String,
    custom: function () {
      let that = this;
      let values = Constants.findOne({ name: 'object_types_for_links' }).data;

      if (R.isNil(R.find(R.propEq('value', that.value), values))) {
        return 'notAllowed';
      }
    }
  },

  link_types: {
    type: [String],
    minCount: 1,
    defaultValue: [],
    custom: function () {
      let that = this;
      let findResult = R.all(function (pLinkType) {
        if (R.isNil(LinkTypes.findOne({ type: pLinkType }))) {
          return false;
        }

        return true;
      }, that.value);

      if (! findResult) { return 'notAllowed'; }

      return;
    },
  },

  name: {
    type: String
  },
};

let simpleSchema = new SimpleSchema(schema);

simpleSchema.addValidator(function () {
  let that = this;

  let existing = CliqueTypes.findOne({ 
    environment: that.field('environment').value,
    focal_point_type: that.field('focal_point_type').value
  });

  if (R.allPass([
    R.pipe(R.isNil, R.not), 
    R.pipe(R.propEq('_id', that.docId), R.not)
  ])(existing)) { 

    return 'alreadyExists';
  }
});

simpleSchema.addValidator(function () {
  let that = this;

  let existing = CliqueTypes.findOne({ 
    environment: that.field('environment').value,
    name: that.field('name').value
  });

  if (R.allPass([
    R.pipe(R.isNil, R.not), 
    R.pipe(R.propEq('_id', that.docId), R.not)
  ])(existing)) { 

    return 'alreadyExists';
  }
});

CliqueTypes.schema = simpleSchema;
CliqueTypes.attachSchema(CliqueTypes.schema);
