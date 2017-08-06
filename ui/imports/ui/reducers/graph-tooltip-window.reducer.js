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
