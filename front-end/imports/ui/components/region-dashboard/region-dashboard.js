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
 * Template Component: RegionDashboard 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import * as R from 'ramda';
import { Inventory } from '/imports/api/inventories/inventories';
import { store } from '/imports/ui/store/store';
import { Icon } from '/imports/lib/icon';
import { regexEscape } from '/imports/lib/regex-utils';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
//import { setCurrentNode } from '/imports/ui/actions/navigation';

import '/imports/ui/components/accordion-nav-menu/accordion-nav-menu';
import '/imports/ui/components/data-cubic/data-cubic';
import '/imports/ui/components/list-info-box/list-info-box';
        
import './region-dashboard.html';     
    
let infoBoxes = [{
  header: ['components', 'regionDashboard', 'infoBoxes', 'instances', 'header'],
  dataSource: 'instancesCount',
  icon: { type: 'fa', name: 'desktop' },
  theme: 'dark'
}, {
  header: ['components', 'regionDashboard', 'infoBoxes', 'vServices', 'header'],
  dataSource: 'vServicesCount',
  icon: { type: 'fa', name: 'object-group' },
  theme: 'dark'
}, {
  header: ['components', 'regionDashboard', 'infoBoxes', 'hosts', 'header'],
  dataSource: 'hostsCount',
  icon: { type: 'fa', name: 'server' },
  theme: 'dark'
}, {
  header: ['components', 'regionDashboard', 'infoBoxes', 'vConnectors', 'header'],
  dataSource: 'vConnectorsCount',
  icon: { type: 'fa', name: 'compress' },
  theme: 'dark'
}];

let listInfoBoxes = [{
  header: ['components', 'regionDashboard', 'listInfoBoxes', 'availabilityZones', 'header'],
  baseType: ['components', 'regionDashboard', 'listInfoBoxes', 'availabilityZones', 'baseType'],
  listName: 'availabilityZones',
  listItemFormat: { 
    getLabelFn: (item) => { return item.name; },
    getValueFn: (item) => { return item._id._str; },
  },
  icon: { type: 'material', name: 'developer_board' },
}, {
  header: ['components', 'regionDashboard', 'listInfoBoxes', 'aggregates', 'header'],
  baseType: ['components', 'regionDashboard', 'listInfoBoxes', 'aggregates', 'baseType'],
  listName: 'aggregates',
  listItemFormat: { 
    getLabelFn: (item) => { return item.name; },
    getValueFn: (item) => { return item._id._str; },
  },
  icon: { type: 'material', name: 'storage' },
}];

/*  
 * Lifecycles
 */   
  
Template.RegionDashboard.onCreated(function() {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    _id: null,
    id_path: null,
    instancesCount: 0,
    vServicesCount: 0,
    hostsCount: 0,
    vConnectors: 0,
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
    Inventory.find({ _id: _id }).forEach((region) => {
      instance.state.set('id_path', region.id_path);

      instance.subscribe('inventory?id_path', region.id_path);
      instance.subscribe('inventory?id_path_start&type', region.id_path, 'instance');
      instance.subscribe('inventory?id_path_start&type', region.id_path, 'vservice');
      instance.subscribe('inventory?id_path_start&type', region.id_path, 'host');
      instance.subscribe('inventory?id_path_start&type', region.id_path, 'vconnector');
      instance.subscribe('inventory?id_path_start&type', region.id_path, 'availability_zone');
      instance.subscribe('inventory?id_path_start&type', region.id_path, 'aggregate');

      let idPathExp = new RegExp(`^${regexEscape(region.id_path)}`);

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
    });

  });

});  

/*
Template.RegionDashboard.rendered = function() {
};  
*/

/*
 * Events
 */

Template.RegionDashboard.events({
});
   
/*  
 * Helpers
 */

Template.RegionDashboard.helpers({    
  region: function () {
    let instance = Template.instance();
    let _id = instance.state.get('_id');

    return Inventory.findOne({ _id: _id });
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
    let region_id_path = instance.state.get('id_path');

    return {
      header: R.path(listInfoBox.header, store.getState().api.i18n),
      baseType: R.path(listInfoBox.baseType, store.getState().api.i18n),
      list: getList(listInfoBox.listName, region_id_path),
      //dataInfo: instance.state.get(infoBox.dataSource).toString(),
      icon: new Icon(listInfoBox.icon),
      //theme: infoBox.theme
      listItemFormat: listInfoBox.listItemFormat,
      onItemSelected: function (itemKey) {
        data.onNodeSelected(new Mongo.ObjectID(itemKey));
      }
    };
  },
});

function getList(listName, parentIdPath) {
  let idPathExp = new RegExp(`^${regexEscape(parentIdPath)}`);

  switch (listName) {
  case 'availabilityZones':
    return Inventory.find({ 
      id_path: idPathExp,
      type: 'availability_zone'
    });   

  case 'aggregates':
    return Inventory.find({ 
      id_path: idPathExp,
      type: 'aggregate'
    });   

  default:
    throw 'unknowned list type';
  }
}
