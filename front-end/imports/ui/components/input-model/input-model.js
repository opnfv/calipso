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
 * Template Component: InputModel
 */

//import { Meteor } from 'meteor/meteor';
import { Template } from 'meteor/templating';
//import { ReactiveDict } from 'meteor/reactive-dict';
import * as R from 'ramda';

import './input-model.html';

/*
 * Lifecycles
 */

Template.InputModel.onCreated(function () {
});

/*
Template.InputModel.rendered = function() {
};
*/

/*
 * Events
 */

Template.InputModel.events({
  'input .inputField': function (event, instance) {
    if (instance.data.type === 'checkbox') { return; }

    let value;
    switch (event.target.type) {
      case 'number':
        value = event.target.valueAsNumber;
        break;

      default:
        value = event.target.value;
    }

    instance.data.setModel(value);
  },
  'click .inputField': function (event, instance) {
    if (instance.data.type !== 'checkbox') { return; }

    let element = instance.$('.inputField')[0];
    instance.data.setModel(element.checked);
  }
});

/*
 * Helpers
 */

Template.InputModel.helpers({
  calcAttrs: function () {
    let instance = Template.instance();
    let attrs = {};

    if (instance.data.type === 'checkbox') {
      if (instance.data.value) {
        attrs.checked = true;
      }
    } else {
      attrs.value = instance.data.value;
    }

    return attrs;
  },

  calcType: function () {
    let instance = Template.instance();
    return instance.data.type;
  },

  calcId: function () {
  },

  calcName: function () {
  },

  calcClass: function () {
    let instance = Template.instance();
    if (R.isNil(instance.data.classes)) {
      return 'form-control';
    } else {
      return instance.data.classes;
    }
  },

  isCalcTypeCheckbox: function() {
    let instance = Template.instance();
    return instance.data.type === "checkbox";
  },

  isCalcTypeEmail: function() {
    let instance = Template.instance();
    return instance.data.type === "email";
  },

  isCalcTypePassword: function() {
    let instance = Template.instance();
    return instance.data.type === "password";
  },

  isCalcTypeNumber: function() {
    let instance = Template.instance();
    return instance.data.type === "number";
  },

  calcPlaceholder: function () {
    let instance = Template.instance();
    if (R.isNil(instance.data.placeholder)) { return ''; }

    return instance.data.placeholder;
  },

  markIfDisabled: function () {
    let instance = Template.instance();
    let attrs = {};
    if (instance.data.disabled) {
      attrs = R.assoc('disabled', true, attrs);
    }

    return attrs;
  }
});
