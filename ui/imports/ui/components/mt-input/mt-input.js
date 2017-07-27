/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: MtInput 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';
//import { ReactiveDict } from 'meteor/reactive-dict';
        
import './mt-input.html';     
    
/*  
 * Lifecycles
 */   
  
Template.MtInput.onCreated(function() {
  let instance = this;

  instance.autorun(function () {
    let data = Template.currentData();

    //simple schema does not support input value type of: number or string together.
    data = R.dissoc('inputValue', data);
    
    instance.autorun(function () {
      new SimpleSchema({
        inputType: { type: String }, 
        classStr: { type: String, optional: true },
        placeholder: { type: String, optional: true },
        isDisabled: { type: Boolean, optional: true },
        onInput: { type: Object, blackbox: true },
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
Template.MtInput.rendered = function() {
};  
*/

/*
 * Events
 */

Template.MtInput.events({
  'input .input-field': function (event, instance) {
    if (event.target.type === 'checkbox') { return; }
    
    let value = R.cond([
      [R.equals('number'), R.always(event.target.valueAsNumber)],
      [R.T, R.always(event.target.value)],
    ])(event.target.type);
    
    instance.onInput(value);
  },

  'click .input-field': function (event, instance) {
    if (event.target.type !== 'checkbox') { return; }

    let element = instance.$('.input-field')[0];
    instance.onInput(element.checked);
  }
});
   
/*  
 * Helpers
 */

Template.MtInput.helpers({    
  attrsInput: function (inputType, placeholder, isDisabled) {
    let attrs = {};

    if (hasPlaceholder(inputType, placeholder)) {
      attrs = R.assoc('placeholder', placeholder, attrs);
    }

    if (isDisabled) {
      attrs = R.assoc('disabled', 'disabled', attrs);
    }

    return attrs;
  },

}); // end: helpers

function hasPlaceholder(inputType, placeholder) {
  if (R.contains(inputType, ['checkbox', 'select'])) {
    return false;
  }

  if (R.isNil(placeholder)) {
    return false;
  }

  return true;
}
