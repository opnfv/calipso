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
 */

//import { Meteor } from 'meteor/meteor';
import { Session } from 'meteor/session';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import * as R from 'ramda';
import { ConnectionTests } from '/imports/api/connection-tests/connection-tests';

import { Environments } from '/imports/api/environments/environments';
import { subsNameSupportedEnvs, 
  isMonitoringSupported,
  isListeningSupported,
} from '/imports/api/supported_environments/supported_environments';
import { createNewConfGroup } from '/imports/api/environments/environments';
import { store } from '/imports/ui/store/store';

import './environment-wizard.html';

import '/imports/ui/components/env-main-info/env-main-info';
import '/imports/ui/components/env-os-api-endpoint-info/env-os-api-endpoint-info';
import '/imports/ui/components/env-open-stack-db-credentials-info/env-open-stack-db-credentials-info';
import '/imports/ui/components/env-master-host-credentials-info/env-master-host-credentials-info';
//import '/imports/ui/components/env-nfv-info/env-nfv-info';
import '/imports/ui/components/env-aci-info/env-aci-info';
import '/imports/ui/components/env-amqp-credentials-info/env-amqp-credentials-info';
import '/imports/ui/components/env-monitoring-info/env-monitoring-info';
import '/imports/ui/components/env-kube-info/env-kube-info';

import {
  insert,
  update
} from '/imports/api/environments/methods';

import { insert as insertConnectionTests } from '/imports/api/connection-tests/methods';

/*
 * Lifecycles
 */

Template.EnvironmentWizard.onCreated(function(){
  let instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    environment: null,
    action: 'insert',
    isError: false,
    isSuccess: false,
    isMessage: false,
    message: null,
    disabled: false,
    connectionTestId: null
  });

  instance.autorun(function () {
    let controller = Iron.controller();
    controller.state.set('needsConfirmation', true);
    Session.set('isDirty', false);
    //let params = controller.getParams();

    //let envName = params.env;
    let envName = Session.get('wizardEnv');
    if (envName) {
      instance.subscribe('environments?name', envName);
      instance.state.set('action', 'update');

    } else {
      instance.state.set('action', 'insert');
    }

    instance.subscribe(subsNameSupportedEnvs);

    let action = instance.state.get('action');
    if (action === 'update') {
      Environments.find({'name': envName})
        .forEach(function (envItem) {
          instance.state.set('environmentModel', R.clone(envItem));
        });
    } else if (action === 'insert') {
      instance.state.set('environmentModel', generateNewEnv());
    }
  });

  instance.autorun(function () {
    let connectionTestId = instance.state.get('connectionTestId');
    if (R.isNil(connectionTestId)) { return; }
    
    instance.subscribe('connection_tests?_id', connectionTestId);
    ConnectionTests.find({ _id: connectionTestId }).forEach((connTest) => {
      if (connTest.status !== 'response') { 
        return; 
      }

      R.mapObjIndexed((success, groupName) => {
        if (success) {
          toastr.success(`${groupName} connection succeeded`, { timeOut: 5000 });
        } else {
          toastr.error(`${groupName} connection failed: ${connTest.errors[groupName]}`,
                       { timeOut: 5000 });
        }
      }, connTest.test_results);
    });
  });

  instance.storeUnsubscribe = store.subscribe(() => {
    let i18n = store.getState().api.i18n;
    instance.state.set('i18n', i18n);
  });


  let i18n = store.getState().api.i18n;
  instance.state.set('i18n', i18n);
});

Template.EnvironmentWizard.rendered = function(){

  // todo: refactor to use component - not jquery click
  $('.btnPrevious').click(function(){
    $('.nav-tabs > .active').prev('li').find('a').trigger('click');
  });

};

Template.EnvironmentWizard.onDestroyed(function () {
  let instance = this;
  instance.storeUnsubscribe();
});

/*
 * Helpers
 */

export const environmentSpecificTabs = {
  'OpenStack': ['OpenStack', 'AMQP'],
  'Kubernetes': ['Kubernetes']
};

Template.EnvironmentWizard.helpers({
  model: function () {
    let instance = Template.instance();
    return instance.state.get('environmentModel');
  },

  tabs: function () {
    let instance = Template.instance();

    let environmentModel = instance.state.get('environmentModel');
    let action = instance.state.get('action');
    let disabled = instance.state.get('disabled');
    let activateNextTab = function (tabId) {
      let nextTab = instance.$('#link-' + tabId).closest('li').next();
      if (nextTab.length === 0) {
        nextTab = instance.$(".tab-list").find('li').first();
      }
      nextTab.find('.sm-tab-link').tab('show');
    };

    if (R.isNil(environmentModel)) {
      return [];
    }

    let isMonSupportedRes = isMonitoringSupported(
      environmentModel.distribution, 
      environmentModel.distribution_version, 
      environmentModel.type_drivers,
      environmentModel.mechanism_drivers
    );

    let isMonitoringDisabled = disabled || !isMonSupportedRes;


    let monitoringDisabledMessage = null;
    if (isMonitoringDisabled && !isMonSupportedRes) {
      monitoringDisabledMessage = 'Distribution, type drivers and mechanism driver are not supported at this moment';
    }
    
    let isListeningSupportedRes = isListeningSupported(
      environmentModel.distribution, 
      environmentModel.distribution_version, 
      environmentModel.type_drivers,
      environmentModel.mechanism_drivers
    );
    let isListeningDisabled = disabled || !isListeningSupportedRes;

    let monitoringTabDisabled = !(environmentModel.enable_monitoring && isMonSupportedRes);
    let isAciTabDisabled = !(environmentModel.aci_enabled);

    let envType = environmentModel.environment_type;
    let envSpecificTabs = environmentSpecificTabs[(envType in environmentSpecificTabs)
                                                  ? envType
                                                  : "OpenStack"];
    let osTabDisabled = !(envSpecificTabs.includes("OpenStack"));
    let amqpTabDisabled = !(envSpecificTabs.includes("AMQP")
                            && environmentModel.listen
                            && isListeningSupportedRes);
    let kubeTabDisabled = !(envSpecificTabs.includes("Kubernetes"));

    return [{
      label: 'Main Info',
      localLink: 'maininfo',
      defaultTab: true,
      disabled: false,
      templateName: 'EnvMainInfo',
      templateData: {
        model: environmentModel, 
        disabled: disabled,
        isListeningDisabled: isListeningDisabled,
        isMonitoringDisabled: isMonitoringDisabled,
        isKubeDisabled: kubeTabDisabled,
        setModel: function (newModel) {
          Session.set('isDirty', true);

          if (newModel.aci_enabled) {
            let monitoringGroup = getGroupInArray('Monitoring', newModel.configuration);
            newModel = setConfigurationGroup('Monitoring', monitoringGroup, newModel);
          } else {
            newModel = removeConfigurationGroup('Monitoring', newModel);
          }

          if (newModel.enable_monitoring) {
            let monitoringGroup = getGroupInArray('ACI', newModel.configuration);
            newModel = setConfigurationGroup('ACI', monitoringGroup, newModel);
          } else {
            newModel = removeConfigurationGroup('ACI', newModel);
          }

          if (newModel.listen) {
            let monitoringGroup = getGroupInArray('AMQP', newModel.configuration);
            newModel = setConfigurationGroup('AMQP', monitoringGroup, newModel);
          } else {
            newModel = removeConfigurationGroup('AMQP', newModel);
          }

          instance.state.set('environmentModel', newModel);
        },
        onNextRequested: activateNextTab.bind(null, 'maininfo'),
        action: action,
      }
    }, {
      label: 'OS API Endpoint',
      localLink: 'endpoint-panel',
      disabled: osTabDisabled,
      templateName: 'EnvOsApiEndpointInfo',
      templateData: {
        model: getGroupInArray('OpenStack', environmentModel.configuration),
        disabled: osTabDisabled,
        setModel: function (newSubModel) {
          Session.set('isDirty', true);
          let model = instance.state.get('environmentModel');
          let newModel = setConfigurationGroup('OpenStack', newSubModel, model);
          instance.state.set('environmentModel', newModel);
        },
        onNextRequested: activateNextTab.bind(null, 'endpoint-panel'),
        action: action,
        onTestConnection: function () {
          testConnection(instance);
        },
      }
    }, {
      label: 'OS DB Credentials',
      localLink: 'db-credentials',
      disabled: osTabDisabled,
      templateName: 'EnvOpenStackDbCredentialsInfo',
      templateData: {
        model: getGroupInArray('mysql', environmentModel.configuration),
        disabled: osTabDisabled,
        setModel: function (newSubModel) {
          Session.set('isDirty', true);
          let model = instance.state.get('environmentModel');
          let newModel = setConfigurationGroup('mysql', newSubModel, model);
          instance.state.set('environmentModel', newModel);
        },
        onNextRequested: activateNextTab.bind(null, 'db-credentials'),
        action: action,
        onTestConnection: function () {
          testConnection(instance);
        },
      }
    }, {
      label: 'Master Host Credentials',
      localLink: 'master-host',
      disabled: false,
      templateName: 'EnvMasterHostCredentialsInfo',
      templateData: {
        model: getGroupInArray('CLI', environmentModel.configuration),
        disabled: disabled,
        setModel: function (newSubModel) {
          Session.set('isDirty', true);
          let model = instance.state.get('environmentModel');
          let newModel = setConfigurationGroup('CLI', newSubModel, model);
          instance.state.set('environmentModel', newModel);
        },
        onNextRequested: activateNextTab.bind(null, 'master-host'),
        action: action,
        onTestConnection: function () {
          testConnection(instance);
        },
      }
    }, {
      label: 'AMQP Credentials',
      localLink: 'amqp',
      disabled: amqpTabDisabled,
      templateName: 'EnvAmqpCredentialsInfo',
      templateData: {
        model: getGroupInArray('AMQP', environmentModel.configuration),
        disabled: amqpTabDisabled,
        setModel: function (newSubModel) {
          Session.set('isDirty', true);
          let model = instance.state.get('environmentModel');
          let newModel = setConfigurationGroup('AMQP', newSubModel, model);
          instance.state.set('environmentModel', newModel);
        },
        onNextRequested: activateNextTab.bind(null, 'amqp'),
        action: action,
        onTestConnection: function () {
          testConnection(instance);
        },
      }
    }, 
    /*  {
      label: 'NFV Credentials',
      localLink: 'nfv',
      disabled: false,
      templateName: 'EnvNfvInfo',
      templateData: {
        model: getGroupInArray('NFV_provider', environmentModel.configuration),
        disabled: disabled,
        setModel: function (newSubModel) {
          Session.set('isDirty', true);
          let model = instance.state.get('environmentModel');
          let newModel = setConfigurationGroup('NFV_provider', newSubModel, model);
          instance.state.set('environmentModel', newModel);
        },
        onNextRequested: activateNextTab.bind(null, 'monitoringInfo'),
        action: action,
      }
    }, */
    {
      label: 'ACI Credentials',
      localLink: 'aci',
      disabled: isAciTabDisabled,
      templateName: 'EnvAciInfo',
      templateData: {
        model: getGroupInArray('ACI', environmentModel.configuration),
        disabled: isAciTabDisabled,
        setModel: function (newSubModel) {
          Session.set('isDirty', true);
          let model = instance.state.get('environmentModel');
          let newModel = setConfigurationGroup('ACI', newSubModel, model);
          instance.state.set('environmentModel', newModel);
        },
        onNextRequested: activateNextTab.bind(null, 'aci'),
        action: action,
        onTestConnection: function () {
          testConnection(instance);
        },
      }
    }, {
      label: 'Monitoring',
      localLink: 'monitoringInfo',
      disabled: monitoringTabDisabled,
      templateName: 'EnvMonitoringInfo',
      templateData: {
        model: getGroupInArray('Monitoring', environmentModel.configuration),
        disabled: isMonitoringDisabled,
        disabledMessage: monitoringDisabledMessage,
        setModel: function (newSubModel) {
          Session.set('isDirty', true);
          let model = instance.state.get('environmentModel');
          let newModel = setConfigurationGroup('Monitoring', newSubModel, model);
          instance.state.set('environmentModel', newModel);
        },
        onNextRequested: activateNextTab.bind(null, 'monitoringInfo'),
        action: action,
        onTestConnection: function () {
          testConnection(instance);
        },
      }
    }, {
      label: 'Kubernetes',
      localLink: 'kubeInfo',
      disabled: kubeTabDisabled,
      templateName: 'EnvKubeInfo',
      templateData: {
        model: getGroupInArray('Kubernetes', environmentModel.configuration),
        disabled: kubeTabDisabled,
        disabledMessage: "Kubernetes tab is enabled only for environments of type 'Kubernetes'",
        setModel: function (newSubModel) {
          Session.set('isDirty', true);
          let model = instance.state.get('environmentModel');
          let newModel = setConfigurationGroup('Kubernetes', newSubModel, model);
          instance.state.set('environmentModel', newModel);
        },
        onNextRequested: activateNextTab.bind(null, 'kubeInfo'),
        action: action,
        onTestConnection: function () {
          testConnection(instance);
        },
      }
    }];
  },

  isDefaultTab: function (tab) {
    return tab.defaultTab;
  },

  environment: function () {
    let instance = Template.instance();
    return instance.state.get('environment');
  },

  getConfSection: function(sectionName, environment) {
    if (R.isNil(environment)) { return null; }
    let section = R.find(R.propEq('name', sectionName),
      environment.configuration);
    return section;
  },

  getState: function (key) {
    let instance = Template.instance();
    return instance.state.get(key); 
  },
});

/*
 * Events
 */

Template.EnvironmentWizard.events({
  /*
  'click .toast' : function () {
    toastr.success('Have fun storming the castle!', 'Open Stack server says');
  },
  */

  // todo: research: seems not implemented
  /*
  'click .fa-trash' : function () {
    Meteor.call('deleteRecipe', this._id);
  },
  */

  'click .sm-submit-button': function () {
    let instance = Template.instance();
    doSubmit(instance);
  },

  'click .sm-tab-link': function (event, _instance) {
    let isDisabled = event.target.dataset.isDisabled; 
    if (isDisabled) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }
  },
});

function generateNewEnv() {
  return Environments.schema.clean({});
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
      let message = error.message;
      if (error.errors) {
        message = R.reduce((acc, errorItem) => {
          return acc + '\n- ' + errorItem.name;
        }, message, error.errors);
      }
      instance.state.set('message', message);
    }

  } else {
    instance.state.set('isError', false);
    instance.state.set('isSuccess', true);
    instance.state.set('isMessage', true);  

    if (action === 'insert') {
      instance.state.set('message', 'Record had been added successfully');
      instance.state.set('disabled', true);
    } else if (action === 'update') {
      instance.state.set('message', 'Record had been updated successfully');
    }

    Session.set('isDirty', false);
  }
}

function processInsertTestConnnectionResult(instance, error, itemId) {
  if (error) {
    instance.state.set('isError', true);
    instance.state.set('isSuccess', false);
    instance.state.set('isMessage', true);  

    if (typeof error === 'string') {
      instance.state.set('message', error);
    } else {
      let message = error.message;
      if (error.errors) {
        message = R.reduce((acc, errorItem) => {
          return acc + '\n- ' + errorItem.name;
        }, message, error.errors);
      }
      instance.state.set('message', message);
    }

    return;
  } 

  instance.state.set('connectionTestId', itemId);

  instance.state.set('isError', false);
  instance.state.set('isSuccess', true);
  instance.state.set('isMessage', true);  

  instance.state.set('message', 'Connection sent to be tested');
}

function getGroupInArray(groupName, array) {
  let group = R.find(R.propEq('name', groupName), array);
  return group ? group : createNewConfGroup(groupName);
}

function removeGroupInArray(groupName, array) {
  return R.reject(R.propEq('name', groupName), array);
}

function setConfigurationGroup(groupName, group, model) {
  let tempConfiguration = removeGroupInArray(groupName, model.configuration);
  let newConfiguration = R.append(group, tempConfiguration);
  let newModel = R.assoc('configuration', newConfiguration, model);
  return newModel;
}

function removeConfigurationGroup(groupName, model) {
  let newConfiguration = removeGroupInArray(groupName, model.configuration);
  let newModel = R.assoc('configuration', newConfiguration, model);
  return newModel;
}

function doSubmit(instance) {
  let action = instance.state.get('action');
  let environment = instance.state.get(
    'environmentModel');

  instance.state.set('isError', false);  
  instance.state.set('isSuccess', false);  
  instance.state.set('isMessage', false);  
  instance.state.set('message', null);  

  switch (action) {
  case 'insert':
    insert.call({
      configuration: environment.configuration,
      distribution: environment.distribution,
      distribution_version: environment.distribution_version,
      name: environment.name,
      environment_type: environment.environment_type,
      type_drivers: environment.type_drivers,
      mechanism_drivers: environment.mechanism_drivers,
      listen: environment.listen,
      enable_monitoring: environment.enable_monitoring,
      aci_enabled: environment.aci_enabled,
      app_path:environment.app_path,
    }, processActionResult.bind(null, instance));
    break;

  case 'update':
    update.call({
      _id: environment._id,
      configuration: environment.configuration,
      environment_type: environment.environment_type,
      //distribution: environment.distribution,
      //name: environment.name,
      type_drivers: environment.type_drivers,
      mechanism_drivers: environment.mechanism_drivers,
      listen: environment.listen,
      enable_monitoring: environment.enable_monitoring,
      aci_enabled: environment.aci_enabled,
      app_path:environment.app_path,
    }, processActionResult.bind(null, instance));
    break;

  default:
    // todo
    break;
  }
}

function testConnection(instance) {
  let environmentModel = instance.state.get('environmentModel');
  insertConnectionTests.call({
    environment: environmentModel.name,
    targets_configuration: environmentModel.configuration,
  }, processInsertTestConnnectionResult.bind(null, instance));
}
