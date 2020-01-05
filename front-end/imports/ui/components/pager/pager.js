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
 * Template Component: Pager 
 */

//import { Meteor } from 'meteor/meteor'; 
import * as R from 'ramda';
import { Template } from 'meteor/templating';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { ReactiveDict } from 'meteor/reactive-dict';

import './pager.html';

/*  
 * Lifecycles
 */

Template.Pager.onCreated(function () {
  var instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    pagesButtons: [{ label: '1', number: 1 }],
    currentPage: 1,
  });

  instance.autorun(function () {
    let data = Template.currentData();
    new SimpleSchema({
      disableNext: { type: Boolean },
      disablePrev: { type: Boolean },
      totalPages: { type: Number },
      currentPage: { type: Number },
      onReqNext: { type: Function },
      onReqPrev: { type: Function },
      onReqPage: { type: Function },
      onReqFirst: { type: Function },
      onReqLast: { type: Function },
    }).validate(data);

    instance.state.set('totalPages', data.totalPages);
    instance.state.set('currentPage', data.currentPage);
  });

  instance.autorun(function () {
    let numOfPagesInPager = 5;
    let totalPages = instance.state.get('totalPages');
    let currentPage = instance.state.get('currentPage');
    let first = R.ifElse((x) => x < 1, R.always(1), R.identity)(currentPage - numOfPagesInPager + 1);
    let last = R.ifElse((x) => x > totalPages, R.always(totalPages + 1), R.identity)(
      first + numOfPagesInPager);

    let pagesButtons = R.map((pageNumber) => {
      return {
        label: R.toString(pageNumber), number: pageNumber
      };
    }, R.range(first, last));

    instance.state.set('pagesButtons', pagesButtons);
  });
});

/*
Template.Pager.rendered = function() {
};  
*/

/*
 * Events
 */

Template.Pager.events({
  'click .sm-prev-button': function (_event, _instance) {
    if (_instance.state.get('totalPages') > 0) {
      let data = Template.currentData();
      data.onReqPrev();
    }
  },

  'click .sm-next-button': function (_event, _instance) {
    if (_instance.state.get('totalPages') > 0) {
      let data = Template.currentData();
      data.onReqNext();
    }
  },

  'click .sm-first-button': function (_event, _instance) {
    if (_instance.state.get('totalPages') > 0) {
      let data = Template.currentData();
      data.onReqFirst();
    }
  },

  'click .sm-last-button': function (_event, _instance) {
    if (_instance.state.get('totalPages') > 0) {
      let data = Template.currentData();
      data.onReqLast();
    }
  },

  'click .sm-page-button': function (event, _instance) {
    if (_instance.state.get('totalPages') > 0) {
      let data = Template.currentData();
      let pageNumber = parseInt(event.target.dataset.pageNumber);
      data.onReqPage(pageNumber);
    }
  },


});

/*  
 * Helpers
 */

Template.Pager.helpers({
  pagesButtons: function () {
    let instance = Template.instance();
    return instance.state.get('pagesButtons');
  },

  isCurrentPage: function (pageNum, currentPage) {
    return pageNum === currentPage;
  },
}); // end: helpers


