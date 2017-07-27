/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
//import * as R from 'ramda';

export const ACTIVATE_GRAPH_TOOLTIP_WINDOW = 'ACTIVATE_GRAPH_TOOLTIP_WINDOW';
export const CLOSE_GRAPH_TOOLTIP_WINDOW = 'CLOSE_GRAPH_TOOLTIP_WINDOW';

export function activateGraphTooltipWindow(label, attributes, left, top) {
  return {
    type: ACTIVATE_GRAPH_TOOLTIP_WINDOW,
    payload: {
      label: label,
      attributes: attributes,
      left: left,
      top: top
    }
  };
}

export function closeGraphTooltipWindow() {
  return {
    type: CLOSE_GRAPH_TOOLTIP_WINDOW
  };
}
