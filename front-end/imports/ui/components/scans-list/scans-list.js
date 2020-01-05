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
 * Template Component: ScansList 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import * as R from 'ramda';
import { Counts } from 'meteor/tmeasday:publish-counts';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { Scans, 
  subsScansEnvPageAmountSorted,
  subsScansEnvPageAmountSortedCounter,
} from '/imports/api/scans/scans';
        
import '/imports/ui/components/pager/pager';

import './scans-list.html';     
    
/*  
 * Lifecycles
 */   
  
Template.ScansList.onCreated(function() {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    env: null,
    page: 1,
    amountPerPage: 10,
    sortField: 'submit_timestamp',
    sortDirection: -1,
  });

  instance.autorun(function () {
    //let data = Template.currentData();
    
    var controller = Iron.controller();
    var params = controller.getParams();
    var query = params.query;

    new SimpleSchema({
      env: { type: String, optional: true },
    }).validate(query);

    let env = query.env;
    if (R.isNil(env)) {
      instance.state.set('env', null);
    } else {
      instance.state.set('env', env);
    }

  });

  instance.autorun(function () {
    let env = instance.state.get('env');
    let amountPerPage = instance.state.get('amountPerPage');
    let page = instance.state.get('page');
    let sortField = instance.state.get('sortField');
    let sortDirection = instance.state.get('sortDirection');

    instance.subscribe(subsScansEnvPageAmountSorted, 
      env, page, amountPerPage, sortField, sortDirection);

  });

});  

/*
Template.ScansList.rendered = function() {
};  
*/

/*
 * Events
 */

Template.ScansList.events({
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

Template.ScansList.helpers({    
  scans: function () {
    let instance = Template.instance();
    let page = instance.state.get('page');
    let amountPerPage = instance.state.get('amountPerPage');
    let sortField = instance.state.get('sortField');
    let sortDirection = instance.state.get('sortDirection');

    let skip = (page - 1) * amountPerPage;
    let sortParams = {};
    sortParams = R.ifElse(R.isNil, R.always(sortParams), 
      R.assoc(R.__, sortDirection, sortParams))(sortField);

    let qParams = {
      limit: amountPerPage,
      skip: skip,
      sort: sortParams,
    };

    return Scans.find({}, qParams); 
  },

  currentPage: function () {
    let instance = Template.instance();
    return instance.state.get('page');
  },

  amountPerPage: function () {
    let instance = Template.instance();
    return instance.state.get('amountPerPage');
  },

  totalItems: function () {
    //let instance = Template.instance();
    //let page = instance.state.get('page');
    //let amountPerPage = instance.state.get('amountPerPage');
    let counterName = subsScansEnvPageAmountSortedCounter;

    return Counts.get(counterName);
  },

  argsPager: function (currentPage, amountPerPage, totalItems) {
    let instance = Template.instance();
    let totalPages = Math.ceil(totalItems / amountPerPage);

    return {
      disableNext: currentPage * amountPerPage > totalItems,
      disablePrev: currentPage == 1,
      totalPages: totalPages,      
      currentPage: currentPage,
      onReqNext: function () {
        console.log('next');
        let page = (currentPage * amountPerPage > totalItems) ? currentPage : currentPage + 1;
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
        } else if (pageNumber > Math.ceil(totalItems / amountPerPage)) { 
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
});

