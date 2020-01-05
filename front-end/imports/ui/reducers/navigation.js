///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import * as R from 'ramda';

import * as actions from '/imports/ui/actions/navigation';

const defaultState = { current: [], lastActionable: [] };

function reducer(state = defaultState, action) {
  let lastActionable = null;

  switch (action.type) {
  case actions.SET_CURRENT_NODE:
    lastActionable = isActionable(action.payload.nodeChain) ? action.payload.nodeChain :
        state.lastActionable;

    return R.merge(state, {
      current: action.payload.nodeChain,
      lastActionable: lastActionable
    });

  case actions.SET_CURRENT_NODE_FROM_TREE_CONTROL:
    lastActionable = isActionable(action.payload.nodeChain) ? action.payload.nodeChain :
        state.lastActionable;

    if (contains(action.payload.nodeChain, state.current)) {
      let equalLastIndex = findEqualLastIndex(action.payload.nodeChain, state.current);
      return R.merge(state, {
        current: R.slice(0, equalLastIndex, action.payload.nodeChain),
        lastActionable: lastActionable
      });
    } else {
      return R.merge(state, {
        current: action.payload.nodeChain,
        lastActionable: lastActionable
      });
    }

  default:
    return state;
  }
}

function contains(subArray, array) {
  let equalLastIndex = findEqualLastIndex(subArray, array);

  if (subArray.length <= array.length &&
      equalLastIndex >= 0 &&
      subArray.length === equalLastIndex + 1) {

    return true;
  }

  return false;
}

function findEqualLastIndex (arrayA, arrayB) {
  let indexResult = -1;

  for (let i = 0; (i < arrayA.length) && (i < arrayB.length); i++) {
    if (equalsNodes(arrayA[i], arrayB[i])) {
      indexResult = i;
    } else {
      break;
    }
  }

  return indexResult;
}

function equalsNodes(nodeA, nodeB) {
  if (nodeA.fullIdPath !== nodeB.fullIdPath) { return false; }
  if (nodeA.fullNamePath !== nodeB.fullNamePath) { return false; }

  return true;
}

function isActionable(nodeChain) {
  let last = R.last(nodeChain);

  if (R.isNil(last)) { return false; }
  if (R.isNil(last.item)) { return false; }

  if (! R.isNil(last.item.clique)) { return true; }

  if (last.item.id === 'aggregate-WebEx-RTP-SSD-Aggregate-node-24') {
    return true;
  }

  return false;
}

export const navigation = reducer;
