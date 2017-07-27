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
import { Environments } from '/imports/api/environments/environments';
import { Constants } from '/imports/api/constants/constants';

export const Messages = new Mongo.Collection('messages', { idGeneration: 'MONGO' });

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

  id: {
    type: String
  }, 

  viewed: {
    type: Boolean,
    defaultValue: false
  },

  display_context: {
    type: String
  },

  message: {
    type: Object,
    blackbox: true
  },

  source_system: {
    type: String,
    custom: function () {
      let that = this;
      let values = Constants.findOne({ name: 'message_source_systems' }).data;

      if (R.isNil(R.find(R.propEq('value', that.value), values))) {
        return 'notAllowed';
      }
    }
  },

  level: {
    type: String
  },

  timestamp: {
    type: Date
  },

  related_object_type: {
    type: String
  },

  related_object: {
    type: String
  },

  scan_id: {
    type: Date
  }
};

let simpleSchema = new SimpleSchema(schema);

Messages.schema = simpleSchema;
Messages.attachSchema(Messages.schema);

export function calcIconForMessageLevel(level) {
  switch (level) {
  case 'info':
    return 'notifications';
  case 'warning':
    return 'warning';
  case 'error':
    return 'error';
  default:
    return 'notifications';
  }
}

export function lastMessageTimestamp (level, envName) {
  let query = { level: level };
  query = R.ifElse(R.isNil, R.always(query), R.assoc('environment', R.__, query))(envName);

  let message =  Messages.findOne(query, {
    sort: { timestamp: -1 } 
  });

  let res = R.path(['timestamp'], message);
  if (R.isNil(res)) { return null; }
  return (res instanceof String) ? res : res.toString();
}

export function calcColorClassForMessagesInfoBox(level) {
  switch (level) {
  case 'info':
    return 'green-text';
  case 'warning':
    return 'orange-text';
  case 'error':
    return 'red-text';
  default:
    return 'green-text';
  }
}
