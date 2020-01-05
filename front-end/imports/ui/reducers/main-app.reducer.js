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

import * as actions from '/imports/ui/actions/main-app.actions';

const defaultState = {
  selectedEnvironment: {}, 
};

export function reducer(state = defaultState, action) {
  switch (action.type) {
  case actions.SET_MAIN_APP_SELECTED_ENVIRONMENT:
    return R.assoc('selectedEnvironment', {
      _id: action.payload._id,
      name: action.payload.name
    }, state);

  default:
    return state;
  }
}
