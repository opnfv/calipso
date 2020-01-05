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
 * Template Component: HostDashboard 
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

import './host-dashboard.html';
import {Environments} from "../../../api/environments/environments";
    
let infoBoxes =  [{
  header: ['components', 'hostDashboard', 'infoBoxes', 'vConnectors', 'header'],
  dataSource: 'vConnectorsCount',
  icon: { type: 'fa', name: 'compress' },
  theme: 'dark'
}, {
  header: ['components', 'hostDashboard', 'infoBoxes', 'ports', 'header'],
  dataSource: 'portsCount',
  icon: { type: 'fa', name: 'compress' },
  theme: 'dark'
}, {
  header: ['components', 'hostDashboard', 'infoBoxes', 'networkAgents', 'header'],
  dataSource: 'networkAgentsCount',
  icon: { type: 'fa', name: 'compress' }, // todo: icon
  theme: 'dark'
}, {
  header: ['components', 'hostDashboard', 'infoBoxes', 'pnics', 'header'],
  dataSource: 'pnicsCount',
  icon: { type: 'fa', name: 'compress' }, // todo: icon
  theme: 'dark'
}, {
  header: ['components', 'hostDashboard', 'infoBoxes', 'vEdges', 'header'],
  dataSource: 'vEdgesCount',
  icon: { type: 'fa', name: 'external-link' },
  theme: 'dark'
}];

/*  
 * Lifecycles
 */   
  
Template.HostDashboard.onCreated(function() {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    id_path: null,
    env: null,
    instancesCount: 0,
    vServicesCount: 0,
    containersCount: 0,
    podsCount: 0,
    vConnectors: 0,
    portsCount: 0, 
    networkAgentsCount: 0,
    pnicsCount: 0,
    vEdgesCount: 0,
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
    let host = Inventory.findOne({_id: _id});

    instance.state.set('id_path', host.id_path);
    let env = Environments.findOne({'name': host.environment});
    instance.state.set('env', env);

    let idPathExp = new RegExp(`^${regexEscape(host.id_path)}`);

    instance.subscribe('inventory?id_path', host.id_path);
    if (env.environment_type === 'OpenStack') {
      instance.subscribe('inventory?id_path_start&type', host.id_path, 'instance');
      instance.subscribe('inventory?id_path_start&type', host.id_path, 'vservice');

      instance.state.set('instancesCount', Inventory.find({
          id_path: idPathExp,
          type: 'instance'
      }).count());
      instance.state.set('vServicesCount', Inventory.find({
          id_path: idPathExp,
          type: 'vservice'
      }).count());
    }
    else if (env.environment_type === 'Kubernetes') {
      instance.subscribe('inventory?id_path_start&type', host.id_path, 'container');
      instance.subscribe('inventory?id_path_start&type', host.id_path, 'pod');

      instance.state.set('containersCount', Inventory.find({
          id_path: idPathExp,
          type: 'container'
      }).count());
      instance.state.set('podsCount', Inventory.find({
          id_path: idPathExp,
          type: 'pod'
      }).count());
    }
    instance.subscribe('inventory?id_path_start&type', host.id_path, 'vconnector');
    instance.subscribe('inventory?id_path_start&type', host.id_path, 'network_agent');
    instance.subscribe('inventory?id_path_start&type', host.id_path, 'pnic');
    instance.subscribe('inventory?id_path_start&type', host.id_path, 'vedge');

    Inventory.find({ id_path: host.id_path }).forEach((host) => {
      instance.subscribe('inventory?env&binding:host_id&type',
        host.environment, host.id, 'port');

      instance.state.set('portsCount', Inventory.find({
        environment: host.environment,
        'binding:host_id': host.id,
        type: 'port'
      }).count());
    });

    instance.state.set('vConnectorsCount', Inventory.find({
      id_path: idPathExp,
      type: 'vconnector'
    }).count());

    instance.state.set('networkHostsCount', Inventory.find({
      id_path: idPathExp,
      type: 'network_host'
    }).count());

    instance.state.set('pnicsCount', Inventory.find({
      id_path: idPathExp,
      type: 'pnic'
    }).count());

    instance.state.set('vEdgesCount', Inventory.find({
      id_path: idPathExp,
      type: 'vedge'
    }).count());

  });
});  

/*
Template.HostDashboard.rendered = function() {
};  
*/

/*
 * Events
 */

Template.HostDashboard.events({
});
   
/*  
 * Helpers
 */

Template.HostDashboard.helpers({    
  host: function () {
    let instance = Template.instance();
    let host_id_path = instance.state.get('id_path');

    return Inventory.findOne({ id_path: host_id_path });
  },

  env: function () {
    return Template.instance().state.get('env');
  },

  infoBoxes: function (envType) {
    let boxes = infoBoxes.slice(0);
    if (envType === 'OpenStack') {
      boxes.unshift({
          header: ['components', 'hostDashboard', 'infoBoxes', 'instances', 'header'],
          dataSource: 'instancesCount',
          icon: { type: 'fa', name: 'desktop' },
          theme: 'dark'
      }, {
          header: ['components', 'hostDashboard', 'infoBoxes', 'vServices', 'header'],
          dataSource: 'vServicesCount',
          icon: { type: 'fa', name: 'object-group' },
          theme: 'dark'
      }, )
    }
    else if (envType === 'Kubernetes') {
        boxes.unshift({
            header: ['components', 'hostDashboard', 'infoBoxes', 'containers', 'header'],
            dataSource: 'containersCount',
            icon: { type: 'fa', name: 'cube' },
            theme: 'dark'
        }, {
            header: ['components', 'hostDashboard', 'infoBoxes', 'pods', 'header'],
            dataSource: 'podsCount',
            icon: { type: 'fa', name: 'database' },
            theme: 'dark'
        }, )
    }
    return boxes;
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
});


