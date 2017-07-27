/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: TreeNode
 */

//import { Meteor } from 'meteor/meteor';
import { Template } from 'meteor/templating';
import { EJSON } from 'meteor/ejson';
//import { ReactiveDict } from 'meteor/reactive-dict';
import { ReactiveVar } from 'meteor/reactive-var';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { InventoryTreeNodeBehavior } from '/imports/ui/lib/inventory-tree-node-behavior';
import * as R from 'ramda';
import { calcColorMem } from '/imports/lib/utilities';
import 'jquery.scrollto';

import './tree-node.html';

/*
 * Lifecycles
 */

Template.TreeNode.onCreated(function() {
  let instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    node: null,
    openState: 'closed',
    orderDataSubscribe: { counter: 0, data: { node: null, forOpen: false } },
    needOpenCloseAnimation: { counter: 0, data: { type: 'opening', node: null } },
    positionNeeded: false,
    scrollToNodeIsNeeded: false,
  });

  //console.log('tree-node - on create', R.path(['data', 'node', '_id', '_str'], instance));

  //let oldData = null;

  createAttachedFns(instance);

  instance.currentData = new ReactiveVar(null, EJSON.equals);

  instance.autorun((function(_this) {
    return function(_computation) {
      return _this.currentData.set(Template.currentData());
    };
  })(instance));

  instance.autorun(function () {
    //let data = Template.currentData();
    let data = instance.currentData.get();
    //let data = instance.data;

    new SimpleSchema({
      behavior: {
        type: { isOpenDefault: { type: Boolean } },
        blackbox: true
      },
      showDetailsLine: { type: Boolean },
      openState: { type: String },
      node: { type: Object, blackbox: true },
      children: { type: [Object], blackbox: true },
      childDetected: { type: Boolean },
      needChildDetection: { type: Boolean },
      linkDetected: { type: Boolean },
      level: { type: Number },
      positionNeeded: { type: Boolean },
      scrollToNodeIsNeeded: { type: Boolean },
      onResetChildren: { type: Function },
      onChildRead: { type: Function },
      onChildrenRead: { type: Function },
      onStartOpenReq: { type: Function },
      onOpeningDone: { type: Function },
      onStartCloseReq: { type: Function },
      onClosingDone: { type: Function },
      onChildDetected: { type: Function },
      onNodeSelected: { type: Function },
      onPositionRetrieved: { type: Function },
      onScrollToNodePerformed: { type: Function },
      onOpenLinkReq: { type: Function },
      onResetNeedChildDetection: { type: Function },
    }).validate(data);

    instance.state.set('openState', data.openState);
    instance.state.set('node', data.node);
    instance.state.set('positionNeeded', data.positionNeeded);
    instance.state.set('scrollToNodeIsNeeded', data.scrollToNodeIsNeeded);
    instance.state.set('needChildDetection', data.needChildDetection);

    //console.log('tree-node - main autorun - ' + data.node._id._str);

    /*
    R.forEach((keyName) => {
      if (R.isNil(oldData)) { return; }

      if (! R.equals(R.prop(keyName, data), R.prop(keyName, oldData)) ) {
        console.log('tree-node - main autorun - prop change: ' + keyName);
          //R.path([keyName], data), R.path([keyName], oldData));
      }
    }, R.keys(data));

    if (oldData !== data) { console.log('tree-node - main autorn - data ob change'); }

    oldData = data;
    */

  });

  instance.autorun(function () {
    let node = instance.state.get('node');
    let openState = instance.state.get('openState');

    switch (openState) {
    case 'start_open':
      issueOrder(instance, 'orderDataSubscribe', { node: node, forOpen: true });
      setTimeout(() => { 
        instance.data.onOpeningDone([node._id._str], node);
      }, 400);
      break;
    case 'opened':
      issueOrder(instance, 'needOpenCloseAnimation', { type: 'opening', node: node});  
      break;
    case 'start_close':
      issueOrder(instance, 'needOpenCloseAnimation', { type: 'closing', node: node });  
      setTimeout(() => {
        instance.data.onClosingDone([node._id._str]);
      }, 200);
      break;
    case 'closed':
      issueOrder(instance, 'orderDataSubscribe', { node: node, forOpen: false });
      break;
    }
  });

  instance.autorun(() => {
    let order = instance.state.get('orderDataSubscribe');
    if (order.counter == 0) { return; }

    instance.data.onResetChildren(R.append(R.path(['_id', '_str'], order.data.node), []));
    // console.log('reset children in autoron order data sub: ' + order.data.node._id._str);

    if (order.data.forOpen) {
      instance.data.behavior.subscribeGetChildrenFn(instance, order.data.node);

      let children = [];
      let onChildReadThrottle = _.throttle(() => {
        instance.data.onChildrenRead([ order.data.node._id._str ], children);
        children = [];
      }, 200);

      instance.data.behavior.getChildrenFn(order.data.node).forEach((child) => {
        // todo: aggregate the collection into threshold and then dispatch. 
        // debounce/throttle
        // https://lodash.com/docs#debounce
        
        //instance.data.onChildRead(
        //  [order.data.node._id._str, child._id._str], child);

        children = R.append(child, children);
        onChildReadThrottle();
      });
    }
  });

  instance.autorun(() => {
    //let needChildDetection = 
    instance.state.get('needChildDetection');
    let data = instance.data;

    instance.data.behavior.subscribeGetFirstChildFn(instance, data.node);
    // todo: let childDetectedSubmited = false;
    instance.data.behavior.getChildrenFn(data.node).forEach((_child) => {
      instance.data.onChildDetected([data.node._id._str]);
    });

    instance.data.onResetNeedChildDetection([data.node._id._str]);
  });

  instance.autorun(function () {
    let positionNeeded = instance.state.get('positionNeeded'); 
      
    if (positionNeeded) {
      let el = instance.$('>.os-tree-node')[0];
      let rect = el.getBoundingClientRect();
      instance.data.onPositionRetrieved([instance.data.node._id._str], rect);  
    }
  });

  instance.autorun(function () {
    let scrollToNodeIsNeeded = instance.state.get('scrollToNodeIsNeeded'); 
      
    if (scrollToNodeIsNeeded) {
      let el = instance.$('>.os-tree-node')[0];
      let rect = el.getBoundingClientRect();
      if (rect.top < 0) {
        //window.scroll(0, el.offsetTop);
        $(window).scrollTo(el, 50);
        instance.data.onScrollToNodePerformed([instance.data.node._id._str]);
        return;
      }

      let childrenCont = instance.$('>.os-tree-node > .sm-children-list')[0];
      let childrenRect = childrenCont.getBoundingClientRect();
      if (childrenRect.bottom > window.innerHeight) {
        let scrollPos = childrenRect.bottom - window.innerHeight;
        scrollPos = window.scrollY + scrollPos;
        if ((window.scrollY + rect.top) < scrollPos) {
          scrollPos = window.scrollY + rect.top;
        }
        $(window).scrollTo(scrollPos, 50);
      }

      instance.data.onScrollToNodePerformed([instance.data.node._id._str]);
    }
  });

});

Template.TreeNode.rendered = function() {
  let instance = Template.instance();
  // Detect change in isOpen.
  instance.autorun(() => {
    let order = instance.state.get('needOpenCloseAnimation');
    if (order.counter == 0) { return; }

    let $childrenList;

    switch(order.data.type) {
    case 'opening':
      // The children list element is not present on first isOpen change render. We
      // need to wait out of loop inorder to let the render first render to list then 
      // we animate the opening/closing action.
      
      //$childrenList = instance.$('>.sm-children-list');
      $childrenList = instance.$(instance.firstNode).children('.sm-children-list');
      $childrenList.slideDown(200);
      break;

    case 'closing':
      //$childrenList = instance.$('>.sm-children-list');
      $childrenList = instance.$(instance.firstNode).children('.sm-children-list');
      $childrenList.slideUp(200);
      break;
    }

  });
};

/*
 * Events
 */

Template.TreeNode.events({
  'click .sm-details-line': function (event, _instance) {
    event.preventDefault();
    event.stopPropagation();

    let data = Template.currentData();

    if (R.pathEq(['type'], 'host_ref')(data.node)) {
      data.onOpenLinkReq(data.node.environment, data.node.name); 

    } else {
      switch(data.openState) {
      case 'opened':
        R.when(R.pipe(R.isNil, R.not),
          (fn) => fn([data.node._id._str])
        )(data.onStartCloseReq);
        break;

      case 'closed':
        R.when(R.pipe(R.isNil, R.not),
          (fn) => fn([data.node._id._str])
        )(data.onStartOpenReq);
        break;
      }

      data.onNodeSelected(data.node);
    }
  }
});

/*
 * Helpers
 */

Template.TreeNode.helpers({
  argsChild: function (child, _node) {
    let instance = Template.instance();
    //let data = Template.currentData();

    return {
      behavior: InventoryTreeNodeBehavior,
      showDetailsLine: true,
      openState: child.openState,
      node: child.nodeInfo,
      children: child.children,
      childDetected: child.childDetected,
      needChildDetection: child.needChildDetection,
      linkDetected: child.linkDetected,
      level: child.level,
      positionNeeded: child.positionNeeded,
      scrollToNodeIsNeeded: child.scrollToNodeIsNeeded,
      onChildRead: instance._fns.onChildRead,
      onChildrenRead: instance._fns.onChildrenRead,
      onResetChildren: instance._fns.onResetChildren,
      onStartOpenReq: instance._fns.onStartOpenReq,
      onOpeningDone: instance._fns.onOpeningDone,
      onStartCloseReq: instance._fns.onStartCloseReq,
      onClosingDone: instance._fns.onClosingDone,
      onChildDetected: instance._fns.onChildDetected,
      onNodeSelected: instance._fns.onNodeSelected,
      onPositionRetrieved: instance._fns.onPositionRetrieved,
      onScrollToNodePerformed: instance._fns.onScrollToNodePerformed,
      onOpenLinkReq: instance._fns.onOpenLinkReq,
      onResetNeedChildDetection: instance._fns.onResetNeedChildDetection,
    };
  },

  isOpen: function () {
    let instance = Template.instance();
    return R.equals('opened', instance.state.get('openState'));
  },

  calcColor: function (level) {
    return calcColorMem(level);
  },

  linkRefName: function () {
    let instance = Template.instance();
    let node = instance.state.get('node');

    if (R.isNil(node)) { return ''; }
    if (R.propEq('type', 'host_ref', node)) {
      return node.name;
    }

    return '';
  }
}); // end: helpers

function issueOrder(instance, name, data) {
  let val = JSON.parse(instance.state.keys[name]);
  val = R.merge(val, {
    counter: val.counter + 1,
    data: data
  });
  
  instance.state.set(name, val);
}

function createAttachedFns(instance) {

  instance._fns = {
    onChildRead: function (reqPath, nodeInfo) {
      instance.data.onChildRead(
        R.prepend(instance.data.node._id._str, reqPath), nodeInfo);
    },
    onChildrenRead: function (reqPath, childrenInfo) {
      instance.data.onChildrenRead(
        R.prepend(instance.data.node._id._str, reqPath), childrenInfo);
    },
    onResetChildren: function (reqPath) {
      instance.data.onResetChildren(
        R.prepend(instance.data.node._id._str, reqPath));
    },
    onStartOpenReq: (reqPath) => {
      instance.data.onStartOpenReq(
        R.prepend(instance.data.node._id._str, reqPath));
    },
    onOpeningDone: (reqPath, nodeInfo) => {
      instance.data.onOpeningDone(
        R.prepend(instance.data.node._id._str, reqPath), nodeInfo);
    },
    onStartCloseReq: (reqPath) => {
      instance.data.onStartCloseReq(
        R.prepend(instance.data.node._id._str, reqPath));
    },
    onClosingDone: (reqPath) => {
      instance.data.onClosingDone(
        R.prepend(instance.data.node._id._str, reqPath));
    },
    onChildDetected: (reqPath) => {
      instance.data.onChildDetected(
        R.prepend(instance.data.node._id._str, reqPath));
    },
    onNodeSelected: (nodeInfo) => {
      instance.data.onNodeSelected(nodeInfo);
    },
    onPositionRetrieved: (reqPath, rect) => {
      instance.data.onPositionRetrieved(
        R.prepend(instance.data.node._id._str, reqPath),
        rect
      );
    },
    onScrollToNodePerformed: (reqPath) => {
      instance.data.onScrollToNodePerformed(
        R.prepend(instance.data.node._id._str, reqPath)
      );
    },

    onOpenLinkReq: (envName, nodeName) => {
      instance.data.onOpenLinkReq(envName, nodeName);
    },

    onResetNeedChildDetection: (reqPath) => {
      instance.data.onResetNeedChildDetection(
        R.prepend(instance.data.node._id._str, reqPath)
      );
    }
  };
}
