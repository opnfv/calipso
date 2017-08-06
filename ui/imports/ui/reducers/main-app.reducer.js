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
