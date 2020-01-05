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
 * Template Component: User 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { parseReqId } from '/imports/lib/utilities';
import * as R from 'ramda';
import { remove, insert, update } from '/imports/api/accounts/methods';
import { Environments } from '/imports/api/environments/environments';
        
import './user.html';     
    
/*  
 * Lifecycles
 */   
  
Template.User.onCreated(function() {
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
    pageHeader: 'User',
    viewEnvs: [],
    editEnvs: [],
  });

  instance.autorun(function () {
    let controller = Iron.controller();
    let params = controller.getParams();
    let query = params.query;

    new SimpleSchema({
      action: { type: String, allowedValues: ['insert', 'view', 'remove', 'update'] },
      //env: { type: String, optional: true },
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
Template.User.rendered = function() {
};  
*/

/*
 * Events
 */

Template.User.events({
  'submit .sm-item-form': function(event, instance) {
    event.preventDefault(); 

    let _id = instance.state.get('id');
    let username = instance.$('.sm-input-username')[0].value;
    let password = instance.$('.sm-input-password')[0].value; 
    let viewEnvs = R.map(R.prop('value'), 
      instance.$('.sm-input-view-envs')[0].selectedOptions);
    let editEnvs = R.map(R.prop('value'), 
      instance.$('.sm-input-edit-envs')[0].selectedOptions);

    submitItem(instance,
      _id,
      username,
      password,
      viewEnvs,
      editEnvs
    ); 
  }
});
   
/*  
 * Helpers
 */

Template.User.helpers({    
  isUpdateableAction() {
    let instance = Template.instance();
    let action = instance.state.get('action');

    return R.contains(action, ['insert', 'update', 'remove']);
  },

  getState: function (key) {
    let instance = Template.instance();
    return instance.state.get(key);
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

  getModelField: function (fieldName) {
    let instance = Template.instance();
    return R.path([fieldName], instance.state.get('model'));
  },

  actionLabel: function () {
    let instance = Template.instance();
    let action = instance.state.get('action');
    return calcActionLabel(action);
  },

  viewEnvs: function () {
    let instance = Template.instance();
    return instance.state.get('viewEnvs');
  },

  editEnvs: function () {
    let instance = Template.instance();
    return instance.state.get('editEnvs');
  },

  envs: function () {
    return Environments.find({});
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
}); // end: helpers


function initInsertView(instance, query) {
  instance.state.set('action', query.action);
  //instance.state.set('env', query.env);
  
  instance.state.set('model', 
    {
      username: '',
      password: ''
    }
    /*.schema.clean({
    //environment: instance.state.get('env')
    })
    */
  );

  subscribeToOptionsData(instance);
  //instance.subscribe('constants');
  //instance.subscribe('link_types?env', query.env);
}

function initViewView(instance, query) {
  let reqId = parseReqId(query.id);

  instance.state.set('action', query.action);
  //instance.state.set('env', query.env);
  instance.state.set('id', reqId);

  subscribeToOptionsData(instance);
  subscribeToModel(instance, reqId.id);
  //instance.subscribe('constants');
  //instance.subscribe('link_types?_id', reqId.id);

}

function initUpdateView(instance, query) {
  let reqId = parseReqId(query.id);

  instance.state.set('action', query.action);
  //instance.state.set('env', query.env);
  instance.state.set('id', reqId);

  subscribeToOptionsData(instance);
  subscribeToModel(instance, reqId.id);
  //instance.subscribe('constants');
  //instance.subscribe('link_types?_id', reqId.id);
}

function initRemoveView(instance, query) {
  initViewView(instance, query);
}

function subscribeToOptionsData(instance) {
  instance.subscribe('constants');
  instance.subscribe('environments_config');
}

function subscribeToModel(instance, id) {
  instance.subscribe('users');

  Meteor.users.find({ _id: id }).forEach((model) => {
    instance.state.set('model', {
      _id: model._id,
      username: model.username,
      password: '******'
    });

    instance.subscribe('environments.view-env&userId', model._id);
    instance.subscribe('environments.edit-env&userId', model._id);

    let viewEnvsList = [];
    Environments.find({ 'auth.view-env': { $in: [ model._id  ] }}).forEach((viewEnv) => {
      viewEnvsList = R.union(viewEnvsList, [ viewEnv.name ]);
      instance.state.set('viewEnvs', viewEnvsList);
    });

    let editEnvsList = [];
    Environments.find({ 'auth.edit-env': { $in: [ model._id  ] }}).forEach((editEnv) => {
      editEnvsList = R.union(editEnvsList, [ editEnv.name ]);
      instance.state.set('editEnvs', editEnvsList);
    });
  }); 
}

function submitItem(
  instance, 
  id, 
  username,
  password,
  viewEnvs,
  editEnvs
  ){

  let action = instance.state.get('action');

  instance.state.set('isError', false);
  instance.state.set('isSuccess', false);
  instance.state.set('isMessage', false);
  instance.state.set('message', null);

  switch (action) {
  case 'insert':
    insert.call({
      username: username,
      password: password,
      viewEnvs: viewEnvs,
      editEnvs: editEnvs,
    }, processActionResult.bind(null, instance));
    break;

  case 'update': 
    update.call({
      _id: id.id,
      //password: password,
      viewEnvs: viewEnvs,
      editEnvs: editEnvs,
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

  } else {
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
  }
}

function calcActionLabel(action) {
  switch (action) {
  case 'insert':
    return 'Add';
  case 'remove':
    return 'Remove';
  default:
    return 'Submit';
  }
}
