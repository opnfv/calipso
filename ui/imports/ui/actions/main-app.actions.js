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
