/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
//import * as R from 'ramda';

export const SET_MAIN_APP_SELECTED_ENVIRONMENT = 'SET_MAIN_APP_SELECTED_ENVIRONMENT';

export function setMainAppSelectedEnvironment(_id, name) {
  return {
    type: SET_MAIN_APP_SELECTED_ENVIRONMENT,
    payload: {
      _id: _id,
      name: name
    }
  };
}
