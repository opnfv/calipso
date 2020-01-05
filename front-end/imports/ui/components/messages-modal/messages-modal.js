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
 * Template Component: MessagesModal
 */

//import { Meteor } from 'meteor/meteor';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { Counter } from 'meteor/natestrauser:publish-performant-counts';
import * as R from 'ramda';
//import { Messages } from '/imports/api/messages/messages';
import { Environments } from '/imports/api/environments/environments';
import { idToStr } from '/imports/lib/utilities';

import { UserSettings } from '/imports/api/user-settings/user-settings';

import '/imports/ui/components/pager/pager';

import './messages-modal.html';

/*
 * Lifecycles
 */

Template.MessagesModal.onCreated(function () {
  let instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    msgsViewBackDelta: 1,
    messageLevel: 'info',
    iconType: null,
    listHeader: null,
    envName: null,
    page: 1,
    amountPerPage: 10,
    messages: [],
  });

  instance.autorun(function () {

    //let amountPerPage = instance.state.get('amountPerPage');
    //let page = instance.state.get('page');
    let envName = instance.state.get('envName');
    let messageLevel = instance.state.get('messageLevel');

    instance.subscribe('user_settings?user');
    UserSettings.find({ user_id: Meteor.userId() }).forEach((userSettings) => {
      instance.state.set('msgsViewBackDelta', userSettings.messages_view_backward_delta);
    });

    /*

    instance.subscribe('messages?env&level&page&amount', envName, messageLevel, page, amountPerPage);
   
    */
    let backDelta = instance.state.get('msgsViewBackDelta');
    instance.subscribe('messages/count');
    instance.subscribe('messages/count?backDelta', backDelta);
    instance.subscribe('messages/count?level', 'info');
    instance.subscribe('messages/count?level', 'warning');
    instance.subscribe('messages/count?level', 'error');

    if (!R.isNil(envName)) {
      instance.subscribe('messages/count?level&env', messageLevel, envName);
    }
  });

  instance.autorun(function () {
    let level = instance.state.get('messageLevel');
    let envName = instance.state.get('envName');
    let page = instance.state.get('page');
    let amountPerPage = instance.state.get('amountPerPage');

    Meteor.apply('messages/get?level&env&page&amountPerPage&sortField&sortDirection', [
      level, envName, page, amountPerPage, null, null
    ], {
        wait: false
      }, function (err, res) {
        if (err) {
          console.error(R.toString(err));
          return;
        }

        instance.state.set('messages', res);
      });
  });
});

/*
Template.MessagesModal.rendered = function() {
};
*/

/*
 * Events
 */

Template.MessagesModal.events({
  'show.bs.modal #messagesModalGlobal': function (event, instance) {
    let data = event.relatedTarget.dataset;

    setParams(data.messageLevel, data.envName, instance);
  },

  'click .sm-display-context-link': function (event, instance) {
    event.preventDefault();
    let envName = event.target.dataset.envName;
    let nodeId = event.target.dataset.itemId;

    let environment = Environments.findOne({ name: envName });

    Meteor.apply('inventoryFindNode?env&id', [
      environment.name,
      nodeId,
    ], {
        wait: false
      }, function (err, resp) {
        if (err) {
          console.error(R.toString(err));
          return;
        }

        if (R.isNil(resp.node)) {
          console.error('error finding node related to message', R.toString(nodeId));
          return;
        }

        Router.go('environment', {
          _id: idToStr(environment._id)
        }, {
            query: {
              selectedNodeId: idToStr(resp.node._id)
            }
          });

        instance.$('#messagesModalGlobal').modal('hide');

      });

  }
});

/*
 * Helpers
 */

Template.MessagesModal.helpers({
  iconType: function () {
    let instance = Template.instance();
    return instance.state.get('iconType');
  },

  listHeader: function () {
    let instance = Template.instance();
    return instance.state.get('listHeader');
  },

  envName: function () {
    let instance = Template.instance();
    return instance.state.get('envName');
  },

  messages: function () {
    let instance = Template.instance();
    return instance.state.get('messages');
  },

  currentPage: function () {
    let instance = Template.instance();
    return instance.state.get('page');
  },

  amountPerPage: function () {
    let instance = Template.instance();
    return instance.state.get('amountPerPage');
  },

  totalMessages: function () {
    let instance = Template.instance();
    let level = instance.state.get('messageLevel');
    let env = instance.state.get('envName');

    if (R.isNil(env)) {
      return Counter.get(`messages/count?level=${level}`);
    } else {
      return Counter.get(`messages/count?level=${level}&env=${env}`);
    }
  },

  argsPager: function (currentPage, amountPerPage, totalMessages) {
    let instance = Template.instance();
    let totalPages = Math.ceil(totalMessages / amountPerPage);

    return {
      disableNext: currentPage * amountPerPage > totalMessages,
      disablePrev: currentPage == 1,
      totalPages: totalPages,
      currentPage: currentPage,
      onReqNext: function () {
        console.log('next');
        let page = (currentPage * amountPerPage > totalMessages) ? currentPage : currentPage + 1;
        instance.state.set('page', page);
      },
      onReqPrev: function () {
        console.log('prev');
        let page = (currentPage == 1) ? currentPage : currentPage - 1;
        instance.state.set('page', page);
      },
      onReqFirst: function () {
        console.log('req first');
        instance.state.set('page', 1);
      },
      onReqLast: function () {
        console.log('req last');
        instance.state.set('page', totalPages);
      },
      onReqPage: function (pageNumber) {
        console.log('req page');
        let page;
        if (pageNumber <= 1) {
          page = 1;
        } else if (pageNumber > Math.ceil(totalMessages / amountPerPage)) {
          page = totalPages;
        } else {
          page = pageNumber;
        }

        instance.state.set('page', page);
      },
    };
  },

  argsInvPropDisplay: function (env, nodeId) {
    return {
      env: env,
      nodeId: nodeId,
      displayFn: (node) => {
        if (R.isNil(node)) { return ''; }
        return `${node.object_name} - ${node.type}`;
      }
    };
  },
}); // end: helpers

function setParams(messageLevel, envName, instance) {
  instance.state.set('messageLevel', messageLevel);
  instance.state.set('iconType', calcIconType(messageLevel));
  instance.state.set('listHeader', calcListHeader(messageLevel, envName));
  instance.state.set('envName', envName);
  instance.state.set('page', 1);
}

function calcIconType(messageLevel) {
  switch (messageLevel) {
    case 'notify':
      return 'notifications';
    case 'info':
      return 'info';
    case 'warning':
      return 'warning';
    case 'error':
      return 'error';
    default:
      throw 'unimplemented message level for icon';
  }
}

function calcListHeader(messageLevel, envName) {
  let header;

  switch (messageLevel) {
    case 'notify':
      header = 'List of notifications';
      break;
    case 'info':
      header = 'List of info messages';
      break;
    case 'warning':
      header = 'List of warnings';
      break;
    case 'error':
      header = 'List of errors';
      break;
    default:
      throw 'unimplemented message level for list header';
  }

  if (!R.isNil(envName)) {
    header = header + ` for environment ${envName}.`;
  }

  return header;
}
