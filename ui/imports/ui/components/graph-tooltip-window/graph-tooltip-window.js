/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: GraphTooltipWindow 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
//import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { store } from '/imports/ui/store/store';
import { closeGraphTooltipWindow } from '/imports/ui/actions/graph-tooltip-window.actions';
        
import './graph-tooltip-window.html';     
    
/*  
 * Lifecycles
 */   
  
Template.GraphTooltipWindow.onCreated(function() {
  let instance = this;

  instance.autorun(() => {
    new SimpleSchema({
      label: { type: String },
      title: { type: String },
      left: { type: Number },
      top: { type: Number },
      show: { type: Boolean }
    }).validate(Template.currentData());
  });
});  

/*
Template.GraphTooltipWindow.rendered = function() {
};  
*/

/*
 * Events
 */

Template.GraphTooltipWindow.events({
  'mouseout .os-graph-tooltip-window': function(_e, _instance) {
    /*
    if (!instance.data.show) { return; }

    e.preventDefault();
    e.stopPropagation();
    store.dispatch(closeGraphTooltipWindow());
    */
  },

  'click .os-graph-tooltip-window': function(e, instance) {
    if (!instance.data.show) { return; }

    e.preventDefault();
    e.stopPropagation();
    store.dispatch(closeGraphTooltipWindow());
  },
});
   
/*  
 * Helpers
 */

Template.GraphTooltipWindow.helpers({    
});


