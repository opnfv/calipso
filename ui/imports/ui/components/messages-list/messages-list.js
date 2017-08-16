/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: MessagesList 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import * as R from 'ramda';
import { Template } from 'meteor/templating';
import { Counter } from 'meteor/natestrauser:publish-performant-counts';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
//import { Messages } from '/imports/api/messages/messages';
import { Environments } from '/imports/api/environments/environments';
import { idToStr } from '/imports/lib/utilities';
        
import '/imports/ui/components/pager/pager';
import '/imports/ui/components/inventory-properties-display/inventory-properties-display';

import './messages-list.html';     
    
/*  
 * Lifecycles
 */   
  
Template.MessagesList.onCreated(function() {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    env: null,
    page: 1,
    amountPerPage: 10,
    sortField: 'timestamp',
    sortDirection: -1,
    messsages: [],
  });

  instance.autorun(function () {
    //let data = Template.currentData();
    
    var controller = Iron.controller();
    var params = controller.getParams();
    var query = params.query;

    new SimpleSchema({
    }).validate(query);

    instance.subscribe('environments_config');
    instance.subscribe('messages/count');
  });

  instance.autorun(function () {
    let amountPerPage = instance.state.get('amountPerPage');
    let page = instance.state.get('page');
    let sortField = instance.state.get('sortField');
    let sortDirection = instance.state.get('sortDirection');

    Meteor.apply('messages/get?level&env&page&amountPerPage&sortField&sortDirection', [
      null, null, page, amountPerPage, sortField, sortDirection
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
Template.MessagesList.rendered = function() {
};  
*/

/*
 * Events
 */

Template.MessagesList.events({
  'click .sm-display-context-link': function (event, _instance) {
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

    });

  },

  'click .sm-scan-id-link': function (event, _instance) {
    event.preventDefault();
    let scanStartTimeStamp = moment(event.target.dataset.scanId).toDate();

    Meteor.apply('scansFind?start-timestamp-before', [
      scanStartTimeStamp
    ], {
      wait: false
    }, function (err, resp) {
      if (err) { 
        console.error(R.toString(err));
        return; 
      }

      if (R.isNil(resp.scan)) {
        console.error('error finding scan related to message', R.toString(scanStartTimeStamp));
        return;
      }

      Router.go('scanning-request', { 
        _id: idToStr(resp.scan._id)
      }, { 
        query: {
          env: idToStr(resp.environment._id),
          id: idToStr(resp.scan._id),
          action: 'view'
        } 
      });

    });
  },

  'click .sm-table-header': function (event, instance) {
    event.preventDefault();
    let isSortable = event.target.dataset.isSortable;
    if (! isSortable ) { return; }

    let sortField = event.target.dataset.sortField;
    let currentSortField = instance.state.get('sortField');
    let currentSortDirection = instance.state.get('sortDirection');

    if (sortField === currentSortField) {
      let sortDirection = null;
      if (currentSortDirection === null) {
        sortDirection = -1; 
      } else if (currentSortDirection === -1) {
        sortDirection = 1; 
      } else if (currentSortDirection === 1) {
        sortField = null;
        sortDirection = null;
      } else {
        sortField = null;
        sortDirection = null;
      }

      instance.state.set('sortField', sortField);
      instance.state.set('sortDirection', sortDirection);

    } else {
      instance.state.set('sortField', sortField);
      instance.state.set('sortDirection', -1);
    }
  },
});
   
/*  
 * Helpers
 */

Template.MessagesList.helpers({    
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
    return Counter.get(`messages/count`);
  },

  toIsoFormatStr: function (date) {
    if (R.isNil(date)) {
      return '';
    }

    let str = moment(date).format();
    return str;
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

  fieldSortClass: function (fieldName) {
    let instance = Template.instance();
    let classes = 'fa fa-sort';
    if (fieldName === instance.state.get('sortField')) {
      let sortDirection = instance.state.get('sortDirection');
      if (sortDirection === -1) {
        classes = 'fa fa-sort-desc';
      } else if (sortDirection === 1) {
        classes = 'fa fa-sort-asc';
      }
    }

    return classes; 
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
