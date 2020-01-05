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
 * Template Component: MtRadios 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
//import { ReactiveDict } from 'meteor/reactive-dict';
import * as R from 'ramda';
        
import './mt-radios.html';     
    
/*  
 * Lifecycles
 */   
  
Template.MtRadios.onCreated(function() {
  let instance = this;

  instance.autorun(function () {
    let data = Template.currentData();

    instance.onInput = function (value) {
      R.when(R.pipe(R.isNil, R.not), x => x(value))(R.path(['onInput', 'fn'], data));    
    };
  });
});  

/*
Template.MtRadios.rendered = function() {
};  
*/

/*
 * Events
 */

Template.MtRadios.events({
  'click .cl-mt-radio-input': function (event, instance) {
    event.preventDefault();
    event.stopPropagation();

    instance.onInput(event.target.value); 
  },
});
   
/*  
 * Helpers
 */

Template.MtRadios.helpers({    
  attrsInput: function (inputValue, selectedValue) {
    let attrs = {};

    if (inputValue === selectedValue) {
      attrs = R.assoc('checked', 'checked', attrs);
    }

    return attrs;
  },
}); // end: helpers


