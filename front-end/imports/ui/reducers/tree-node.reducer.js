///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
//import { Mongo } from 'meteor/mongo';
import * as R from 'ramda';

import * as actions from '/imports/ui/actions/tree-node.actions';
import {isReferenceType} from "../../lib/utilities";

const defaultState = {
  _id: null,
  nodeInfo: {},
  openState: 'closed', // opened, start_close, closed, start_open
  children: [],
  childDetected: false,
  needChildDetection: true,
  linkDetected: false,
  level: 1,
  positionNeeded: false,
  position: null,
  scrollToNodeIsNeeded: false
};

export function reducer(state = defaultState, action) {
  let nodeId;
  let rest;
  //let child;
  //let index;

  if (R.isNil(action)) { return defaultState; }

  switch (action.type) {

  case actions.UPDATE_TREE_NODE_INFO:
    return R.merge(state, {
      _id: action.payload.nodeInfo._id._str,
      nodeInfo: action.payload.nodeInfo,
      openState: 'closed',
      children: [],
      childDetected: false,
      needChildDetection: true,
      linkDetected: isReferenceType(action.payload.nodeInfo.type),
      level: action.payload.level,
    });

  case actions.ADD_UPDATE_CHILDREN_TREE_NODE:
    nodeId = R.head(action.payload.nodePath);
    rest = R.tail(action.payload.nodePath);

    if (R.isNil(nodeId)) {
      let actionChildren = R.map((childInfo) => {
        let existingChild = R.find(
          R.pathEq(['nodeInfo', '_id', '_str'], childInfo._id._str), state.children);

        return reducer(existingChild,  
            actions.updateTreeNodeInfo(childInfo, action.payload.level + 1));
      }, action.payload.childrenInfo);

      let allChildren = R.unionWith(R.eqBy(R.path(['nodeInfo', '_id', '_str'])), 
        actionChildren, state.children);
      
      /*
      R.forEach((actionChild) => {
        let index = R.findIndex(R.pathEq(['nodeInfo', '_id', '_str'], actionChild._id._str),state.children);
        if (index < 0) {
          state.children.push(actionChild);
        } else {
          state.children[index] = actionChild;
        }
      }, actionChildren);
      let allChildren = state.children;
      */

      return R.merge(state, {
        children: allChildren,
        childDetected: R.length(allChildren) > 0
      });
      
      /*
      state.childDetected = R.length(allChildren) > 0;
      return state;
      */
    }

    return reduceActionOnChild(state, 
      actions.addUpdateChildrenTreeNode(
        rest, action.payload.childrenInfo, action.payload.level + 1), 
      nodeId);

  case actions.RESET_TREE_NODE_CHILDREN:
    nodeId = R.head(action.payload.nodePath);
    rest = R.tail(action.payload.nodePath);

    if (R.isNil(nodeId)) {
      return R.merge(state, { 
        children: [],
        childDetected: false,
        needChildDetection: true,
      });
    }

    return reduceActionOnChild(state, actions.resetTreeNodeChildren(rest), nodeId);

  case actions.START_OPEN_TREE_NODE:
    nodeId = R.head(action.payload.nodePath);
    rest = R.tail(action.payload.nodePath);

    if (R.isNil(nodeId)) {
      return R.assoc('openState', 'start_open', state);
    }

    return reduceActionOnChild(state, actions.startOpenTreeNode(rest), nodeId);

  case actions.END_OPEN_TREE_NODE:
    nodeId = R.head(action.payload.nodePath);
    rest = R.tail(action.payload.nodePath);

    if (R.isNil(nodeId)) {
      return R.assoc('openState', 'opened', state);
    }

    return reduceActionOnChild(state, actions.endOpenTreeNode(rest), nodeId);

  case actions.START_CLOSE_TREE_NODE:
    nodeId = R.head(action.payload.nodePath);
    rest = R.tail(action.payload.nodePath);

    if (R.isNil(nodeId)) {
      return R.assoc('openState', 'start_close', state);
    }

    return reduceActionOnChild(state, actions.startCloseTreeNode(rest), nodeId);

  case actions.END_CLOSE_TREE_NODE:
    nodeId = R.head(action.payload.nodePath);
    rest = R.tail(action.payload.nodePath);

    if (R.isNil(nodeId)) {
      return R.assoc('openState', 'closed', state);
    }

    return reduceActionOnChild(state, actions.endCloseTreeNode(rest), nodeId);

  case actions.SET_CHILD_DETECTED_TREE_NODE:
    nodeId = R.head(action.payload.nodePath);
    rest = R.tail(action.payload.nodePath);

    if (R.isNil(nodeId)) {
      return R.assoc('childDetected', true, state);
    }

    return reduceActionOnChild(state, actions.setChildDetectedTreeNode(rest), nodeId);

  case actions.SET_POSITION_REPORT_IS_NEEDED_AS_ON:
    nodeId = R.head(action.payload.nodePath);
    rest = R.tail(action.payload.nodePath);

    if (R.isNil(nodeId)) {
      return R.assoc('positionNeeded', true, state);
    }

    return reduceActionOnChild(state, actions.setPositionReportIsNeededAsOn(rest), nodeId);

  case actions.REPORT_NODE_POSITION_RETRIEVED:
    nodeId = R.head(action.payload.nodePath);
    rest = R.tail(action.payload.nodePath);

    if (R.isNil(nodeId)) {
      return R.merge(state, {
        position: {
          top: action.payload.rect.top,
          bottom: action.payload.rect.bottom,
          height: action.payload.rect.height,
        },
        positionNeeded: false
      });
    }

    return reduceActionOnChild(state, 
        actions.reportNodePositionRetrieved(rest, action.payload.rect), nodeId);

  case actions.SET_SCROLL_TO_NODE_IS_NEEDED_AS_ON:
    nodeId = R.head(action.payload.nodePath);
    rest = R.tail(action.payload.nodePath);

    if (R.isNil(nodeId)) {
      return R.assoc('scrollToNodeIsNeeded', true, state);
    }

    return reduceActionOnChild(state, actions.setScrollToNodeIsNeededAsOn(rest), nodeId);

  case actions.REPORT_SCROLL_TO_NODE_PERFORMED:
    nodeId = R.head(action.payload.nodePath);
    rest = R.tail(action.payload.nodePath);

    if (R.isNil(nodeId)) {
      return R.assoc('scrollToNodeIsNeeded', false, state);
    }

    return reduceActionOnChild(state, actions.reportScrollToNodePerformed(rest), nodeId);

  case actions.RESET_NEED_CHILD_DETECTION:
    nodeId = R.head(action.payload.nodePath);
    rest = R.tail(action.payload.nodePath);

    if (R.isNil(nodeId)) {
      return R.assoc('needChildDetection', false, state);
    }

    return reduceActionOnChild(state, actions.resetNeedChildDetection(rest), nodeId);


  default:
    return state;
  }
}

function reduceActionOnChild(state, action, nodeId) {
  let index = R.findIndex(R.pathEq(['nodeInfo', '_id', '_str'], nodeId), state.children);
  if (index < 0) throw 'error in reduce action on child';
  let child = state.children[index];

  return R.assoc('children',
    R.update(index,
      reducer(child, action),
      state.children),
  state);
}
