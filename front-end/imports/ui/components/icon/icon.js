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
 * Template Component: Icon 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
//import { ReactiveDict } from 'meteor/reactive-dict';
        
import './icon.html';     
    
/*  
 * Lifecycles
 */   
  
Template.Icon.onCreated(function() {
});  

/*
Template.Icon.rendered = function() {
};  
*/

/*
 * Events
 */

Template.Icon.events({
});
   
/*  
 * Helpers
 */

Template.Icon.helpers({    
  iconType: function (type, targetType) {
    return type === targetType;
  }
});


