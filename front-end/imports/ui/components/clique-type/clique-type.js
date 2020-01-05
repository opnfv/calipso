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
 * Template Component: CliqueType 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import * as R from 'ramda';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
//import { Constants } from '/imports/api/constants/constants';
import { CliqueTypes, isEmpty } from '/imports/api/clique-types/clique-types';
import { Environments } from '/imports/api/environments/environments';
import { Constants } from '/imports/api/constants/constants';
import { EnvironmentOptions } from '/imports/api/environment_options/environment_options';
import { LinkTypes } from '/imports/api/link-types/link-types';
import { insert, update, remove } from '/imports/api/clique-types/methods';
import { parseReqId } from '/imports/lib/utilities';
        
import '/imports/ui/components/selectable-ordered-input/selectable-ordered-input';

import './clique-type.html';     
    
/*  
 * Lifecycles
 */   
  
Template.CliqueType.onCreated(function() {
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
    pageHeader: 'Clique Type'
  });

  instance.autorun(function () {
    let controller = Iron.controller();
    let params = controller.getParams();
    let query = params.query;

    new SimpleSchema({
      action: { type: String, allowedValues: ['insert', 'view', 'update', 'remove'] },
      env: { type: String, optional: true },
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
Template.CliqueType.rendered = function() {
};  
*/

/*
 * Events
 */

Template.CliqueType.events({
  'change #env-select': function (event, instance) {
    let inputs = instance.$('.conf-input');
    if (!event.target.value) {
      inputs.removeProp("disabled");
    }
    else {
      inputs.prop("disabled", true);
    }
  },
  'change #environment-type-input': function(event, instance) {
    // Update the model with new selected environment type
    let envType = instance.$('.sm-input-environment-type')[0].value;
    let newModel = instance.state.get('model');
    newModel = R.dissoc('distribution',
               R.dissoc('type_drivers',
               R.dissoc('mechanism_drivers',
               R.dissoc('distribution_version',
               R.assoc('environment_type', envType, newModel)))));
    instance.state.set('model', newModel);

    instance.$('.env-options-input')
          .find("option:selected")
          .prop("selected", false);
    instance.$('#distribution-input')
          .find("option:selected")
          .prop("selected", false);
  },
  'change #distribution-input': function (event, instance) {
    // Update the model with new selected distribution
    let distribution = instance.$('.sm-input-distribution')[0].value;
    let newModel = instance.state.get('model');
    newModel = R.dissoc('type_drivers',
               R.dissoc('mechanism_drivers',
               R.dissoc('distribution_version',
               R.assoc('distribution', distribution, newModel))));
    instance.state.set('model', newModel);

    instance.$('.env-options-input')
            .find("option:selected")
            .prop("selected", false);
  },
  'change .conf-input': function (event, instance) {
    let non_empty_fields = $('.conf-input').filter(function(i, elem) {
      return !isEmpty(elem.value);
    });

    let env_select = instance.$('#env-select');
    if (non_empty_fields.length === 0) {
        env_select.removeProp("disabled");
    }
    else {
        env_select.prop("disabled", true);
        $(env_select).find("option:selected").prop("selected", false);
    }
  },
  'submit .sm-item-form': function(event, instance) {
    event.preventDefault(); 

    let _id = instance.state.get('id');
    let env = instance.$('.sm-input-env')[0].value;
    let isEnvEmpty = isEmpty(env);
    let environmentType = instance.$('.sm-input-environment-type')[0].value;
    let distribution = instance.$('.sm-input-distribution')[0].value;
    let distributionVersion = instance.$('.sm-input-distribution-version')[0].value;
    let mechanismDrivers = instance.$('.sm-input-mechanism-drivers')[0].value;
    let typeDrivers = instance.$('.sm-input-type-drivers')[0].value;
    let focalPointType = instance.$('.sm-input-focal-point-type')[0].value;
    let linkTypes = R.path(['link_types'], instance.state.get('model'));
    let name = instance.$('.sm-input-name')[0].value;
    let useImplicitLinks = instance.$('.sm-input-use-implicit-links')[0].checked;

    submitItem(instance,
      _id,
      env, 
      focalPointType,
      isEnvEmpty ? environmentType: undefined,
      isEnvEmpty ? distribution : undefined,
      isEnvEmpty ? distributionVersion : undefined,
      isEnvEmpty ? mechanismDrivers : undefined,
      isEnvEmpty ? typeDrivers : undefined,
      linkTypes,
      name,
      useImplicitLinks
    );
  }
});
   
/*  
 * Helpers
 */

function isFieldDisabled() {
  let instance = Template.instance();
  let action = instance.state.get('action');
  return R.contains(action, ['view', 'remove']);
}

Template.CliqueType.helpers({    
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

  environmentTypesList: function () {
    return Constants.getByName('environment_types');
  },

  distributionsList: function (env_type) {
    return EnvironmentOptions.getDistributionsByEnvType(env_type);
  },

  distributionVersionsList: function (distribution) {
    return EnvironmentOptions.getOptions(distribution, 'distribution_versions');
  },

  mechanismDriversList: function (distribution) {
    return EnvironmentOptions.getOptions(distribution, 'mechanism_drivers');
  },

  typeDriversList: function (distribution) {
    return EnvironmentOptions.getOptions(distribution, 'type_drivers');
  },

  linkTypesList: function () {
    return LinkTypes.find({});
  },

  envsList: function () {
    return Environments.find({});
  },

  getAttrDisabled: function () {
    return {'disabled': isFieldDisabled()};
  },

  getConfDisabled: function (env_name) {
    return {'disabled': isFieldDisabled() || !isEmpty(env_name)};
  },

  getEnvDisabled: function (env_name) {
    if (isFieldDisabled()) {
      return {'disabled': true};
    }
    let model = Template.instance().state.get('model');
    let conf_empty = (R.all(isEmpty)([model.environment_type, model.distribution,
                                      model.distribution_version,
                                      model.mechanism_drivers, model.type_drivers]));
    return {'disabled': !conf_empty};
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

  argsLinkTypesInput: function (linkTypesList, chosenLinkTypes) {
    let instance = Template.instance();

    let options = R.map((linkType) => { 
      return { value: linkType.type, label: linkType.type }; 
    }, linkTypesList);

    let product = R.map((linkTypeVal) => {
      return { value: linkTypeVal, label: linkTypeVal }; 
    }, chosenLinkTypes);

    return {
      choices: options,
      product: product,
      onProductChange: function (product) {
        let model = instance.state.get('model');
        let link_types = R.map(R.prop('value'), product);
        model = R.assoc('link_types', link_types, model);
        instance.state.set('model', model);
      },
    };
  },

  exists: function (val) {
    return ! R.isNil(val);
  }
}); // end: helpers

function initInsertView(instance, query) {
  instance.state.set('action', query.action);
  instance.state.set('env', query.env);
  instance.state.set('model', CliqueTypes.schema.clean({
    environment: instance.state.get('env')
  }));

  subscribeToOptionsData(instance);
  //instance.subscribe('link_types?env', query.env);
}

function initViewView(instance, query) {
  let reqId = parseReqId(query.id);

  instance.state.set('action', query.action);
  instance.state.set('env', query.env);
  instance.state.set('id', reqId);

  subscribeToOptionsData(instance);
  instance.subscribe('clique_types?_id', reqId.id);

  CliqueTypes.find({ _id: reqId.id }).forEach((model) => {
    instance.state.set('model', model);
  }); 

}

function initUpdateView(instance, query) {
  let reqId = parseReqId(query.id);

  instance.state.set('action', query.action);
  instance.state.set('env', query.env);
  instance.state.set('id', reqId);

  subscribeToOptionsData(instance);
  instance.subscribe('clique_types?env*');
  instance.subscribe('clique_types?_id', reqId.id);

  CliqueTypes.find({ _id: reqId.id }).forEach((model) => {
    instance.state.set('model', model);
  }); 
}

function initRemoveView(instance, query) {
  initViewView(instance, query);
}

function subscribeToOptionsData(instance) {
  instance.subscribe('constants');
  instance.subscribe('environment_options');
  instance.subscribe('environment_options?environment_type*');
  instance.subscribe('environment_options?distributions*');
  instance.subscribe('environments_config');
  instance.subscribe('link_types');
}

function submitItem(
  instance, 
  id, 
  env, 
  focal_point_type,
  environment_type,
  distribution,
  distribution_version,
  mechanism_drivers,
  type_drivers,
  link_types, 
  name,
  use_implicit_links
) {

  let action = instance.state.get('action');

  instance.state.set('isError', false);
  instance.state.set('isSuccess', false);
  instance.state.set('isMessage', false);
  instance.state.set('message', null);

  switch (action) {
  case 'insert':
    insert.call({
      environment: env,
      focal_point_type: focal_point_type,
      environment_type: environment_type,
      distribution: distribution,
      distribution_version: distribution_version,
      mechanism_drivers: mechanism_drivers,
      type_drivers: type_drivers,
      link_types: link_types,
      name: name,
      use_implicit_links: use_implicit_links
    }, processActionResult.bind(null, instance));
    break;

  case 'update': 
    update.call({
      _id: id.id,
      environment: env,
      focal_point_type: focal_point_type,
      environment_type: environment_type,
      distribution: distribution,
      distribution_version: distribution_version,
      mechanism_drivers: mechanism_drivers,
      type_drivers: type_drivers,
      link_types: link_types,
      name: name,
      use_implicit_links: use_implicit_links
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

  Router.go('/clique-types-list');
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
