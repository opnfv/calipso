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
 * Template Component: CliqueConstraint 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import * as R from 'ramda';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { CliqueConstraints } from '/imports/api/clique-constraints/clique-constraints';
import { Environments } from '/imports/api/environments/environments';
import { Constants } from '/imports/api/constants/constants';
import { insert, remove, update } from '/imports/api/clique-constraints/methods';
import { parseReqId } from '/imports/lib/utilities';
        
import './clique-constraint.html';
import {toOptions} from "../../../lib/utilities";
    
/*  
 * Lifecycles
 */   
  
Template.CliqueConstraint.onCreated(function() {
  let instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    id: null,
    //env: null,
    action: 'insert',
    isError: false,
    isSuccess: false,
    isMessage: false,
    message: null,
    disabled: false,
    notifications: {},
    model: {},
    pageHeader: 'Clique Constraint'
  });

  instance.autorun(function () {
    let controller = Iron.controller();
    let params = controller.getParams();
    let query = params.query;

    new SimpleSchema({
      action: { type: String, allowedValues: ['insert', 'view', 'remove', 'update'] },
      id: { type: String, optional: true }
    }).validate(query);

    switch (query.action) {
    case 'insert':
      initInsertView(instance, query); 
      break;

    case 'view':
      initViewView(instance, query);
      break;

    case 'update':
      initUpdateView(instance, query);
      break;

    case 'remove':
      initRemoveView(instance, query);
      break;

    default:
      throw 'unimplemented action';
    }
  });
});  

/*
Template.CliqueConstraint.rendered = function() {
};  
*/

/*
 * Events
 */

Template.CliqueConstraint.events({
  'submit .sm-item-form': function(event, instance) {
    event.preventDefault(); 

    let _id = instance.state.get('id');
    let focalPointType = instance.$('.sm-input-focal-point-type')[0].value;
    let env = instance.$('.sm-input-environment')[0].value;
    let constraints = R.map(R.prop('value'), 
      instance.$('.sm-input-constraints')[0].selectedOptions);

    submitItem(instance,
      _id,
      focalPointType,
      env,
      constraints
    );
  }
});
   
/*  
 * Helpers
 */

Template.CliqueConstraint.helpers({    
  isUpdateableAction() {
    let instance = Template.instance();
    let action = instance.state.get('action');

    return R.contains(action, ['insert', 'update', 'remove']);
  },

  getState: function (key) {
    let instance = Template.instance();
    return instance.state.get(key);
  },

  objectTypesList: function () {
    return Constants.getByName('object_types_for_links');
  },

  environmentsList: function () {
    return toOptions(Environments.findAllNames());
  },

  getAttrDisabled: function () {
    let instance = Template.instance();
    let result = {};
    let action = instance.state.get('action');

    if (R.contains(action, ['view', 'remove'])) {
      result = R.assoc('disabled', true, result);
    }

    return result;
  },

  getModel: function () {
    let instance = Template.instance();
    return instance.state.get('model');
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
  },

  getAttrSelectedMultiple: function (optionValue, modelValues) {
    let result = {};

    if (R.isNil(modelValues)) { return result; }

    if (R.contains(optionValue, modelValues)) {
      result = R.assoc('selected', 'selected', result);
    }

    return result;
  },

  actionLabel: function () {
    let instance = Template.instance();
    let action = instance.state.get('action');
    return calcActionLabel(action);
  }
});


function initInsertView(instance, query) {
  instance.state.set('action', query.action);
  instance.state.set('model', CliqueConstraints.schema.clean({
  }));

  subscribeToOptionsData(instance);
  //instance.subscribe('link_types?env', query.env);
}

function initViewView(instance, query) {
  let reqId = parseReqId(query.id);

  instance.state.set('action', query.action);
  instance.state.set('id', reqId);

  subscribeToOptionsData(instance);

  instance.subscribe('clique_constraints?_id', reqId.id);

  CliqueConstraints.find({ _id: reqId.id }).forEach((model) => {
    instance.state.set('model', model);
  }); 
}

function initUpdateView(instance, query) {
  let reqId = parseReqId(query.id);

  instance.state.set('action', query.action);
  instance.state.set('id', reqId);

  subscribeToOptionsData(instance);
  instance.subscribe('clique_constraints?_id', reqId.id);

  CliqueConstraints.find({ _id: reqId.id }).forEach((model) => {
    instance.state.set('model', model);
  }); 
}

function initRemoveView(instance, query) {
  initViewView(instance, query);
}

function subscribeToOptionsData(instance) {
  instance.subscribe('link_types');
  instance.subscribe('constants');
  instance.subscribe('environments_config');
}

function submitItem(
  instance, 
  id, 
  focal_point_type,
  env,
  constraints 
 ) {

  let action = instance.state.get('action');

  instance.state.set('isError', false);
  instance.state.set('isSuccess', false);
  instance.state.set('isMessage', false);
  instance.state.set('message', null);

  switch (action) {
  case 'insert':
    insert.call({
      focal_point_type: focal_point_type,
      environment: env,
      constraints: constraints,
    }, processActionResult.bind(null, instance));
    break;

  case 'update': 
    update.call({
      _id: id.id,
      focal_point_type: focal_point_type,
      environment: env,
      constraints: constraints,
    }, processActionResult.bind(null, instance));
    break;

  case 'remove':
    remove.call({
      _id: id.id
    }, processActionResult.bind(null, instance));
    break;

  default:
      // todo
    break;
  }
}

function processActionResult(instance, error) {
  let action = instance.state.get('action');

  if (error) {
    instance.state.set('isError', true);
    instance.state.set('isSuccess', false);
    instance.state.set('isMessage', true);

    if (typeof error === 'string') {
      instance.state.set('message', error);
    } else {
      instance.state.set('message', error.message);
    }

    return;
  }

  instance.state.set('isError', false);
  instance.state.set('isSuccess', true);
  instance.state.set('isMessage', true);

  switch (action) {
  case 'insert':
    instance.state.set('message', 'Record had been added successfully');
    instance.state.set('disabled', true);
    break;  

  case 'remove':
    instance.state.set('message', 'Record had been removed successfully');
    instance.state.set('disabled', true);
    break;

  case 'update':  
    instance.state.set('message', 'Record had been updated successfully');
    break;
  }

  Router.go('/clique-constraints-list');
}

function calcActionLabel(action) {
  switch (action) {
  case 'insert':
    return 'Add';
  case 'remove':
    return 'Remove';
  case 'update':
    return 'Update';
  default:
    return 'Submit';
  }
}
