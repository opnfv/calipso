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
 * Template Component: MtSelect 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';
//import { ReactiveDict } from 'meteor/reactive-dict';
        
import './mt-select.html';     
    
/*  
 * Lifecycles
 */   
  
Template.MtSelect.onCreated(function() {
  let instance = this;

  instance.autorun(function () {
    let data = Template.currentData();

    instance.autorun(function () {
      new SimpleSchema({
        classStr: { type: String, optional: true },
        selectedValue: { type: String, optional: true },
        isDisabled: { type: Boolean, optional: true },
        options: { type: [Object], blackbox: true },
        onInput: { type: Object, blackbox: true },
        size: { type: Number, optional: true },
      }).validate(data);
    });
  });

  instance.autorun(function () {
    let data = Template.currentData();

    instance.onInput = function (value) {
      R.when(R.pipe(R.isNil, R.not), x => x(value))(R.path(['onInput', 'fn'], data));    
    };
  });
});  

/*
Template.MtSelect.rendered = function() {
};  
*/

/*
 * Events
 */

Template.MtSelect.events({
  'change .sm-mt-select': function (event, instance) {
    event.preventDefault();
    event.stopPropagation();

    let value = R.pipe(R.head, R.prop('value'))(event.target.selectedOptions);
    instance.onInput(value);
  },
});
   
/*  
 * Helpers
 */

Template.MtSelect.helpers({    
  attrsSelect: function (isDisabled, size) {
    let attrs = {};
    if (isDisabled) {
      attrs = R.assoc('disabled', 'disabled', attrs);
    }

    if (size) {
      attrs = R.assoc('size', size, attrs);
    }

    return attrs;
  },

  attrOptSelected: function (currentValue, selectedValue) {
    let attrs = {};
    if (currentValue === selectedValue) {
      attrs = R.assoc('selected', 'selected', attrs);
    }
    return attrs;
  },

}); // helpers


