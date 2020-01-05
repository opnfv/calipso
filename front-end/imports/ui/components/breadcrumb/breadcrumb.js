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
 * Template Component: breadcrumb
 */

import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';
//import { Inventory } from '/imports/api/inventories/inventories';

import '../breadcrumbNode/breadcrumbNode';
import './breadcrumb.html';

Template.breadcrumb.onCreated(function () {
  let instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    nodeId: null,
    nodesList: [],
  });

  instance.autorun(function () {
    let data = Template.currentData();
    new SimpleSchema({
      nodeId: { type: { _str: { type: String, regEx: SimpleSchema.RegEx.Id } } },
      onNodeSelected: { type: Function },
    }).validate(data);

    instance.state.set('nodeId', data.nodeId);
  });

  instance.autorun(function () {
    let nodeId = instance.state.get('nodeId');

    if (R.isNil(nodeId)) { 
      return; 
    } 

    Meteor.apply('expandNodePath', [ nodeId ], { wait: false }, function (err, res) {
      if (err) { 
        console.error(err);
        return;
      }

      if (R.isNil(res)) { 
        instance.state.set('nodesList', []);
        return;
      }
      
      instance.state.set('nodesList', res);
    });
  });
});

Template.breadcrumb.onDestroyed(function () {
});

Template.breadcrumb.helpers({
  nodesList: function () {
    let instance = Template.instance();
    return instance.state.get('nodesList');
  },

  argsNode: function (node) {
    //let instance = Template.instance();
    let data = Template.currentData();

    return {
      node: node,
      onClick: function () {
        data.onNodeSelected(node);
      }
    };
  },
}); // end: helpers
