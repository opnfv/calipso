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
 * Template Component: SelectableOrderedInput 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';
        
import './selectable-ordered-input.html';     
    
/*  
 * Lifecycles
 */   
  
Template.SelectableOrderedInput.onCreated(function() {
  let instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    choices: [],
    currentChoices: [],
    currentProduct: [],
    selectedChoice: null,
    selectedProductOption: null,
  });

  instance.autorun(function () {
    let data = Template.currentData();

    new SimpleSchema({
      choices: { type: [Object], blackbox: true },
      product: { type: [Object], blackbox: true },
      onProductChange: { type: Function },
    }).validate(data);

    instance.state.set('choices', data.choices);
    instance.state.set('product', data.product);
    instance.onProductChange = R.defaultTo((_x) => {}, data.onProductChange);
  });

  instance.autorun(function () {
    let choices = instance.state.get('choices');
    let product = instance.state.get('product');

    let currentChoices = R.differenceWith((choice, product) => choice.value === product.value, 
      choices, product);

    instance.state.set('currentChoices', currentChoices);
    instance.state.set('currentProduct', product);
    instance.state.set('selectedChoice', null);
    instance.state.set('selectedProductOption', null);
  });

  let lastCurrentProduct = null;
  instance.autorun(function () {
    let currentProduct = instance.state.get('currentProduct');
    if (R.isNil(lastCurrentProduct)) {
      lastCurrentProduct = currentProduct;
      return;
    }

    if (R.equals(lastCurrentProduct, currentProduct)) {
      return; 
    }

    lastCurrentProduct = currentProduct;
    instance.onProductChange(currentProduct);
  });

});  

/*
Template.SelectableOrderedInput.rendered = function() {
};  
*/

/*
 * Events
 */

Template.SelectableOrderedInput.events({
  'click .sm-add-choice-btn': function (event, instance) {
    event.preventDefault();

    moveSelectedChoiceToProduct(instance);
  },

  'click .sm-remove-choice-btn': function (event, instance) {
    event.preventDefault();

    moveSelectedProductOptionToChoices(instance);
  },

  'click .sm-move-up-product-btn': function (event, instance) {
    event.preventDefault();

    moveSelectedProductOptionUp(instance); 
  },

  'click .sm-move-down-product-btn': function (event, instance) {
    event.preventDefault();

    moveSelectedProductOptionDown(instance); 
  },
});
   
/*  
 * Helpers
 */

Template.SelectableOrderedInput.helpers({    
  argsChoicesSelect: function (choices, selectedValue) {
    let instance = Template.instance();

    return {
      classStr: 'cl-input',
      //isDisabled:,
      selectedValue: selectedValue,
      size: 7,
      options: choices,
      onInput: {
        fn: function (choice) {
          let choices = instance.state.get('currentChoices');
          let fullChoice = R.find(R.propEq('value', choice), choices); 
          instance.state.set('selectedChoice', fullChoice);
        }
      },
    };
  },

  currentChoices: function () {
    let instance = Template.instance();
    return instance.state.get('currentChoices');
  },

  argsProductSelect: function (currentProduct, selectedProductOptValue) {
    let instance = Template.instance();

    return {
      classStr: 'cl-input',
      //isDisabled:,
      selectedValue: selectedProductOptValue,
      size: 7,
      options: currentProduct,
      onInput: {
        fn: function (productOption) {
          let product = instance.state.get('currentProduct');
          let fullProductOption = R.find(R.propEq('value', productOption), product); 
          instance.state.set('selectedProductOption', fullProductOption);
        }
      },
    };
  },

  currentProduct: function () {
    let instance = Template.instance();
    return instance.state.get('currentProduct');
  },

  selectedChoiceValue: function () {
    let instance = Template.instance();
    return R.path(['value'], instance.state.get('selectedChoice'));
  },

  selectedProductOptValue: function () {
    let instance = Template.instance();
    return R.path(['value'], instance.state.get('selectedProductOption'));
  },
}); // end: helpers

function moveSelectedChoiceToProduct(instance) {
  let selectedChoice = instance.state.get('selectedChoice');
  if (R.isNil(selectedChoice)) { return; }

  // remove selected choice from choices.
  let choices = instance.state.get('currentChoices');
  choices = R.reject(R.propEq('value', selectedChoice.value), choices);
  instance.state.set('currentChoices', choices);
  
  // add selected choice to product.
  let product = instance.state.get('currentProduct');
  product = R.append(selectedChoice, product);
  instance.state.set('currentProduct', product);

  // clear selected choice
  instance.state.set('selectedChoice', null);
}

function moveSelectedProductOptionToChoices(instance) {
  let selectedProductOption = instance.state.get('selectedProductOption');
  if (R.isNil(selectedProductOption)) { return; }

  // remove selected option from product
  let product = instance.state.get('currentProduct');
  product = R.reject(R.propEq('value', selectedProductOption.value), product);
  instance.state.set('currentProduct', product);

  // add selected option to choices
  let choices = instance.state.get('currentChoices');
  choices = R.append(selectedProductOption, choices);
  instance.state.set('currentChoices', choices);

  // clear selection product option
  instance.state.set('selectedProductOption', null);
}

function moveSelectedProductOptionUp(instance) {
  // get selected product option. exit if null.
  let selectedProductOption = instance.state.get('selectedProductOption');
  if (R.isNil(selectedProductOption)) { return; }

  // move product option up.
  let product = instance.state.get('currentProduct');
  let index = R.findIndex(R.propEq('value', selectedProductOption.value), product);
  if (index === 0) { return; }
  product = R.remove(index, 1, product);
  product = R.insert(index - 1, selectedProductOption, product);
  instance.state.set('currentProduct', product);
}

function moveSelectedProductOptionDown(instance) {
  // get selected product option. exit if null.
  let selectedProductOption = instance.state.get('selectedProductOption');
  if (R.isNil(selectedProductOption)) { return; }

  // move product option down.
  let product = instance.state.get('currentProduct');
  let index = R.findIndex(R.propEq('value', selectedProductOption.value), product);
  if (index === product.length - 1) { return; }

  product = R.remove(index, 1, product);
  product = R.insert(index + 1, selectedProductOption, product);
  instance.state.set('currentProduct', product);
}
