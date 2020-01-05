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
 * Template Component: EnvironmentDashboard 
 */

//import { Meteor } from 'meteor/meteor'; 
import * as R from 'ramda';
import * as _ from 'lodash';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { remove } from '/imports/api/environments/methods';
import { Icon } from '/imports/lib/icon';
import { store } from '/imports/ui/store/store';
import { Environments } from '/imports/api/environments/environments';
import { Inventory } from '/imports/api/inventories/inventories';
import { calcIconForMessageLevel, lastMessageTimestamp, calcColorClassForMessagesInfoBox }
  from '/imports/api/messages/messages';
import { Counts } from 'meteor/tmeasday:publish-counts';
import { Roles } from 'meteor/alanning:roles';
//import { idToStr } from '/imports/lib/utilities';
import { UserSettings } from '/imports/api/user-settings/user-settings';
import { Counter } from 'meteor/natestrauser:publish-performant-counts';

//import '/imports/ui/components/data-cubic/data-cubic';
import '/imports/ui/components/data-cube/data-cube';
import '/imports/ui/components/icon/icon';
import '/imports/ui/components/list-info-box/list-info-box';
import './environment-dashboard.html';
import '/imports/ui/components/messages-info-box/messages-info-box';
import '/imports/ui/components/messages-modal/messages-modal';
import '/imports/ui/components/alarm-icons/alarm-icons';
import '/imports/ui/components/list-details-box/list-details-box';

/*  
 * Lifecycles
 */

Template.EnvironmentDashboard.onCreated(function () {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    _id: null,
    envName: null,
    allowEdit: false,
    msgsViewBackDelta: 1,
  });

  instance.autorun(function () {
    let data = Template.currentData();
    new SimpleSchema({
      _id: { type: { _str: { type: String, regEx: SimpleSchema.RegEx.Id } } },
      onNodeSelected: { type: Function },
    }).validate(data);

    instance.state.set('_id', data._id);
  });

  instance.autorun(function () {
    let _id = instance.state.get('_id');

    instance.subscribe('environments?_id', _id);
    Environments.find({ _id: _id }).forEach((env) => {
      instance.state.set('envName', env.name);
      instance.state.set('envType', env.environment_type);
      instance.state.set('envDist', env.distribution);
      instance.state.set('infoLastScanning', env.last_scanned);

      let allowEdit = false;
      let auth = R.path(['auth', 'edit-env'], env);
      if (auth && R.contains(Meteor.userId(), auth)) {
        allowEdit = true;
      }
      if (Roles.userIsInRole(Meteor.userId(), 'edit-env', 'default-group')) {
        allowEdit = true;
      }

      instance.state.set('allowEdit', allowEdit);

      subscribe(instance, env);

      /*
      instance.subscribe('messages/count?level&env', 'info', env.name);
      instance.subscribe('messages/count?level&env', 'warning', env.name);
      instance.subscribe('messages/count?level&env', 'error', env.name);
      */

      setDataSources(instance, env);
    });

  });

  instance.autorun(function () {
    instance.subscribe('user_settings?user');
    UserSettings.find({ user_id: Meteor.userId() }).forEach((userSettings) => {
      instance.state.set('msgsViewBackDelta', userSettings.messages_view_backward_delta);
    });
  });

  instance.autorun(function () {
    let msgsViewBackDelta = instance.state.get('msgsViewBackDelta');
    let env = instance.state.get('envName');

    instance.subscribe('messages/count?backDelta&level&env', msgsViewBackDelta, 'info', env);
    instance.subscribe('messages/count?backDelta&level&env', msgsViewBackDelta, 'warning', env);
    instance.subscribe('messages/count?backDelta&level&env', msgsViewBackDelta, 'error', env);
  });
});

/*
Template.EnvironmentDashboard.rendered = function() {
};  
*/

/*
 * Events
 */

Template.EnvironmentDashboard.events({
  'click .sm-edit-button': function (event, instance) {
    let envName = instance.state.get('envName');
    let allowEdit = instance.state.get('allowEdit');
    if (!allowEdit) { return; }

    Router.go('/wizard/' + envName, {}, {});
  },

  'click .sm-scan-button': function (event, instance) {
    let envName = instance.state.get('envName');

    Router.go('new-scanning', {}, { query: { env: envName } });
  },

  'click .sm-delete-button': function (event, instance) {
    let allowEdit = instance.state.get('allowEdit');
    if (!allowEdit) { return; }

    let $deleteModal = instance.$('#env-delete-modal');
    $deleteModal.modal({ show: true });
  }
});

/*  
 * Helpers
 */

function getInfoBox(listName, icon) {
  return {
      header: ['components', 'environment', 'newListInfoBoxes', listName, 'header'],
      baseType: ['components', 'environment', 'newListInfoBoxes', listName, 'baseType'],
      listName: listName,
      listItemFormat: {
          getLabelFn: (item) => { return item.name; },
          getValueFn: (item) => { return item._id._str; },
      },
      icon: icon,
  }
}

Template.EnvironmentDashboard.helpers({
  getState: function (key) {
    let instance = Template.instance();
    return instance.state.get(key);
  },

  getListInfoBoxes: function (env_type) {
    if (env_type === 'OpenStack') {
      return [
        getInfoBox('regions', { type: 'material', name: 'public' }),
        getInfoBox('projects', { type: 'material', name: 'folder' })
      ]
    }
    else if (env_type === 'Kubernetes') {
      return [
        getInfoBox('networks', { type: 'material', name: 'public' }),
        getInfoBox('hosts', { type: 'material', name: 'folder' }),
        getInfoBox('namespaces', { type: 'material', name: 'public' }),
      ]
    }
    return [];
  },

  getBriefInfoList: function (env_type) {
    let briefInfoList = [{
      header: ['components', 'environment', 'newBriefInfos', 'hostsNum', 'header'],
      dataSource: 'infoHostsCount',
      icon: new Icon({ type: 'fa', name: 'server' }),
    }, {
      header: ['components', 'environment', 'newBriefInfos', 'vConnectorsNum', 'header'],
      dataSource: 'infoVConnectorsCount',
      icon: new Icon({ type: 'fa', name: 'compress' }),
    },
      //{
      //     header: ['components', 'environment', 'newBriefInfos', 'lastScanning', 'header'],
      //     dataSource: 'infoLastScanning',
      //     icon: new Icon({ type: 'fa', name: 'search' }),
      // }
    ];

    if (R.isEmpty(env_type)
      || R.isNil(env_type)
      || env_type === 'OpenStack') {
      briefInfoList.unshift({
        header: ['components', 'environment', 'newBriefInfos', 'instancesNum', 'header'],
        dataSource: 'infoInstancesCount',
        icon: new Icon({ type: 'fa', name: 'desktop' }),
      }, {
          header: ['components', 'environment', 'newBriefInfos', 'vServicesNum', 'header'],
          dataSource: 'infoVServicesCount',
          icon: new Icon({ type: 'fa', name: 'object-group' }),
        });
    }
    else if (env_type === 'Kubernetes') {
      briefInfoList.unshift({
        header: ['components', 'environment', 'newBriefInfos', 'containersNum', 'header'],
        dataSource: 'infoContainersCount',
        icon: new Icon({ type: 'local', name: 'container.png' }),
      }, {
          header: ['components', 'environment', 'newBriefInfos', 'podsNum', 'header'],
          dataSource: 'infoPodsCount',
          icon: new Icon({ type: 'fa', name: 'empire', }),
        });
    }

    return briefInfoList;
  },

  infoMessagesCount: function () {
    let instance = Template.instance();
    let envName = instance.state.get('envName');
    if (R.isNil(envName)) { return; }

    return Counts.get('messages?env+level!counter?env=' +
      envName + '&level=' + 'info');
  },

  warningsCount: function () {
    let instance = Template.instance();
    let envName = instance.state.get('envName');
    if (R.isNil(envName)) { return; }

    return Counts.get('messages?env+level!counter?env=' +
      envName + '&level=' + 'warn');
  },

  errorsCount: function () {
    let instance = Template.instance();
    let envName = instance.state.get('envName');
    if (R.isNil(envName)) { return; }

    return Counts.get('messages?env+level!counter?env=' +
      envName + '&level=' + 'error');
  },

  argsEnvDeleteModal: function () {
    let instance = Template.instance();
    return {
      onDeleteReq: function () {
        instance.$('#env-delete-modal').modal('hide');
        let _id = instance.state.get('_id');
        remove.call({ _id: _id }, function (error, _res) {
          if (R.isNil(error)) {
            setTimeout(() => {
              Router.go('/dashboard');
            }, 700);
          } else {
            alert('error removing environment. ' + error.message);
          }
        });
        console.log('delete req performed');
      }
    };
  },

  argsBriefInfo: function (briefInfo) {
    let instance = Template.instance();

    let info = R.when(R.isNil, R.always(0))(instance.state.get(briefInfo.dataSource));
    let briefObj = {
      header: R.path(briefInfo.header, store.getState().api.i18n),
      dataInfo: R.toString(info),
      icon: new Icon(briefInfo.icon)
    };

    return briefObj;
  },

  argsListInfoBox: function (listInfoBox) {
    
    let instance = Template.instance();
    let data = Template.currentData();
    let envName = instance.state.get('envName');

    //let lastScanned = calcLastScanned(listInfoBox.listName, envName);

    return {
      header: R.path(listInfoBox.header, store.getState().api.i18n),
      baseType: R.path(listInfoBox.baseType, store.getState().api.i18n),
      list: getList(listInfoBox.listName, envName),
      icon: new Icon(listInfoBox.icon),
      listItemFormat: listInfoBox.listItemFormat,
      //lastScanning: lastScanned,      
      onItemSelected: function (itemKey) {
        data.onNodeSelected(new Mongo.ObjectID(itemKey));
      }
    };
  },

  notAllowEdit: function () {
    let instance = Template.instance();
    let allowEdit = instance.state.get('allowEdit');
    return !allowEdit;
  },

  getListMessagesInfoBox: function () {
    return [
      {
        level: 'info'
      },
      {
        level: 'warning'
      },
      {
        level: 'error'
      },
    ];
  },

  argsMessagesInfoBox: function (boxDef, env) {
    let instance = Template.instance();
    let envName = instance.state.get('envName');
    let msgsViewBackDelta = instance.state.get('msgsViewBackDelta');

    if (R.isNil(envName)) {
      return {
        title: '', count: 0, lastScanTimestamp: '', onMoreDetailsReq: function () { }
      };
    }

    //let counterName = `messages/count?level=${boxDef.level}&env=${envName}`;
    let counterName = `messages/count?backDelta=${msgsViewBackDelta}&level=${boxDef.level}&env=${envName}`;
    let count = Counter.get(counterName);

    //let count =  Counts.get('messages?env+level!counter?env=' +
    //   envName + '&level=' + boxDef.level);

    let title = _.capitalize(boxDef.level);

    return {
      title: title,
      count: count,
      lastScanTimestamp: lastMessageTimestamp(boxDef.level, env),
      icon: calcIconForMessageLevel(boxDef.level),
      colorClass: calcColorClassForMessagesInfoBox(boxDef.level),
      onMoreDetailsReq: function () {
        $('#messagesModalGlobal').modal('show', {
          dataset: {
            messageLevel: boxDef.level,
            envName: env,
          }
        });
      }
    };
  },

  argsAlarmIcons: function () {
    let instance = Template.instance();
    let envName = instance.state.get('envName');

    if (!R.isNil(envName)) {
      return {
        envName: envName
      };
    }
  }
}); // end: helpers


let listTypes = {
  'regions': 'region',
  'projects': 'project',
  'networks': 'network',
  'hosts': 'host',
  'namespaces': 'namespace',
};

function getList(listName, envName) {
    let type = listTypes[listName];
    if (!type) {
      throw new Error('Unknown list type');
    }
    return Inventory.find({
      environment: envName,
      type: type
    });
}

function subscribe(instance, env) {
  let subscriptions = ['host', 'vconnector'];
  if (R.isEmpty(env.environment_type)
    || R.isNil(env.environment_type)
    || env.environment_type === 'OpenStack') {
    subscriptions.push('instance', 'vservice', 'project', 'region');
  }
  else if (env.environment_type === 'Kubernetes') {
    subscriptions.push('container', 'pod', 'network', 'namespace');
  }

  for (let i = 0; i < subscriptions.length; i++) {
    instance.subscribe('inventory?env+type', env.name, subscriptions[i]);
  }
}

function setDataSources(instance, env) {
  let dataSources = [
    { object: 'vconnector', variableName: 'infoVConnectorsCount' },
    { object: 'host', variableName: 'infoHostsCount' },
    { object: 'project', variableName: 'projectsCount' },
    { object: 'region', variableName: 'regionsCount' },
  ];
  if (R.isEmpty(env.environment_type)
    || R.isNil(env.environment_type)
    || env.environment_type === 'OpenStack') {
    dataSources.push(
      { object: 'instance', variableName: 'infoInstancesCount' },
      { object: 'vservice', variableName: 'infoVServicesCount' }
    );
  }
  else if (env.environment_type === 'Kubernetes') {
    dataSources.push(
      { object: 'container', variableName: 'infoContainersCount' },
      { object: 'pod', variableName: 'infoPodsCount' }
    );
  }

  for (let i = 0; i < dataSources.length; i++) {
    let counterName = 'inventory?env+type!counter?env=' + env.name +
      '&type=' + dataSources[i].object;
    let objectsCount = Counts.get(counterName);
    instance.state.set(dataSources[i].variableName, objectsCount);
  }
}

/*
function calcLastScanned(listName, envName) {
  switch (listName) {
  case 'regions':
    return R.path(['last_scanned'], Inventory.findOne({
      environment: envName, 
      type:'region'
    }));

  case 'projects':
    return R.path(['last_scanned'], Inventory.findOne({
      environment: envName, 
      type:'project'
    }));

  default:
    throw 'unknown';
  }
}
*/
