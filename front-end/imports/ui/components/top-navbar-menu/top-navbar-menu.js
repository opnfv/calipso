///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: TopNavbarMenu 
 */

import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';

import { store } from '/imports/ui/store/store';
import { idToStr } from '/imports/lib/utilities';
import factory from 'reactive-redux';

import '/imports/ui/components/search-auto-complete-list/search-auto-complete-list';
import '/imports/ui/components/get-started/get-started';
import '/imports/ui/components/env-form/env-form';
import '/imports/ui/components/alarm-icons/alarm-icons';
import '/imports/ui/components/settings-list/settings-list';

import './top-navbar-menu.html';

/*  
 * Lifecycles
 */

let loginButtonsSession = Accounts._loginButtonsSession;

Template.body.events({
    'click': function (e) {
        handleLoginMenu(e);
    }
});

Template.TopNavbarMenu.onCreated(function () {
  let instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    isAutoCompleteOpen: false,
    searchTerm: null,
    loginButtonsOpen: false,
  });

  const mainEnvIdSelector = (state) => (state.components.mainApp.selectedEnvironment._id);
  instance.rdxMainEnvId = factory(mainEnvIdSelector, store);

  instance.tempSearchTerm = null;
  instance.searchDebounced = _.debounce(function () {
    instance.state.set('searchTerm', instance.tempSearchTerm);
    instance.state.set('isAutoCompleteOpen', true);
  }, 250);
});

Template.TopNavbarMenu.events = {
  'keyup #search': function (event) {
    let instance = Template.instance();

    instance.tempSearchTerm = instance.$(event.target).val();
    instance.searchDebounced();
  },

  'click .os-nav-link': function (event) {
    let instance = Template.instance();
    handleLoginMenu(event);
    instance.state.set('isAutoCompleteOpen', false);
  },

  'click .sm-dashboard-link': function () {
    Router.go('Dashboard');
  },

  'click .sm-get-started-link': function () {
    Router.go('getstarted');
  }
};

export function handleLoginMenu(ev) {
  // Toggle login buttons dropdown if clicked on login block
  if ($("#login-main-container").find(ev.target).addBack(ev.target).length > 0) {
      // Keep dropdown open if clicked inside of it
      if ($("#login-dropdown-list").find(ev.target).addBack(ev.target).length === 0) {
          toggleLoginMenu();
      }
  }
  else if ($("#login-buttons").find(ev.target).addBack(ev.target).length === 0) {
      // Close dropdown if clicked anywhere outside of it
      closeLoginMenu();
  }
}

function toggleLoginMenu() {
  if (loginButtonsSession.get('dropdownVisible') === true) { closeLoginMenu(); } else { openLoginMenu(); }
}

function openLoginMenu() {
  loginButtonsSession.set('dropdownVisible', true);
}

export function closeLoginMenu() {
  loginButtonsSession.set('dropdownVisible', false);
  loginButtonsSession.closeDropdown();
}

Template.loginButtons.events({
  'click #login-buttons-open-change-password': function (ev, _instance) {
    if(loginButtonsSession.get('inChangePasswordFlow') === true){
        _instance.$('#login-dropdown-list').addClass('change-password-dialog-wide');
    }
  },
});

Template.TopNavbarMenu.helpers({
  envId: function () {
    let instance = Template.instance();
    return instance.rdxMainEnvId.get();
  },

  searchTerm: function () {
    let instance = Template.instance();
    return instance.state.get('searchTerm');
  },

  argsSearch: function (envId, searchTerm) {
    let instance = Template.instance();

    return {
      isOpen: instance.state.get('isAutoCompleteOpen'),
      envId: envId,
      searchTerm: searchTerm,
      onResultSelected(node) {
        instance.state.set('isAutoCompleteOpen', false);

        let searchInput = instance.$('input#search');
        searchInput.val(node.name_path);

        Router.go('environment', { _id: idToStr(node._envId) }, {
          query: { selectedNodeId: idToStr(node._id) }
        });
      },
      onCloseReq() {
        instance.state.set('isAutoCompleteOpen', false);

        let searchInput = instance.$('input#search');
        searchInput.val(null);
      },
    };
  },

  argsEnvForm: function () {
    let instance = Template.instance();
    let selectedEnvironment = instance.state.get('selectedEnvironment');

    return {
      selectedEnvironment: selectedEnvironment,
      onEnvSelected: function (env) {
        Router.go('environment', { _id: idToStr(env._id) }, { query: `r=${Date.now()}` });
      }
    };
  }

}); // end: helpers
