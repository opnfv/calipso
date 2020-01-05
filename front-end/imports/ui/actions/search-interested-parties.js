///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
//import * as R from 'ramda';

const ADD_SEARCH_INTERESTED_PARTY = 'ADD_SEARCH_INTERESTED_PARTY';
const REMOVE_SEARCH_INTERESTED_PARTY = 'REMOVE_SEARCH_INTERESTED_PARTY';
const SET_SEARCH_TERM = 'SET_SEARCH_TERM';
const SET_SEARCH_AUTO_COMPLETE_TERM = 'SET_SEARCH_AUTO_COMPLETE_TERM';
const RESET_SEARCH_AUTO_COMPLETE_FUTURE = 'RESET_SEARCH_AUTO_COMPLETE_FUTURE';
const SET_SEARCH_AUTO_COMPLETE_FUTURE = 'SET_SEARCH_AUTO_COMPLETE_FUTURE';

const AUTO_COMPLETE_DELAY = 300; // miliseconds.

function addSearchInterestedParty(listener) {
  return {
    type: ADD_SEARCH_INTERESTED_PARTY,
    payload: {
      listener: listener
    }
  };
}

function removeSearchInterestedParty(listener) {
  return {
    type: REMOVE_SEARCH_INTERESTED_PARTY,
    payload: {
      listener: listener
    }
  };
}

function setSearchTerm(searchTerm) {
  return {
    type: SET_SEARCH_TERM,
    payload: {
      searchTerm: searchTerm
    }
  };
}

function setSearchAutoCompleteTerm(searchTerm) {
  return {
    type: SET_SEARCH_AUTO_COMPLETE_TERM,
    payload: {
      searchTerm: searchTerm
    }
  };
}

function resetSearchAutoCompleteFuture() {
  return {
    type: RESET_SEARCH_AUTO_COMPLETE_FUTURE,
  };
}

function setSearchAutoCompleteFuture(futureId) {
  return {
    type: SET_SEARCH_AUTO_COMPLETE_FUTURE,
    payload: {
      futureId: futureId
    }
  };
}

function notifySearchAutoCompleteTermChanged(searchTerm) {
  return (dispatch) => {
    let autoCompleteFutureId = setTimeout(() => {
      dispatch(resetSearchAutoCompleteFuture());
      dispatch(setSearchAutoCompleteTerm(searchTerm));
    }, AUTO_COMPLETE_DELAY);
    dispatch(setSearchAutoCompleteFuture(autoCompleteFutureId));
  };
}

export {
  ADD_SEARCH_INTERESTED_PARTY,
  REMOVE_SEARCH_INTERESTED_PARTY,
  SET_SEARCH_TERM,
  SET_SEARCH_AUTO_COMPLETE_TERM,
  RESET_SEARCH_AUTO_COMPLETE_FUTURE,
  SET_SEARCH_AUTO_COMPLETE_FUTURE,
  addSearchInterestedParty,
  removeSearchInterestedParty,
  setSearchTerm,
  setSearchAutoCompleteTerm,
  notifySearchAutoCompleteTermChanged
};
