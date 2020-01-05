///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
//import * as R from 'ramda';

export const UPDATE_TREE_NODE_INFO = 'UPDATE_TREE_NODE_INFO';
export const ADD_UPDATE_CHILDREN_TREE_NODE = 'ADD_UPDATE_CHILDREN_TREE_NODE';
export const RESET_TREE_NODE_CHILDREN = 'RESET_TREE_NODE_CHILDREN';
export const START_OPEN_TREE_NODE = 'START_OPEN_TREE_NODE';
export const END_OPEN_TREE_NODE = 'END_OPEN_TREE_NODE';
export const START_CLOSE_TREE_NODE = 'START_CLOSE_TREE_NODE';
export const END_CLOSE_TREE_NODE = 'END_CLOSE_TREE_NODE';
export const SET_CHILD_DETECTED_TREE_NODE = 'SET_CHILD_DETECTED_TREE_NODE';
export const SET_POSITION_REPORT_IS_NEEDED_AS_ON = 'SET_POSITION_REPORT_IS_NEEDED_AS_ON';
export const REPORT_NODE_POSITION_RETRIEVED = 'REPORT_NODE_POSITION_RETRIEVED';
export const SET_SCROLL_TO_NODE_IS_NEEDED_AS_ON = 'SET_SCROLL_TO_NODE_IS_NEEDED_AS_ON';
export const REPORT_SCROLL_TO_NODE_PERFORMED = 'REPORT_SCROLL_TO_NODE_PERFORMED';
export const RESET_NEED_CHILD_DETECTION = 'RESET_NEED_CHILD_DETECTION';

export function updateTreeNodeInfo(nodeInfo, level) {
  return {
    type: UPDATE_TREE_NODE_INFO,
    payload: {
      nodeInfo: nodeInfo,
      level: level
    }
  };
}

export function addUpdateChildrenTreeNode(nodePath, childrenInfo, level) {
  return {
    type: ADD_UPDATE_CHILDREN_TREE_NODE,
    payload: {
      nodePath: nodePath,
      childrenInfo: childrenInfo,
      level: level
    },
  };
}

export function resetTreeNodeChildren(nodePath) {
  return {
    type: RESET_TREE_NODE_CHILDREN,
    payload: {
      nodePath: nodePath,
    }
  };
}

export function startOpenTreeNode(nodePath) {
  return {
    type: START_OPEN_TREE_NODE,
    payload: {
      nodePath: nodePath,
    }
  };
}

export function endOpenTreeNode(nodePath) {
  return {
    type: END_OPEN_TREE_NODE,
    payload: {
      nodePath: nodePath,
    }
  };
}

export function startCloseTreeNode(nodePath) {
  return {
    type: START_CLOSE_TREE_NODE,
    payload: {
      nodePath: nodePath,
    }
  };
}

export function endCloseTreeNode(nodePath) {
  return {
    type: END_CLOSE_TREE_NODE,
    payload: {
      nodePath: nodePath,
    }
  };
}

export function setChildDetectedTreeNode(nodePath) {
  return {
    type: SET_CHILD_DETECTED_TREE_NODE,
    payload: {
      nodePath: nodePath
    }
  };
}

export function setPositionReportIsNeededAsOn(nodePath) {
  return {
    type: SET_POSITION_REPORT_IS_NEEDED_AS_ON,
    payload: {
      nodePath: nodePath
    }
  };
}

export function reportNodePositionRetrieved(nodePath, rect) {
  return {
    type: REPORT_NODE_POSITION_RETRIEVED,
    payload: {
      nodePath: nodePath, 
      rect: rect
    }
  };
}

export function setScrollToNodeIsNeededAsOn(nodePath) {
  return {
    type: SET_SCROLL_TO_NODE_IS_NEEDED_AS_ON,
    payload: {
      nodePath: nodePath 
    }
  };
}

export function reportScrollToNodePerformed(nodePath) {
  return {
    type: REPORT_SCROLL_TO_NODE_PERFORMED,
    payload: {
      nodePath: nodePath
    }
  };
}

export function resetNeedChildDetection(nodePath) {
  return {
    type: RESET_NEED_CHILD_DETECTION,
    payload: {
      nodePath: nodePath
    }
  };
}
