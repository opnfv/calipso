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
  Template Component: accordionNavMenu
 */

/* eslint indent: "off" */

import * as R from 'ramda';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
//import { Tracker } from 'meteor/tracker';
//import { Session } from 'meteor/session';
//import { InventoryTreeNodeBehavior } from '/imports/ui/lib/inventory-tree-node-behavior';
import { EnvironmentTreeNodeBehavior } from '/imports/ui/lib/environment-tree-node-behavior';
//import { Inventory } from '/imports/api/inventories/inventories';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';

import '/imports/ui/components/tree-node/tree-node';
import '/imports/ui/components/accordionTreeNode/accordionTreeNode';
import '/imports/ui/components/d3graph/d3graph';

import { store } from '/imports/ui/store/store'; 
import { 
  resetEnvTreeNodeChildren, 
  addUpdateEnvTreeNode,
  addUpdateChildrenEnvTreeNode,
  startOpenEnvTreeNode,
  startCloseEnvTreeNode,
  endCloseEnvTreeNode,
  setEnvChildDetectedTreeNode,
} from '/imports/ui/actions/environment-panel.actions';

import './accordion-nav-menu.html';

Template.accordionNavMenu.onCreated(function () {
  let instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault ({});

  createAttachedFns(instance);

  instance.autorun(function () {
    let data = Template.currentData();

    new SimpleSchema({
      envName: { type: String },
      mainNode: { type: Object, blackbox: true },
      onOpeningDone: { type: Function },
      onNodeSelected: { type: Function },
      onToggleGraphReq: { type: Function },
      onResetSelectedNodeReq: { type: Function },
      onPositionRetrieved: { type: Function },
      onScrollToNodePerformed: { type: Function },
      onOpenLinkReq: { type: Function },
      onResetNeedChildDetection: { type: Function },
      onToggleMenu: { type: Function },
      showCollapsed: { type: Boolean },
    }).validate(data);
  });

});


Template.accordionNavMenu.rendered = function () {
};

Template.accordionNavMenu.onDestroyed(function () {
});

/*
 * Events
 */

Template.accordionNavMenu.events({
  'click .sm-btn-dashboard': function (_event, _instance) {
    let data = Template.currentData();
    data.onResetSelectedNodeReq();  
  },

  'click .sm-toggle-graph-button': function (_event, _instance) {
    let data = Template.currentData();
    data.onToggleGraphReq();
  },

  'click .sm-menu-toggle-btn': function (_event, instance) {
    instance.data.onToggleMenu();
  }
});

/*
 * Helpers
 */

Template.accordionNavMenu.helpers({
  argsTreeNode: function (node) {
    let instance = Template.instance();
    let data = Template.currentData();

    return {
      behavior: EnvironmentTreeNodeBehavior,
      showDetailsLine: false,
      openState: node.openState,
      node: node.nodeInfo,
      children: node.children,
      childDetected: node.childDetected,
      needChildDetection: node.needChildDetection,
      linkDetected: node.linkDetected,
      level: node.level,
      positionNeeded: node.positionNeeded,
      scrollToNodeIsNeeded: node.scrollToNodeIsNeeded,
      onResetChildren: instance._fns.onResetChildren,
      onChildRead: instance._fns.onChildRead,
      onChildrenRead: instance._fns.onChildrenRead,
      onStartOpenReq: instance._fns.onStartOpenReq,
      onStartCloseReq: instance._fns.onStartCloseReq, 
      onClosingDone: instance._fns.onClosingDone,
      onChildDetected: instance._fns.onChildDetected,
      onOpeningDone: data.onOpeningDone,
      onNodeSelected: data.onNodeSelected,
      onPositionRetrieved: data.onPositionRetrieved,
      onScrollToNodePerformed: data.onScrollToNodePerformed,
      onOpenLinkReq: data.onOpenLinkReq,
      onResetNeedChildDetection: data.onResetNeedChildDetection,
    };
  }
}); // end: helpers

function createAttachedFns(instance) {

  instance._fns = {
    onResetChildren: function (nodePath) {
      store.dispatch(resetEnvTreeNodeChildren(R.tail(nodePath)));
    },
    onChildRead: function (nodePath, childNode) {
      store.dispatch(addUpdateEnvTreeNode(R.tail(nodePath), childNode));
    },
    onChildrenRead: function (nodePath, childrenInfo) {
      store.dispatch(addUpdateChildrenEnvTreeNode(R.tail(nodePath), childrenInfo));
    },
    onStartOpenReq: (nodePath) => {
      store.dispatch(startOpenEnvTreeNode(R.tail(nodePath)));
    },
    onStartCloseReq: (nodePath) => {
      store.dispatch(startCloseEnvTreeNode(R.tail(nodePath)));
    },
    onClosingDone: (nodePath) => {
      store.dispatch(endCloseEnvTreeNode(R.tail(nodePath)));
    },
    onChildDetected: (nodePath) => {
      store.dispatch(setEnvChildDetectedTreeNode(R.tail(nodePath)));
    },
  };
}
