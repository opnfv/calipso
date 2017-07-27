/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: ListInfoBox 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
//import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';
import { LocalCollection } from 'meteor/minimongo';
import { Icon } from '/imports/lib/icon';
        
import './list-info-box.html';     
    
/*  
 * Lifecycles
 */   
  
Template.ListInfoBox.onCreated(function() {
  let instance = this;
  instance.autorun(function () {
    let data = Template.currentData();
    new SimpleSchema({
      header: { type: String },
      list: { type: LocalCollection.Cursor, blackbox: true },
      icon: { type: Icon, blackbox: true },
      listItemFormat: {
        type: {
          getLabelFn: { type: Function },
          getValueFn: { type: Function },
        },
        blackbox: true
      },
      onItemSelected: { type: Function },

    }).validate(data);

  });
});  

/*
Template.ListInfoBox.rendered = function() {
};  
*/

/*
 * Events
 */

Template.ListInfoBox.events({
  'click .os-list-item'(event) {
    let instance = Template.instance();
    let val = event.target.attributes['data-value'].value;
    instance.data.onItemSelected(val);
  }
});
   
/*  
 * Helpers
 */

Template.ListInfoBox.helpers({    
  options: function (list, listItemFormat) {
    //let instance = Template.instance();

    let options = R.map((listItem) => {
      return { 
        label: listItemFormat.getLabelFn(listItem), 
        value: listItemFormat.getValueFn(listItem) 
      };
    }, list.fetch());

    return options;
  },

  itemsCount: function () {
    let instance = Template.instance();
    return instance.data.list.count();
  },

  argsSelect: function (list, listItemFormat) {
    let instance = Template.instance();

    let options = R.map((listItem) => {
      return { 
        label: listItemFormat.getLabelFn(listItem), 
        value: listItemFormat.getValueFn(listItem) 
      };
    }, list.fetch());

    return {
      values: [],
      options: options,
      showNullOption: true,
      nullOptionLabel: 'Select from dropdown',
      setModel: function (val) {
        instance.data.onItemSelected(val);
      },
    };
  }
});


