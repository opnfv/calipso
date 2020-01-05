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
 * Template Component: AutoSearchResultLine 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
//import { ReactiveDict } from 'meteor/reactive-dict';
        
import './auto-search-result-line.html';     
    
/*  
 * Lifecycles
 */   
  
Template.AutoSearchResultLine.onCreated(function() {
});  

/*
Template.AutoSearchResultLine.rendered = function() {
};  
*/

/*
 * Events
 */

Template.AutoSearchResultLine.events({
  'click': function(event, instance) {
    event.stopPropagation();
    event.preventDefault();

    instance.data.onClick(instance.data.namePath);
  }
});
   
/*  
 * Helpers
 */

Template.AutoSearchResultLine.helpers({    
});


