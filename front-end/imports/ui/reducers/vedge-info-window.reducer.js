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

import * as actions from '/imports/ui/actions/vedge-info-window.actions';

const defaultState = { 
  node: null,
  left: 0,
  top: 0,
  show: false
};

export function reducer(state = defaultState, action) {
  let newState;

  switch (action.type) {
  case actions.ACTIVATE_VEDGE_INFO_WINDOW:
    newState = R.merge(state, {
      node: R.pick([
        '_id', 
        'id', 
        'id_path', 
        'name', 
        'name_path',
        'environment'
      ], action.payload.node),
      left: action.payload.left,
      top: action.payload.top - 28,
      show: true
    });
    return newState;

  case actions.CLOSE_VEDGE_INFO_WINDOW:
    return R.merge(state, {
      show: false,
      top: 0,
      left: 0
    });

  default: 
    return state;
  }
}
