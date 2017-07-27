/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: accordionTreeNode
 */

/* eslint no-undef: off */

import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';

import { Inventory } from '/imports/api/inventories/inventories';
//import { store } from '/client/imports/store';
//import { setCurrentNode } from '/client/imports/actions/navigation';

//import { d3Graph } from '/imports/lib/d3-graph';

import '/imports/ui/components/accordionTreeNodeChildren/accordionTreeNodeChildren';
import './accordionTreeNode.html';

var subMenuClass = 'submenu';
var switchingSpeed = 200;

Template.accordionTreeNode.onCreated(function () {
  var instance = this;
  this.state = new ReactiveDict();
  this.state.setDefault({
    openState: 'close',
    needChildrenClosing: false,
    openedChildId: null,
    showNow: false,
    startAsClickedState: 'not_done',
    data: null,
  });

  instance.autorun(function () {
    //var tempData = instance.state.get('data');

    let data = Template.currentData();
    let node = data.node;
    instance.subscribe('inventory.first-child',
      node.id, node.type, node.name, node.environment);
  });

});

Template.accordionTreeNode.rendered = function () {
  var instance = this;

  setTimeout(function () {
    instance.state.set('showNow', true);
  }, 50);

  instance.autorun(function () {
    var openState = instance.state.get('openState');
    switch (openState) {
    case 'opening':
      // Blaze arcitecture bug: in render the children are not it rendered.
      // There for we need to wait until children are rendered to do the animation.
      instance.state.set('openState', 'open');
      activateNodeAction(instance);
      setTimeout(function () {
        animateOpening(instance.$(instance.firstNode));
      }, 65);
      break;

    case 'closing':

      animateClosing(instance.$(instance.firstNode));
      setTimeout(function () {
        instance.state.set('openState', 'close');
        //instance.data.onClose(instance.data.node.id);
      }, 200);
      break;

    case 'none':
      break;

    default:
      break;
    }
  });

};

Template.accordionTreeNode.helpers({
  reactOnShowOpen: function (showOpen) {
    let instance = Template.instance();
    let openState = instance.state.get('openState');
    let nextOpenState = null;

    if (showOpen === false) {
      if (openState === 'open' ||
          openState === 'opening') {
        nextOpenState = 'closing';
      }
    } else if (showOpen === true) {
      if (openState === 'close' ||
          openState === 'closing') {
        nextOpenState = 'opening';
      }
    }

    if (nextOpenState) {
      setTimeout(function () {
        instance.state.set('openState', nextOpenState);
      }, 10);
    }
  },

  reactOnNewData: function (node) {
    let instance = Template.instance();
    instance.state.set('data', { node: node }); 
  },

  isNot: function (condition) {
    return ! condition;
  },

  isNotClose: function () {
    var instance = Template.instance();
    var openState = instance.state.get('openState');
    return (openState !== 'close');
  },

  hasClique: function(){
    var controller = Iron.controller();
    var envName = controller.state.get('envName');

    if(Inventory.find({
      parent_id: this.node.id,
      parent_type: this.node.type,
      environment: envName,
      clique:true,
      show_in_tree:true
    }).count() > 0){

      return 'true';
    }
    else{
      return 'false';
    }

  },

  hasChildren: function(){
    return hasChildren(this);
  },

  isOpen: function () {
    var instance = Template.instance();
    return instance.state.get('openState') === 'open';
  },

  isOpenOrOpening: function () {
    var instance = Template.instance();
    var openState = instance.state.get('openState');
    return (openState === 'open' || openState === 'opening');
  },

  createChildrenArgs: function(
    parentNode,
    selectedNode
    ) {

    let instance = Template.instance();
    return {
      node: parentNode,
      selectedNode: selectedNode,
      onClick(childNode) {
        instance.data.onClick(childNode);
      },
    };
  },

  isNeedChildrenClosing: function () {
    var instance = Template.instance();
    return instance.state.get('needChildrenClosing');
  },

  closeWhenNeeded: function() {
    var instance = Template.instance();
    var openState = instance.state.get('openState');

    if (! singleOpenOption) { return; }
    if (! instance.data.openedFamilyId) { return; }
    if (openState !== 'open') { return; }
    if (instance.data.node.id === instance.data.openedFamilyId) { return; }

    instance.state.set('openState', 'closing');
  },

  showNow: function () {
    var instance = Template.instance();
    return instance.state.get('showNow');
  },
});

Template.accordionTreeNode.events({
  'click': function(event, instance){
    event.stopPropagation();
    event.preventDefault();

    instance.data.onClick(instance.data.node);

    /*
     * todo : remove code
    store.dispatch(setCurrentNode(
      instance.data.node.id_path,
      instance.data.node.name_path));

    var openState  = instance.state.get('openState');
    var nextState = openState;

    if (hasChildren(instance.data)) {
      switch (openState) {
      case 'open':
        nextState = 'closing';
        break;

      case 'opening':
        break;

      case 'close':
        nextState = 'opening';
        break;

      case 'closing':
        break;
      }

      instance.state.set('openState', nextState);

    }


    */
  },
});

function activateNodeAction (_instance) {

}

function hasChildren(instance) {
  var counterName = 'inventory.first-child!counter!id=' + instance.node.id;
  return Counts.get(counterName) > 0;

  /*
  var controller = Iron.controller();
  var envName = controller.state.get('envName');

  return hasChildrenQuery(instance.node, envName);
  */
}

/*
function hasChildrenQuery(node, envName) {
  return Inventory.find({
    parent_id: node.id,
    parent_type: node.type,
    environment: envName,
    show_in_tree: true
  }, {
    limit: 1
  }).count() > 0;
}
*/

function animateOpening($element) {
  $subMenu = $element.children('.' + subMenuClass);
  $subMenu.slideDown(switchingSpeed);
}

function animateClosing($element) {
  $subMenu = $element.children('.' + subMenuClass);
  $subMenu.slideUp(switchingSpeed);
}
