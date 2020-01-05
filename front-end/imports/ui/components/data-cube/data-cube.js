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
 * Template Component: DataCube
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import * as R from 'ramda';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { Icon } from '/imports/lib/icon';
        
import './data-cube.html';     
    
/*  
 * Lifecycles
 */   
  
Template.DataCube.onCreated(function() {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    theme: null
  });

  this.autorun(() => {
    new SimpleSchema({
      header: { type: String },
      dataInfo: { type: String },
      icon: { type: Icon },
      theme: { type: String, optional: true }
    }).validate(Template.currentData());

    let theme = Template.currentData().theme;
    theme = R.isNil(theme) ? 'light' : theme; 
    instance.state.set('theme', theme);
  });
});  

/*
Template.DataCube.rendered = function() {
};  
*/

/*
 * Events
 */

Template.DataCube.events({
});
   
/*  
 * Helpers
 */

Template.DataCube.helpers({    
  getTheme: function () {
    let instance = Template.instance();
    return instance.state.get('theme');
  }
});


