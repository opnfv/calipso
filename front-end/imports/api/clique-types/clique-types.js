///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import { Mongo } from 'meteor/mongo';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';
import { Constants } from '/imports/api/constants/constants';
import { Environments } from '/imports/api/environments/environments';
import { LinkTypes } from '/imports/api/link-types/link-types';
import {callApiValidators} from "../../lib/utilities";

export const CliqueTypes = new Mongo.Collection(
  'clique_types', { idGeneration: 'MONGO' });

let schema = {
  _id: { type: { _str: { type: String, regEx: SimpleSchema.RegEx.Id } } },

  environment: {
    type: String,
    defaultValue: "",
    optional: true,
    custom: function () {
      let that = this;
      if (that.value !== that.definition.defaultValue) {
        let env = Environments.findOne({name: that.value});

        if (R.isNil(env)) {
          return 'notAllowed';
        }
      }

      // Document validators workaround
      let validators = [requiredFieldsValidator, focalPointValidator,
                        nameValidator, duplicateConfigurationValidator];
      return callApiValidators(that, validators);
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

  environment_type: {
    type: String,
    defaultValue: null,
    optional: true,
    custom: function () {
        return Constants.validateValue('environment_types', this);
    }
  },

  distribution: {
    type: String,
    defaultValue: null,
    optional: true,
    custom: function () {
        return Constants.validateValue('distributions', this);
    }
  },

  distribution_version: {
    type: String,
    defaultValue: null,
    optional: true,
    custom: function () {
        return Constants.validateValue('distribution_versions', this);
    }
  },

  mechanism_drivers: {
    type: String,
    defaultValue: null,
    optional: true,
    custom: function () {
      return Constants.validateValue('mechanism_drivers', this);
    }
  },

  type_drivers: {
    type: String,
    defaultValue: null,
    optional: true,
    custom: function () {
      return Constants.validateValue('type_drivers', this);
    }
  },

  use_implicit_links: {
    type: Boolean
  },
};

let simpleSchema = new SimpleSchema(schema);

function focalPointValidator(that) {
  // Validate focal point uniqueness
  console.log("Validator: focal point uniqueness");
  if (isEmpty(that.field('environment').value)) {
    return;
  }

  let existing = CliqueTypes.findOne({
    environment: that.field('environment').value,
    focal_point_type: that.field('focal_point_type').value
  });

  if (R.allPass([
    R.pipe(R.isNil, R.not),
    R.pipe(R.propEq('_id', that.docId), R.not)
  ])(existing)) {
    console.warn("Duplicate focal point type in env");
    return 'alreadyExists';
  }
}

function nameValidator(that) {
  // Validate name uniqueness
  console.log("Validator: name uniqueness");

  let existing = CliqueTypes.findOne({
    environment: that.field('environment').value,
    name: that.field('name').value
  });

  if (R.allPass([
    R.pipe(R.isNil, R.not),
    R.pipe(R.propEq('_id', that.docId), R.not)
  ])(existing)) {
    console.warn("Duplicate name in env");
    return 'alreadyExists';
  }
}

export function isEmpty(obj) {
    return R.isEmpty(obj) || R.isNil(obj)
}

function requiredFieldsValidator(that) {
  // Validate all required fields
  console.log("Validator: required fields");

  if (isEmpty(that.field('environment').value)
      && isEmpty(that.field('environment_type').value)) {
    console.warn('insufficientCliqueTypeData');
    return 'insufficientCliqueTypeData';
  }
  if (isEmpty(that.field('focal_point_type').value)) {
    console.warn('noFocalPoint');
    return 'noFocalPoint';
  }
  if (!isEmpty(that.field('distribution_version').value)
      && isEmpty(that.field('distribution').value)) {
    console.warn('versionWithoutDistribution');
    return 'versionWithoutDistribution';
  }

}

function duplicateConfigurationValidator(that) {
  // Validate that the clique type configuration is not a duplicate
  // Environment-specific duplicates are handled in other validators
  console.log("Validator: duplicate clique type configuration");
  if (!isEmpty(that.field('environment').value)) {
    return;
  }

  let fields = ['distribution', 'mechanism_drivers', 'type_drivers'];
  let search = {
      'environment_type': that.field('environment_type').value,
      'focal_point_type': that.field('focal_point_type').value
  };
  for (let i = 0; i < fields.length; ++i) {
      let field = fields[i];
      let value = that.field(field).value;
      if (!isEmpty(value)) {
          search[field] = value;
          if (field === 'distribution') {
              let dv = that.field('distribution_version').value;
              search['distribution_version'] = !isEmpty(dv) ? dv : null;
          }
      }
      else {
          search[field] = null;
      }
  }

  let existing = CliqueTypes.findOne(search);
  if (R.allPass([R.pipe(R.isNil, R.not),
                 R.pipe(R.propEq('_id', that.docId), R.not)])(existing)) {
      console.warn("Duplicate clique type");
      return 'alreadyExists';
    }
}

CliqueTypes.schema = simpleSchema;
CliqueTypes.attachSchema(CliqueTypes.schema);
