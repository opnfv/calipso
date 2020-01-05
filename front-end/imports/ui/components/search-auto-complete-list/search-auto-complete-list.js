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
 * Template Component: SearchAutoCompleteList 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import * as R from 'ramda';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { ReactiveVar } from 'meteor/reactive-var';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { EJSON } from 'meteor/ejson';
import { _idFieldDef } from '/imports/lib/simple-schema-utils';
        
//import { store } from '/imports/ui/store/store';

import '../auto-search-result-line/auto-search-result-line';

import './search-auto-complete-list.html';     
    
/*  
 * Lifecycles
 */   
  
Template.SearchAutoCompleteList.onCreated(function() {
  let instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    isOpen: false,
    envId: null,
    searchTerm: null,
    results: [],
  });

  instance.currentData = new ReactiveVar(null, EJSON.equals);
  instance.autorun((function(_this) {
    return function(_computation) {
      return _this.currentData.set(Template.currentData());
    };
  })(instance));

  instance.autorun(function () {
    let data = instance.currentData.get();

    new SimpleSchema({
      isOpen: { type: Boolean },
      envId: R.merge(_idFieldDef, { optional: true }), 
      searchTerm: { type: String, optional: true },
      onResultSelected: { type: Function },
      onCloseReq: { type: Function }, 
    }).validate(data);

    instance.state.set('isOpen', data.isOpen);
    instance.state.set('envId', data.envId);
    instance.state.set('searchTerm', data.searchTerm);
    
    instance.onCloseReq = R.defaultTo(() => console.log('close requested'), data.onCloseReq);
  });

  instance.opCounter = 0;

  instance.autorun(function () {
    let envId = instance.state.get('envId');
    let searchTerm = instance.state.get('searchTerm');
    performSearch(searchTerm, envId,
      function getLastOpCounter() {
        return instance.opCounter;
      },
      function setLastOpCounter(opCounter) {
        instance.opCounter = opCounter;
      }
    ).then(function (results) {
      instance.state.set('results', results);
    });
  });

});  

/*
Template.SearchAutoCompleteList.rendered = function() {
};  
*/

Template.SearchAutoCompleteList.onDestroyed(() => {
});

/*
 * Events
 */

Template.SearchAutoCompleteList.events({
  'click .sm-backdrop': function (event, instance) {
    instance.onCloseReq();
  }
}); // end - events
   
/*  
 * Helpers
 */

Template.SearchAutoCompleteList.helpers({    
  searchResults: function () {
    let instance = Template.instance();
    return instance.state.get('results');
  },

  createAutoSearchResultLineArgs: function (resultItem) {
    let instance = Template.instance();

    return {
      namePath: resultItem.name_path,
      objectName: resultItem.object_name,
      objectType: resultItem.type,
      environment: resultItem.environment,
      onClick() {
        instance.data.onResultSelected(resultItem); 
      }
    };
  },

}); // end - helpers

function performSearch(
  searchTerm, 
  envId, 
  getLastOpCounterFn, 
  setLastOpCounterFn
) {
  return new Promise((resolve, reject) => {
    let results = [];
    let opCounter = getLastOpCounterFn() + 1;
    setLastOpCounterFn(opCounter);

    Meteor.apply('inventorySearch', [ 
      searchTerm, envId, opCounter, 
    ], { 
      wait: false 
    }, function (err, res) {
      if (err) {
        console.error(R.toString(err));
        reject(err);
        return;
      }

      let currentOpCounter = getLastOpCounterFn();
      if (res.opCounter !== currentOpCounter) {
        reject('stale search result');
        return;
      }
       
      R.forEach((resultItem) => {
        results = R.append(resultItem, results);
      }, res.searchResults);

      resolve(results);
      return;
    });
  });
}
