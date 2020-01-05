///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: MessagesDeleteModal 
 */
import * as R from 'ramda';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { Environments } from '/imports/api/environments/environments';
import './messages-delete-modal.html';
import { toOptions, isNullOrEmpty } from "../../../lib/utilities";


Template.MessagesDeleteModal.onCreated(function () {
  let instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    id: null,
    model: {},
  });
});

Template.MessagesDeleteModal.events({
  'click .sm-button-delete': function (_event, _instance) {
    let onDeleteReq = Template.currentData().onDeleteReq;
    let env = _instance.$('.sm-input-msgmodal')[0].value;

    if (isNullOrEmpty(env)) {
      return;
    };

    Meteor.call('messages.clearEnvMessages?env', { env: env }, (err, res) => {
      if (!R.isNil(err)) {
        toastr.error('Clear Messages Failed.', { timeOut: 5000 });
        return;
      }

      if (R.and(!R.isNil(res), R.gt(res, 0))) {
        toastr.success(`Clearing ${env} messages was successful.`, { timeOut: 5000 });
        onDeleteReq();
      }
      else {
        toastr.info(`No Messages To Clear.`, { timeOut: 5000 });
      }

      _instance.$('#messages-delete-modal').modal('hide');
    });
  }
});

Template.MessagesDeleteModal.helpers({
  environmentsList: function () {
    return toOptions(Environments.findAllNames());
  },

  getModelField: function (fieldName) {
    let instance = Template.instance();
    return R.path([fieldName], instance.state.get('model'));
  },

  getAttrSelected: function (optionValue, modelValue) {
    let result = {};

    if (optionValue === modelValue) {
      result = R.assoc('selected', 'selected', result);
    }

    return result;
  }
});