/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: Message 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import * as R from 'ramda';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { Messages } from '/imports/api/messages/messages';
import { Constants } from '/imports/api/constants/constants';
import { Environments } from '/imports/api/environments/environments';
import { idToStr } from '/imports/lib/utilities';
//import { insert, update, remove } from '/imports/api/clique-types/methods';
import { parseReqId } from '/imports/lib/utilities';
//import { store } from '/imports/ui/store/store';
//import { setCurrentNode } from '/imports/ui/actions/navigation';
        
import './message.html';     
    
/*  
 * Lifecycles
 */   
  
Template.Message.onCreated(function() {
  let instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    id: null,
    action: 'insert',
    isError: false,
    isSuccess: false,
    isMessage: false,
    message: null,
    disabled: false,
    notifications: {},
    model: {},
    pageHeader: 'Message'
  });

  instance.autorun(function () {
    let data = Template.currentData();

    new SimpleSchema({
      action: { type: String, allowedValues: ['view'] },
      id: { type: String, optional: true }
    }).validate(data);

    switch (data.action) {
    /*
    case 'insert':
      initInsertView(instance, data); 
      break;
      */

    case 'view':
      initViewView(instance, data);
      break;

    /*
    case 'update':
      initUpdateView(instance, data);
      break;

    case 'remove':
      initRemoveView(instance, data);
      break;
    */

    default:
      throw 'unimplemented action';
    }
  });
});  

/*
Template.Message.rendered = function() {
};  
*/

/*
 * Events
 */

Template.Message.events({
  'click .sm-field-group-display-context': function (event, instance) {
    event.preventDefault();

    let model = instance.state.get('model');
    let environment = Environments.findOne({ name: model.environment });
    let nodeId = model.display_context;

    Meteor.apply('inventoryFindNode?env&id', [
      environment.name,
      nodeId,
    ], {
      wait: false
    }, function (err, resp) {
      if (err) { 
        console.error(R.toString(err));
        return; 
      }

      if (R.isNil(resp.node)) {
        console.error('error finding node related to message', R.toString(nodeId));
        return;
      }

      Router.go('environment', { 
        _id: idToStr(environment._id) 
      }, { 
        query: {
          selectedNodeId: idToStr(resp.node._id)
        } 
      });

    });

  },

});
   
/*  
 * Helpers
 */

Template.Message.helpers({    
  isUpdateableAction() {
    let instance = Template.instance();
    let action = instance.state.get('action');

    return R.contains(action, ['insert', 'update', 'remove']);
  },

  getState: function (key) {
    let instance = Template.instance();
    return instance.state.get(key);
  },

  envsList: function () {
    return Environments.find({});
  },

  sourceSystemsList: function () {
    return R.ifElse(R.isNil, R.always([]), R.prop('data')
    )(Constants.findOne({ name: 'message_source_systems' }));
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
  },

  argsInvPropDisplay: function (env, nodeId) {
    return {
      env: env,
      nodeId: nodeId,
      displayFn: (node) => {
        if (R.isNil(node)) { return ''; }
        return `${node.object_name} - ${node.type}`;
      }
    };
  },
}); // end - helpers


function initViewView(instance, data) {
  let reqId = parseReqId(data.id);

  instance.state.set('action', data.action);
  //instance.state.set('env', query.env);
  instance.state.set('id', reqId);

  subscribeToOptionsData(instance);
  instance.subscribe('messages?_id', reqId.id);

  Messages.find({ _id: reqId.id }).forEach((model) => {
    instance.state.set('model', model);
  }); 

}

function subscribeToOptionsData(instance) {
  instance.subscribe('environments_config');
  instance.subscribe('constants');
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
