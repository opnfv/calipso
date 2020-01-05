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

export const SET_ENV_NAME = 'SET_ENV_NAME';
export const UPDATE_ENV_TREE_NODE = 'UPDATE_ENV_TREE_NODE';
export const ADD_UPDATE_CHILDREN_ENV_TREE_NODE = 'ADD_UPDATE_CHILDREN_ENV_TREE_NODE';
export const RESET_ENV_TREE_NODE_CHILDREN = 'RESET_ENV_TREE_NODE_CHILDREN';
export const START_OPEN_ENV_TREE_NODE = 'START_OPEN_ENV_TREE_NODE';
export const END_OPEN_ENV_TREE_NODE = 'END_OPEN_ENV_TREE_NODE';
export const START_CLOSE_ENV_TREE_NODE = 'START_CLOSE_ENV_TREE_NODE';
export const END_CLOSE_ENV_TREE_NODE = 'END_CLOSE_ENV_TREE_NODE';
export const SET_ENV_CHILD_DETECTED_TREE_NODE = 'SET_ENV_CHILD_DETECTED_TREE_NODE';
export const SET_ENV_SELECTED_NODE = 'SET_ENV_SELECTED_NODE';
export const SET_ENV_ENV_ID = 'SET_ENV_ENV_ID';
export const SET_ENV_SELECTED_NODE_INFO = 'SET_ENV_SELECTED_NODE_INFO';
export const SET_ENV_AS_LOADED = 'SET_ENV_AS_LOADED';
export const SET_ENV_AS_NOT_LOADED = 'SET_ENV_AS_NOT_LOADED';
export const SET_ENV_SELECTED_NODE_AS_ENV = 'SET_ENV_SELECTED_NODE_AS_ENV';
export const SET_SHOW_DASHBOARD = 'SET_SHOW_DASHBOARD';
export const SET_SHOW_GRAPH = 'SET_SHOW_GRAPH';
export const TOGGLE_ENV_SHOW = 'TOGGLE_ENV_SHOW';
export const SET_ENV_POSITION_REPORT_IS_NEEDED_AS_ON = 'SET_ENV_POSITION_REPORT_IS_NEEDED_AS_ON';
export const REPORT_ENV_NODE_POSITION_RETRIEVED = 'REPORT_ENV_NODE_POSITION_RETRIEVED';
export const SET_ENV_SCROLL_TO_NODE_IS_NEEDED_AS_ON = 'SET_ENV_SCROLL_TO_NODE_IS_NEEDED_AS_ON';
export const REPORT_ENV_SCROLL_TO_NODE_PERFORMED = 'REPORT_ENV_SCROLL_TO_NODE_PERFORMED';
export const RESET_ENV_NEED_CHILD_DETECTION = 'RESET_ENV_NEED_CHILD_DETECTION';

export function setEnvName(envName) {
  return {
    type: SET_ENV_NAME,
    payload: {
      envName: envName
    }
  };
}

export function updateEnvTreeNode(nodeInfo) {
  return {
    type: UPDATE_ENV_TREE_NODE,
    payload: {
      nodeInfo: nodeInfo
    }
  };
}

export function addUpdateChildrenEnvTreeNode(nodePath, childrenInfo) {
  return {
    type: ADD_UPDATE_CHILDREN_ENV_TREE_NODE,
    payload: {
      nodePath: nodePath,
      childrenInfo: childrenInfo
    },
  };
}

export function resetEnvTreeNodeChildren(nodePath) {
  return {
    type: RESET_ENV_TREE_NODE_CHILDREN,
    payload: {
      nodePath: nodePath,
    }
  };
}

export function startOpenEnvTreeNode(nodePath) {
  return {
    type: START_OPEN_ENV_TREE_NODE,
    payload: {
      nodePath: nodePath,
    }
  };
}

export function endOpenEnvTreeNode(nodePath) {
  return {
    type: END_OPEN_ENV_TREE_NODE,
    payload: {
      nodePath: nodePath,
    }
  };
}

export function startCloseEnvTreeNode(nodePath) {
  return {
    type: START_CLOSE_ENV_TREE_NODE,
    payload: {
      nodePath: nodePath,
    }
  };
}

export function endCloseEnvTreeNode(nodePath) {
  return {
    type: END_CLOSE_ENV_TREE_NODE,
    payload: {
      nodePath: nodePath,
    }
  };
}

export function setEnvChildDetectedTreeNode(nodePath) {
  return {
    type: SET_ENV_CHILD_DETECTED_TREE_NODE,
    payload: {
      nodePath: nodePath
    }
  };
}

export function setEnvSelectedNode(nodeId, nodeType) {
  return {
    type: SET_ENV_SELECTED_NODE,
    payload: {
      nodeId: nodeId,
      nodeType: nodeType
    }
  };
}

export function setEnvSelectedNodeAsEnv() {
  return {
    type: SET_ENV_SELECTED_NODE_AS_ENV,
  };
}

export function setEnvEnvId(_id) {
  return {
    type: SET_ENV_ENV_ID,
    payload: {
      _id: _id
    }
  };
}

export function setEnvSelectedNodeInfo(nodeInfo) {
  return {
    type: SET_ENV_SELECTED_NODE_INFO,
    payload: {
      nodeInfo: nodeInfo
    }
  };
}

export function setEnvAsLoaded() {
  return {
    type: SET_ENV_AS_LOADED,
  };
}

export function setEnvAsNotLoaded() {
  return {
    type: SET_ENV_AS_NOT_LOADED
  };
}

export function setShowDashboard() {
  return {
    type: SET_SHOW_DASHBOARD
  };
}

export function setShowGraph() {
  return {
    type: SET_SHOW_GRAPH
  };
}

export function toggleEnvShow() {
  return {
    type: TOGGLE_ENV_SHOW
  };
}

export function setEnvPositionReportIsNeededAsOn(nodePath) {
  return {
    type: SET_ENV_POSITION_REPORT_IS_NEEDED_AS_ON,
    payload: {
      nodePath: nodePath
    }
  };
}

export function reportEnvNodePositionRetrieved(nodePath, rect) {
  return {
    type: REPORT_ENV_NODE_POSITION_RETRIEVED,
    payload: {
      nodePath: nodePath,
      rect: rect
    }
  };
}

export function setEnvScrollToNodeIsNeededAsOn(nodePath) {
  return {
    type: SET_ENV_SCROLL_TO_NODE_IS_NEEDED_AS_ON,
    payload: {
      nodePath: nodePath
    }
  };
}

export function reportEnvScrollToNodePerformed(nodePath) {
  return {
    type: REPORT_ENV_SCROLL_TO_NODE_PERFORMED,
    payload: {
      nodePath: nodePath
    }
  };
}

export function resetEnvNeedChildDetection(nodePath) {
  return {
    type: RESET_ENV_NEED_CHILD_DETECTION,
    payload: {
      nodePath: nodePath
    }
  };
}
