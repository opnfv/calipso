/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
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
import { Counter } from 'meteor/natestrauser:publish-performant-counts';
//import { Messages } from '/imports/api/messages/messages';
import { store } from '/imports/ui/store/store';
import { setMainAppSelectedEnvironment } from '/imports/ui/actions/main-app.actions';

import '/imports/ui/components/messages-info-box/messages-info-box';
import '/imports/ui/components/environment-box/environment-box';

import './dashboard.html';     

/*
 * Lifecycle methods
 */

Template.Dashboard.onCreated(function () {
  var instance = this;

  instance.autorun(function () {
    instance.subscribe('environments_config');

    instance.subscribe('messages/count?level', 'info');
    instance.subscribe('messages/count?level', 'warning');
    instance.subscribe('messages/count?level', 'error');

    Environments.find({}).forEach(function (envItem) {
      instance.subscribe('inventory?env+type', envItem.name, 'instance');
      instance.subscribe('inventory?env+type', envItem.name, 'vservice');
      instance.subscribe('inventory?env+type', envItem.name, 'host');
      instance.subscribe('inventory?env+type', envItem.name, 'vconnector');
      instance.subscribe('inventory?env+type', envItem.name, 'project');
      instance.subscribe('inventory?env+type', envItem.name, 'region');
    });

    store.dispatch(setMainAppSelectedEnvironment(null));
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

  regoinsCount: function (envName){
    //return Inventory.find({environment: envName, type:'region'}).count();
    return Counts.get('inventory?env+type!counter?env=' +
      envName + '&type=' + 'region');
  },

  regoins: function (envName) {
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

  messageCount: function (level) {
    return Counter.get(`messages/count?level=${level}`);
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

  argsEnvBox: function (
    environmentName,
    regionsCount, 
    regions, 
    projectsCount, 
    projects, 
    instancesCount,
    vservicesCount,
    vconnectorsCount,
    hostsCount
  ) {

    return {
      environmentName: environmentName,
      regionsCount: regionsCount,
      regions: regions,
      projectsCount,
      projects: projects,
      instancesCount: instancesCount,
      vservicesCount: vservicesCount,
      vconnectorsCount: vconnectorsCount,
      hostsCount: hostsCount,
    };
  }
}); // end: helpers
