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
