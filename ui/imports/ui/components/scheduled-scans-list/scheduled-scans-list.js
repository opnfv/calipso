/*
 * Template Component: ScheduledScansList 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import * as R from 'ramda';
import { Counts } from 'meteor/tmeasday:publish-counts';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { ScheduledScans, 
  subsScheduledScansPageAmountSorted,
  subsScheduledScansPageAmountSortedCounter,
} from '/imports/api/scheduled-scans/scheduled-scans';
        
import '/imports/ui/components/pager/pager';

import './scheduled-scans-list.html';     
    
/*  
 * Lifecycles
 */   
  
Template.ScheduledScansList.onCreated(function() {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    env: null,
    page: 1,
    amountPerPage: 10,
    sortField: null,
    sortDirection: -1,
  });

  instance.autorun(function () {
    let data = Template.currentData();
    
    new SimpleSchema({
    }).validate(data);
  });

  instance.autorun(function () {
    let amountPerPage = instance.state.get('amountPerPage');
    let page = instance.state.get('page');
    let sortField = instance.state.get('sortField');
    let sortDirection = instance.state.get('sortDirection');

    instance.subscribe(subsScheduledScansPageAmountSorted, 
      page, amountPerPage, sortField, sortDirection);
  });
});  

/*
Template.ScheduledScansList.rendered = function() {
};  
*/

/*
 * Events
 */

Template.ScheduledScansList.events({
});
   
/*  
 * Helpers
 */

Template.ScheduledScansList.helpers({    
  scheduledScans: function () {
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

    return ScheduledScans.find({}, qParams); 
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
    let counterName = subsScheduledScansPageAmountSortedCounter;

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
}); // end: helpers


