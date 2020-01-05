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

import * as actions from '/imports/ui/actions/search-interested-parties';

const defaultState = { 
  listeners: [], 
  searchTerm: null, 
  searchAutoCompleteTerm: null,
  searchAutoCompleteFutureId: null
};

function reducer(state = defaultState, action) {
  let newListeners;

  switch (action.type) {
  case actions.ADD_SEARCH_INTERESTED_PARTY: 
    newListeners = R.unionWith(
        R.eqBy(R.prop('action')),
        state.listeners, 
        [{ action: action.payload.listener }]);
    return R.assoc('listeners', newListeners, state);

  case actions.REMOVE_SEARCH_INTERESTED_PARTY: 
    newListeners = R.differenceWith(
      R.eqBy(R.prop('action')),
      state.listeners, 
      [{ action:action.payload.listener }]);
    return R.assoc('listeners', newListeners, state);

  case actions.SET_SEARCH_TERM:
    asyncCall(() => { 
      notifyListeners(action.payload.searchTerm, state.listeners); 
    });  
    return R.assoc('searchTerm', action.payload.searchTerm, state);

  case actions.SET_SEARCH_AUTO_COMPLETE_TERM:
    return R.assoc('searchAutoCompleteTerm', action.payload.searchTerm, state);

  case actions.RESET_SEARCH_AUTO_COMPLETE_FUTURE:
    if (! R.isNil(state.searchAutoCompleteFutureId)) {
      clearTimeout(state.searchAutoCompleteFutureId);
    }
    return R.assoc('searchAutoCompleteFutureId', null, state);

  case actions.SET_SEARCH_AUTO_COMPLETE_FUTURE:
    if (! R.isNil(state.searchAutoCompleteFutureId)) {
      clearTimeout(state.searchAutoCompleteFutureId);
    }
    return R.assoc('searchAutoCompleteFutureId', action.payload.futureId, state);

  default:
    return state;
  }
}

function asyncCall(fnObject) {
  setTimeout(() => {
    fnObject.call(null);
  }, 0);
}

function notifyListeners(searchTerm, listeners) {
  R.forEach((listenerItem) => {
    listenerItem.action.call(null, searchTerm);
  }, listeners);
}

export const searchInterestedParties = reducer;
