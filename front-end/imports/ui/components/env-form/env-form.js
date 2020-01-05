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
 * Template Component: envForm
 */

import * as R from 'ramda';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { Environments } from '/imports/api/environments/environments';
import { parseReqId } from '/imports/lib/utilities';

import './env-form.html';

/*
 * Lifecycle methods
 */

Template.envForm.onCreated(function () {
  var instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    selectedEnv: null
  });


  instance.autorun(function() {
    let data = R.when(R.isNil, R.always({}), Template.currentData());

    new SimpleSchema({
      selectedEnvironment: {
        type: Object,
        blackbox: true,
        optional: true
      },
      onEnvSelected: { type: Function }
    }).validate(data);

    instance.state.set('selectedEnv', data.selectedEnvironment);

    instance.subscribe('environments_config');
  });
});

/*
 * Events
 */  

Template.envForm.events({
  'click .os-env-form-dropdown-menu .sm-env-item': function (event, _instance) {
    event.preventDefault();

    let envName = R.path(['target','dataset', 'envName'], event);
    let _id = R.path(['target', 'dataset', 'envId'], event);

    if (R.isNil(envName)) { return; }
    _id = parseReqId(_id);

    let data = Template.currentData();
    if (data.onEnvSelected) {
      data.onEnvSelected({
        _id: _id.id,
        name: envName
      });
    }
  }
});

/*
 * Helpers
 */   

Template.envForm.helpers({
  selectedEnvName: function () {
    let instance = Template.instance();
    let selectedEnv = instance.state.get('selectedEnv');

    let envName = R.when(
      R.isNil, 
      R.always('MY ENVIRONMENTS')
    )(R.path(['name'], selectedEnv));

    return envName;
  },

  envList: function () {
    return Environments.find({});
  },
});
