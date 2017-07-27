/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
//import * as R from 'ramda';

export const ACTIVATE_VEDGE_INFO_WINDOW = 'ACTIVATE_VEDGE_INFO_WINDOW';
export const CLOSE_VEDGE_INFO_WINDOW = 'CLOSE_VEDGE_INFO_WINDOW';

export function activateVedgeInfoWindow(node, left, top) {
  // todo: remove. this is for debug
  /*
  node = {
    _id: '0',
    id: 'devstack-vpp1-VPP',
    id_path: '',
    name: 'devstack-vpp1-VPP',
    name_path: '',
    environment: 'Devstack-VPP'
  };
  */

  return {
    type: ACTIVATE_VEDGE_INFO_WINDOW,
    payload: {
      node: node,
      left: left,
      top: top
    }
  };
}

export function closeVedgeInfoWindow() {
  return {
    type: CLOSE_VEDGE_INFO_WINDOW
  };
}
