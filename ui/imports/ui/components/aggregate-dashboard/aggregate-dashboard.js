/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: AggregateDashboard 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { Inventory } from '/imports/api/inventories/inventories';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { regexEscape } from '/imports/lib/regex-utils';
import * as R from 'ramda';
import { store } from '/imports/ui/store/store';
import { Icon } from '/imports/lib/icon';
        
//import '/imports/ui/components/accordionNavMenu/accordionNavMenu';
import '/imports/ui/components/data-cubic/data-cubic';
import '/imports/ui/components/list-info-box/list-info-box';

import './aggregate-dashboard.html';     
    
let infoBoxes = [{
  header: ['components', 'aggregateDashboard', 'infoBoxes', 'instances', 'header'],
  dataSource: 'instancesCount',
  icon: { type: 'fa', name: 'desktop' },
  theme: 'dark'
}, {
  header: ['components', 'aggregateDashboard', 'infoBoxes', 'vServices', 'header'],
  dataSource: 'vServicesCount',
  icon: { type: 'fa', name: 'object-group' },
  theme: 'dark'
}, {
  header: ['components', 'aggregateDashboard', 'infoBoxes', 'hosts', 'header'],
  dataSource: 'hostsCount',
  icon: { type: 'fa', name: 'server' },
  theme: 'dark'
}, {
  header: ['components', 'aggregateDashboard', 'infoBoxes', 'vConnectors', 'header'],
  dataSource: 'vConnectorsCount',
  icon: { type: 'fa', name: 'compress' },
  theme: 'dark'
}, {
  header: ['components', 'aggregateDashboard', 'infoBoxes', 'vEdges', 'header'],
  dataSource: 'vEdgesCount',
  icon: { type: 'fa', name: 'external-link' },
  theme: 'dark'
}]; 

let listInfoBoxes = [{
  header: ['components', 'aggregateDashboard', 'listInfoBoxes', 'hosts', 'header'],
  listName: 'hosts',
  listItemFormat: { label: 'name', value: 'id_path' },
  icon: { type: 'material', name: 'developer_board' },
}];

/*  
 * Lifecycles
 */   
  
Template.AggregateDashboard.onCreated(function() {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    _id: null,
    id_path: null,
    instancesCount: 0,
    vServicesCount: 0,
    hostsCount: 0,
    vConnectors: 0,
    vEdges: 0,
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

    instance.subscribe('inventory?_id', _id);
    Inventory.find({ _id: _id }).forEach((aggr) => {
      instance.state.set('id_path', aggr.id_path);

      instance.subscribe('inventory?id_path', aggr.id_path);
      instance.subscribe('inventory?id_path_start&type', aggr.id_path, 'instance');
      instance.subscribe('inventory?id_path_start&type', aggr.id_path, 'vservice');
      instance.subscribe('inventory?id_path_start&type', aggr.id_path, 'host');
      instance.subscribe('inventory?id_path_start&type', aggr.id_path, 'vconnector');
      instance.subscribe('inventory?id_path_start&type', aggr.id_path, 'vedge');

      let idPathExp = new RegExp(`^${regexEscape(aggr.id_path)}`);

      instance.state.set('instancesCount', Inventory.find({ 
        id_path: idPathExp,
        type: 'instance'
      }).count());

      instance.state.set('vServicesCount', Inventory.find({ 
        id_path: idPathExp,
        type: 'vservice'
      }).count());

      instance.state.set('hostsCount', Inventory.find({ 
        id_path: idPathExp,
        type: 'host'
      }).count());

      instance.state.set('vConnectorsCount', Inventory.find({ 
        id_path: idPathExp,
        type: 'vconnector'
      }).count());

      instance.state.set('vEdgesCount', Inventory.find({ 
        id_path: idPathExp,
        type: 'vedge'
      }).count());
    });
  });
});  

/*
Template.AggregateDashboard.rendered = function() {
};  
*/

/*
 * Events
 */

Template.AggregateDashboard.events({
});
   
/*  
 * Helpers
 */

Template.AggregateDashboard.helpers({    
  aggregate: function () {
    let instance = Template.instance();
    let aggregate_id_path = instance.state.get('id_path');

    return Inventory.findOne({ id_path: aggregate_id_path });
  },

  infoBoxes: function () {
    return infoBoxes;
  },

  listInfoBoxes: function () {
    return listInfoBoxes;
  },

  argsInfoBox: function (infoBox) {
    let instance = Template.instance();

    return {
      header: R.path(infoBox.header, store.getState().api.i18n),
      dataInfo: instance.state.get(infoBox.dataSource).toString(),
      icon: new Icon(infoBox.icon),
      theme: infoBox.theme
    };
  },

  argsListInfoBox: function (listInfoBox) {
    let instance = Template.instance();
    let data = Template.currentData();
    let aggregate_id_path = instance.state.get('id_path');

    return {
      header: R.path(listInfoBox.header, store.getState().api.i18n),
      list: getList(listInfoBox.listName, aggregate_id_path),
      //dataInfo: instance.state.get(infoBox.dataSource).toString(),
      icon: new Icon(listInfoBox.icon),
      //theme: infoBox.theme
      listItemFormat: listInfoBox.listItemFormat,
      onItemSelected: function (itemKey) {
        data.onNodeSelected(new Mongo.ObjectID(itemKey));
      }
    };
  }
});


function getList(listName, parentIdPath) {
  let idPathExp = new RegExp(`^${regexEscape(parentIdPath)}`);

  switch (listName) {
  case 'hosts':
    return Inventory.find({ 
      id_path: idPathExp,
      type: 'host'
    });   

  default:
    throw 'unknowned list type';
  }
}
