/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: ProjectDashboard 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';


import { Inventory } from '/imports/api/inventories/inventories';
import { store } from '/imports/ui/store/store';
import { Icon } from '/imports/lib/icon';
import { regexEscape } from '/imports/lib/regex-utils';
        
import '/imports/ui/components/accordion-nav-menu/accordion-nav-menu';

import '/imports/ui/components/network-info-box/network-info-box';

import './project-dashboard.html';     
    
/*  
 * Lifecycles
 */   
  
Template.ProjectDashboard.onCreated(function() {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    _id: null,
    id_path: null,
    infoBoxes: [{
      header: ['components', 'projectDashboard', 'infoBoxes', 'networks', 'header'],
      dataSource: 'networksCount',
      icon: { type: 'material', name: 'device_hub' },
      theme: 'dark'
    }, {
      header: ['components', 'projectDashboard', 'infoBoxes', 'ports', 'header'],
      dataSource: 'portsCount',
      icon: { type: 'material', name: 'settings_input_hdmi' },
      theme: 'dark'
    }],
    networksCount: 0,
    portsCount: 0,
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
    
    Inventory.find({ _id: _id }).forEach((project) => {
      instance.state.set('id_path', project.id_path);

      instance.subscribe('inventory?id_path', project.id_path);
      instance.subscribe('inventory?id_path_start&type', project.id_path, 'network');
      instance.subscribe('inventory?id_path_start&type', project.id_path, 'port');

      let idPathExp = new RegExp(`^${regexEscape(project.id_path)}`);

      instance.state.set('networksCount', Inventory.find({ 
        id_path: idPathExp,
        type: 'network'
      }).count());

      instance.state.set('portsCount', Inventory.find({ 
        id_path: idPathExp,
        type: 'port'
      }).count());
    });
  });
});  

/*
Template.ProjectDashboard.rendered = function() {
};  
*/

/*
 * Events
 */

Template.ProjectDashboard.events({
});
   
/*  
 * Helpers
 */

Template.ProjectDashboard.helpers({    
  project: function () {
    let instance = Template.instance();
    let _id = instance.state.get('_id');
    return Inventory.findOne({ _id: _id });
  },

  infoBoxes: function () {
    let instance = Template.instance();
    return instance.state.get('infoBoxes');
  },

  networks: function () {
    let instance = Template.instance();
    let project_id_path = instance.state.get('id_path');
    let idPathExp = new RegExp(`^${regexEscape(project_id_path)}`);
    return Inventory.find({ 
      id_path: idPathExp,
      type: 'network'
    });
  },

  genArgsInfoBox: function (infoBox) {
    let instance = Template.instance();

    return {
      header: R.path(infoBox.header, store.getState().api.i18n),
      dataInfo: instance.state.get(infoBox.dataSource).toString(),
      icon: new Icon(infoBox.icon),
      theme: infoBox.theme
    };
  },

  argsNetworkInfoBox: function (network) {
    return {
      network: network
    };
  }
});
