/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import * as R from 'ramda';

import * as actions from '/imports/ui/actions/graph-tooltip-window.actions';

const defaultState = { 
  label: '',
  title: '',
  left: 0,
  top: 0,
  show: false
};

export function reducer(state = defaultState, action) {
  let attrsStr;
  switch (action.type) {
  case actions.ACTIVATE_GRAPH_TOOLTIP_WINDOW:
    attrsStr = JSON.stringify(action.payload.attributes, null, 4)
      .toString()
      .replace(/\,/g,'<BR>')
      .replace(/\[/g,'')
      .replace(/\]/g,'')
      .replace(/\{/g,'')
      .replace(/\}/g,'')
      .replace(/"/g,'');

    return R.merge(state, {
      label: action.payload.label,
      title: attrsStr,
      left: action.payload.left,
      top: action.payload.top - 28,
      show: true
    });

  case actions.CLOSE_GRAPH_TOOLTIP_WINDOW:
    return R.assoc('show', false, state);

  default: 
    return state;
  }
}
