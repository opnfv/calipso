/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: accordionTreeNodeChildren
 */

/* eslint no-undef: off */

import * as R from 'ramda';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { Inventory } from '/imports/api/inventories/inventories';

import './accordionTreeNodeChildren.html';

Template.accordionTreeNodeChildren.onCreated(function () {
  var instance = this;
  this.state = new ReactiveDict();
  this.state.setDefault({
    data: null,
    siblingId: null
  });

  instance.autorun(function () {
    let data = Template.currentData();
    let node = data.node;
    instance.subscribe('inventory.children',
      node.id, node.type, node.name, node.environment);

    if (R.equals('host_ref', node.type)) {
      instance.subscribe('inventory?name&env&type', 
        node.name, node.environment, 'host');

      Inventory.find({ 
        name: node.name,
        environment: node.environment,
        type: 'host'
      }).forEach((sibling) => {
        instance.state.set('siblingId', sibling.id);
      });
    }
  });

});

Template.accordionTreeNodeChildren.helpers({
  reactOnNewData: function (node) {
    let instance = Template.instance();
    instance.state.set('data', { node: node });
  },

  children: function () {
    let instance = Template.instance();
    let siblingId = instance.state.get('siblingId');

    return getChildrenQuery(instance.data.node, siblingId);
  },

  createTreeNodeArgs: function(
    node,
    selectedNode
    ) {

    var instance = Template.instance();

    let firstChild = null;
    let restOfChildren = null;  
    let showOpen = false;

    if ((! R.isNil(selectedNode)) &&
          selectedNode.length > 0
    ) {
      firstChild = selectedNode[0];
      restOfChildren = selectedNode.length > 1 ? 
        R.slice(1, Infinity, selectedNode) : null;
      showOpen = firstChild.id === node.id ? true : false;
    }

    return {
      node: node,
      showOpen: showOpen,
      selectedNode: restOfChildren,
      onClick: instance.data.onClick
    };
  },


});

Template.accordionTreeNodeChildren.events({
});

function getChildrenQuery(node, siblingId) {
  let query = 
    {
      $or: [
        {
          parent_id: node.id,
          parent_type: node.type,
          environment: node.environment,
          show_in_tree: true
        }
      ]
    };


  if (R.equals('host_ref', node.type)) {
    query = R.merge(query, {
      $or: R.append({
        parent_id: siblingId,
        show_in_tree: true
      }, query.$or)
    });
  }

  console.log('getChildrenQuery', R.toString(query));

  return Inventory.find(query);
}	
