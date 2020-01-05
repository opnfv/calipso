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
 * Template Component: Dashboard
 */

//import * as R from 'ramda';
import * as _ from 'lodash';
import { Environments } from '/imports/api/environments/environments';
import { //Messages,
  calcIconForMessageLevel, lastMessageTimestamp, calcColorClassForMessagesInfoBox
} from '/imports/api/messages/messages';
import { Template } from 'meteor/templating';
import { Inventory } from '/imports/api/inventories/inventories';
import { Counts } from 'meteor/tmeasday:publish-counts';
//import { Counter } from 'meteor/natestrauser:publish-performant-counts';
//import { Messages } from '/imports/api/messages/messages';
import { store } from '/imports/ui/store/store';
import { setMainAppSelectedEnvironment } from '/imports/ui/actions/main-app.actions';
import { UserSettings } from '/imports/api/user-settings/user-settings';

import '/imports/ui/components/messages-info-box/messages-info-box';
import '/imports/ui/components/environment-box/environment-box';

import './dashboard.html';

/*
 * Lifecycle methods
 */

Template.Dashboard.onCreated(function () {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    msgsViewBackDelta: 1
  });

  instance.autorun(function () {
    instance.subscribe('environments_config');

    instance.subscribe('messages/count?level', 'info');
    instance.subscribe('messages/count?level', 'warning');
    instance.subscribe('messages/count?level', 'error');

    Environments.find({}).forEach(function (envItem) {
      instance.subscribe('inventory?env+type', envItem.name, 'host');
      instance.subscribe('inventory?env+type', envItem.name, 'vconnector');
      if (envItem.environment_type === 'OpenStack') {
        instance.subscribe('inventory?env+type', envItem.name, 'project');
        instance.subscribe('inventory?env+type', envItem.name, 'region');
        instance.subscribe('inventory?env+type', envItem.name, 'instance');
        instance.subscribe('inventory?env+type', envItem.name, 'vservice');
      }
      else if (envItem.environment_type === 'Kubernetes') {
        instance.subscribe('inventory?env+type', envItem.name, 'network');
        instance.subscribe('inventory?env+type', envItem.name, 'container');
        instance.subscribe('inventory?env+type', envItem.name, 'pod');
        instance.subscribe('inventory?env+type', envItem.name, 'namespace');
      }
    });

    store.dispatch(setMainAppSelectedEnvironment(null));
  });

  instance.autorun(function () {
    instance.subscribe('user_settings?user');
    UserSettings.find({user_id: Meteor.userId()}).forEach((userSettings) => {
      instance.state.set('msgsViewBackDelta', userSettings.messages_view_backward_delta); 
    });
  });

  instance.autorun(function () {
    let msgsViewBackDelta = instance.state.get('msgsViewBackDelta');

    instance.subscribe('messages/count?backDelta&level', msgsViewBackDelta, 'info');
    instance.subscribe('messages/count?backDelta&level', msgsViewBackDelta, 'warning');
    instance.subscribe('messages/count?backDelta&level', msgsViewBackDelta, 'error');
  });
});

Template.Dashboard.rendered = function(){

  /*
  $.getScript('https://www.gstatic.com/charts/loader.js', function() {
    google.charts.load('current', {'packages':['gauge', 'line']});
  google.charts.setOnLoadCallback(drawLine);


  function drawLine() {
      var data = new google.visualization.DataTable();
      data.addColumn('number', 'Traffic Webex');
      data.addColumn('number', 'Traffic metapod');
      data.addColumn('number', 'Some other Traffic');
      data.addColumn('number', 'Some other Traffic');

      data.addRows([
        [1,  37.8, 80.8, 41.8],
        [2,  30.9, 69.5, 32.4],
        [3,  25.4,   57, 25.7],
        [4,  11.7, 18.8, 32.5],
        [5,  11.9, 25.6, 10.4],
        [6,   68.8, 13.6,  27.7],
        [7,   7.6, 42.3,  9.6],
        [8,  12.3, 29.2, 10.6],
        [9,  16.9, 42.9, 14.8]
      ]);

  var options = {
    chart: {
      title: 'Network traffic throughput',
      subtitle: 'in Mbps'
    }
  };

  var chart = new google.charts.Line(document.getElementById('curve_chart'));

  chart.draw(data, options);
  }
  });

  */
};
/*
 * Helpers
 */

Template.Dashboard.helpers({

  envList:function(){
    //return Environments.find({type:'environment'});
    return Environments.find({});
  },

  envObjects: function (env) {
      let envName = env.name;

      let specificFields = {};
      if (env.environment_type === 'OpenStack') {
        specificFields = {
          projects: Inventory.find({environment: envName, type: 'project'}),
          regions: Inventory.find({environment: envName, type: 'region'}),
          instancesCount: Counts.get('inventory?env+type!counter?env=' + envName + '&type=instance'),
          vservicesCount: Counts.get('inventory?env+type!counter?env=' + envName + '&type=vservice'),
        }
      }
      else if (env.environment_type === 'Kubernetes') {
        specificFields = {
          networks: Inventory.find({environment: envName, type: 'network'}),
          hosts: Inventory.find({environment: envName, type: 'host'}),
          namespaces: Inventory.find({environment: envName, type: 'namespace'}),
          containersCount: Counts.get('inventory?env+type!counter?env=' + envName + '&type=container'),
          podsCount: Counts.get('inventory?env+type!counter?env=' + envName + '&type=pod'),
        }
      }

      return {
          ...specificFields,
          ...{
              env: env,
              hostsCount: Counts.get('inventory?env+type!counter?env=' + envName + '&type=host'),
              vconnectorsCount: Counts.get('inventory?env+type!counter?env=' + envName + '&type=vconnector')
          }
      }
  },

  instancesCount: function (envName){
    //return Inventory.find({environment: envName, type:'instance'}).count();
    return Counts.get('inventory?env+type!counter?env=' +
      envName + '&type=' + 'instance');
  },

  vservicesCount: function (envName) {
    //return Inventory.find({environment: envName, type:'vservice'}).count();
    return Counts.get('inventory?env+type!counter?env=' +
      envName + '&type=' + 'vservice');
  },

  hostsCount: function (envName) {
    //return Inventory.find({environment: envName, type:'host'}).count();
    return Counts.get('inventory?env+type!counter?env=' +
      envName + '&type=' + 'host');
  },

  vconnectorsCount: function(envName){
    //return Inventory.find({environment: envName, type:'vconnector'}).count();
    return Counts.get('inventory?env+type!counter?env=' +
      envName + '&type=' + 'vconnector');
  },

  projectsCount: function (envName){
    //return Inventory.find({environment: envName, type:'project'}).count();
    return Counts.get('inventory?env+type!counter?env=' +
      envName + '&type=' + 'project');
  },

  regionsCount: function (envName){
    //return Inventory.find({environment: envName, type:'region'}).count();
    return Counts.get('inventory?env+type!counter?env=' +
      envName + '&type=' + 'region');
  },

  regions: function (envName) {
    return Inventory.find({environment: envName, type:'region'});
  },

  projects: function (envName){
    return Inventory.find({environment: envName, type:'project'});
  },

  notificationsCount: function(){
    //return Messages.find({level:'notify'}).count();
    return Counts.get('messages?level!counter?' +
      'level=' + 'notify');
  },

  warningsCount: function(){
    //return Messages.find({level:'warn'}).count();
    return Counts.get('messages?level!counter?' +
      'level=' + 'warn');
  },

  errorsCount: function(){
    //return Messages.find({level:'error'}).count();
    return Counts.get('messages?level!counter?' +
      'level=' + 'error');
  },
  /*
  notificationsTimestamp: function(){
    var msgTimestamp = Messages.findOne({state:'added'},{fields: {'timestamp': 1} });
    return msgTimestamp.timestamp;
  },
  warnings: function(){
    return Messages.findOne({state:'warn'});
  },
  errors: function(){
    return Messages.findOne({state:'down'});
  },
*/

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

  msgCounterName: function (level) {
    let instance = Template.instance();
    let msgsViewBackDelta = instance.state.get('msgsViewBackDelta');
    let counterName = `messages/count?backDelta=${msgsViewBackDelta}&level=${level}`;

    return counterName;
  },

  argsMessagesInfoBox: function(boxDef, messageCount) {
    //let instance = Template.instance();
    let title = _.capitalize(boxDef.level);

    return {
      title: title,
      count: messageCount,
      lastScanTimestamp: lastMessageTimestamp(boxDef.level),
      icon: calcIconForMessageLevel(boxDef.level),
      colorClass: calcColorClassForMessagesInfoBox(boxDef.level),
      onMoreDetailsReq: function () {
        $('#messagesModalGlobal').modal('show', {
          dataset: {
            messageLevel: boxDef.level,
          }
        });
      }
    };
  },
}); // end: helpers
