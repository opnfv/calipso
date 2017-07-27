/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: LinkTypesList 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import * as R from 'ramda';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { LinkTypes } from '/imports/api/link-types/link-types';
import { Roles } from 'meteor/alanning:roles';
        
import './link-types-list.html';     
    
/*  
 * Lifecycles
 */   
  
Template.LinkTypesList.onCreated(function() {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    env: null
  });

  instance.autorun(function () {


    //let data = Template.currentData();
    
    var controller = Iron.controller();
    var params = controller.getParams();
    var query = params.query;

    new SimpleSchema({
      env: { type: String, optional: true },
    }).validate(query);

    let env = query.env;
    if (R.isNil(env)) {
      instance.state.set('env', null);
    } else {
      instance.state.set('env', env);
    }

    instance.subscribe('link_types?env*', env);
  });
});  

/*
Template.LinkTypesList.rendered = function() {
};  
*/

/*
 * Events
 */

Template.LinkTypesList.events({
});
   
/*  
 * Helpers
 */

Template.LinkTypesList.helpers({    
  linkTypes: function () {
    //let instance = Template.instance();

    //var env = instance.state.get('env');
    //return Scans.find({ environment: env });
    return LinkTypes.find({}); 
  },

  isAuthManageLinkTypes: function () {
    return Roles.userIsInRole(Meteor.userId(), 'manage-link-types', Roles.GLOBAL_GROUP); 
  },
}); // end - helpers
