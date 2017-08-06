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
