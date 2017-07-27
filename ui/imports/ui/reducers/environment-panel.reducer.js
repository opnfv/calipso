/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import * as R from 'ramda';

import * as actions from '/imports/ui/actions/environment-panel.actions';
import { reducer as treeNode } from './tree-node.reducer';
import { 
  updateTreeNodeInfo,
  addUpdateChildrenTreeNode, 
  resetTreeNodeChildren, 
  startOpenTreeNode,
  endOpenTreeNode,
  startCloseTreeNode,
  endCloseTreeNode,
  setChildDetectedTreeNode,
  setPositionReportIsNeededAsOn,
  reportNodePositionRetrieved,
  setScrollToNodeIsNeededAsOn,
  reportScrollToNodePerformed,
  resetNeedChildDetection,
} 
  from '/imports/ui/actions/tree-node.actions';

const defaultState = {
  _id: null,
  envName: null,
  isLoaded: false,
  treeNode: treeNode(),
  selectedNode: {
    _id: null,
    type: null
  },
  showType: 'dashboard'
};

let newState;

export function reducer(state = defaultState, action) {
  switch (action.type) {
  case actions.SET_ENV_NAME:
    return R.assoc('envName', action.payload.envName, state);

  case actions.UPDATE_ENV_TREE_NODE:
    return R.assoc('treeNode',
      treeNode(state.treeNode, 
        updateTreeNodeInfo(action.payload.nodeInfo, 0)),
      state);

  case actions.ADD_UPDATE_CHILDREN_ENV_TREE_NODE:
    return R.assoc('treeNode',
      treeNode(state.treeNode, 
        addUpdateChildrenTreeNode(action.payload.nodePath, action.payload.childrenInfo, 0)),
      state);

  case actions.RESET_ENV_TREE_NODE_CHILDREN:
    return R.assoc('treeNode',
      treeNode(state.treeNode, resetTreeNodeChildren(action.payload.nodePath)),
      state
    );

  case actions.START_OPEN_ENV_TREE_NODE:
    return R.assoc('treeNode',
      treeNode(state.treeNode, startOpenTreeNode(action.payload.nodePath)),
      state
    );

  case actions.END_OPEN_ENV_TREE_NODE:
    return R.assoc('treeNode',
      treeNode(state.treeNode, endOpenTreeNode(action.payload.nodePath)),
      state
    );

  case actions.START_CLOSE_ENV_TREE_NODE:
    return R.assoc('treeNode',
      treeNode(state.treeNode, startCloseTreeNode(action.payload.nodePath)),
      state
    );

  case actions.END_CLOSE_ENV_TREE_NODE:
    return R.assoc('treeNode',
      treeNode(state.treeNode, endCloseTreeNode(action.payload.nodePath)),
      state
    );

  case actions.SET_ENV_CHILD_DETECTED_TREE_NODE:
    return R.assoc('treeNode',
      treeNode(state.treeNode, setChildDetectedTreeNode(action.payload.nodePath)),
      state
    );

  case actions.SET_ENV_SELECTED_NODE:
    if (R.pathEq(['selectedNode', '_id'], action.payload.nodeId, state) &&
      R.pathEq(['selectedNode', 'type'], action.payload.nodeType)
    ) {
      return state;
    }

    return R.merge(state, {
      selectedNode: { 
        _id: action.payload.nodeId,
        type: action.payload.nodeType
      }
    });

  case actions.SET_ENV_SELECTED_NODE_INFO:
    newState = R.merge(state, {
      selectedNode: R.merge(state.selectedNode, {
        type: action.payload.nodeInfo.type,
        clique: action.payload.nodeInfo.clique,
        id_path: action.payload.nodeInfo.id_path
      })
    });

    if (! R.isNil(action.payload.nodeInfo.clique)) {
      newState = R.assoc('showType', 'graph', newState);
    }

    return newState;

  case actions.SET_ENV_SELECTED_NODE_AS_ENV:
    return R.merge(state, {
      selectedNode: {
        _id: state._id,
        type: 'environment'
      }
    });

  case actions.SET_ENV_ENV_ID:
    return R.assoc('_id', action.payload._id, state);

  case actions.SET_ENV_AS_LOADED:
    return R.assoc('isLoaded', true, state);

  case actions.SET_ENV_AS_NOT_LOADED:
    return R.assoc('isLoaded', false, state);

  case actions.SET_SHOW_DASHBOARD:
    return R.assoc('showType', 'dashboard', state);

  case actions.SET_SHOW_GRAPH:
    return R.assoc('showType', 'graph', state);

  case actions.TOGGLE_ENV_SHOW:
    return R.pipe(
      R.ifElse(R.equals('dashboard'), 
        R.always('graph'), 
        R.always('dashboard')),
      R.assoc('showType', R.__, state)
    )(state.showType);

  case actions.SET_ENV_POSITION_REPORT_IS_NEEDED_AS_ON:
    return R.assoc('treeNode',
      treeNode(state.treeNode, setPositionReportIsNeededAsOn(action.payload.nodePath)),
      state
    );

  case actions.REPORT_ENV_NODE_POSITION_RETRIEVED:
    return R.assoc('treeNode',
      treeNode(state.treeNode, reportNodePositionRetrieved(
        action.payload.nodePath, action.payload.rect)),
      state
    );
  
  case actions.SET_ENV_SCROLL_TO_NODE_IS_NEEDED_AS_ON:
    return R.assoc('treeNode',
      treeNode(state.treeNode, setScrollToNodeIsNeededAsOn(
        action.payload.nodePath)),
      state
    );

  case actions.REPORT_ENV_SCROLL_TO_NODE_PERFORMED:
    return R.assoc('treeNode',
      treeNode(state.treeNode, reportScrollToNodePerformed(
        action.payload.nodePath)),
      state
    );

  case actions.RESET_ENV_NEED_CHILD_DETECTION:
    return R.assoc('treeNode',
      treeNode(state.treeNode, resetNeedChildDetection(
        action.payload.nodePath)),
      state
    );

  default:
    return state;
  }
}
