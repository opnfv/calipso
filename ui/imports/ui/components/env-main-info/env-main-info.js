/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: EnvMainInfo
 */

//import { Meteor } from 'meteor/meteor';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import * as R from 'ramda';

import '/imports/ui/components/input-model/input-model';
import '/imports/ui/components/select-model/select-model';
import { createInputArgs } from '/imports/ui/lib/input-model';
import { createSelectArgs } from '/imports/ui/lib/select-model';
import { Constants } from '/imports/api/constants/constants';

import './env-main-info.html';

/*
 * Lifecycles
 */

Template.EnvMainInfo.onCreated(function () {
  let instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    action: null,
  });

  instance.autorun(function () {
    let action = Template.currentData().action;
    instance.state.set('action', action);

    instance.subscribe('constants');
  });

});

/*
Template.EnvironmentWizard.rendered = function(){
};
*/
 
/*
 * Helpers
 */

Template.EnvMainInfo.helpers({
  /*
  createInputArgs: function (params) {
    let instance = Template.instance();
    return {
      context: params.hash.context,
      key: params.hash.key,
      type: params.hash.type,
      placeholder: params.hash.placeholder,
      setModel: instance.data.setModel 
    };
  }*/
  createInputArgs: createInputArgs,

  createSelectArgs: createSelectArgs,

  distributionOptions: function () {
    let item = Constants.findOne({ name: 'distributions' });
    if (R.isNil(item)) { return []; }
    return item.data;
  },

  /* depracated 
  networkOptions: function () {
    let item = Constants.findOne({ name: 'network_plugins' });
    if (R.isNil(item))  { return []; }
    return item.data;
  },
  */
 
  typeDriversOptions: function () {
    let item = Constants.findOne({ name: 'type_drivers' });
    if (R.isNil(item))  { return []; }
    return item.data;
  },
 
  mechanismDriversOptions: function () {
    let item = Constants.findOne({ name: 'mechanism_drivers' });
    if (R.isNil(item))  { return []; }
    return item.data;
  },
 
  isFieldDisabled: function (fieldName, globalDisabled) {
    let instance = Template.instance();
    if (globalDisabled) { return true; }

    return  isDisabledByField(fieldName, instance.state.get('action'));
  }
});

/*
 * Events
 */

Template.EnvMainInfo.events({
  'click .sm-next-button': function () {
    let instance = Template.instance();
    instance.data.onNextRequested(); 
  }
});

function isDisabledByField(fieldName, actionName) {
  if (R.contains(fieldName, ['name', 'distribution']) && actionName !== 'insert') {
    return true;
  }
  
  return false;
}
