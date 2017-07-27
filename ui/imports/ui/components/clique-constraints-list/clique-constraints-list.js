/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: CliqueConstraintsList 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { CliqueConstraints } from '/imports/api/clique-constraints/clique-constraints';
import { Roles } from 'meteor/alanning:roles';
        
import './clique-constraints-list.html';     
    
/*  
 * Lifecycles
 */   
  
Template.CliqueConstraintsList.onCreated(function() {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
  });

  instance.autorun(function () {
    //let data = Template.currentData();
    
    var controller = Iron.controller();
    var params = controller.getParams();
    var query = params.query;

    new SimpleSchema({
    }).validate(query);

    instance.subscribe('clique_constraints');
  });
});  

/*
Template.CliqueConstraintsList.rendered = function() {
};  
*/

/*
 * Events
 */

Template.CliqueConstraintsList.events({
});
   
/*  
 * Helpers
 */

Template.CliqueConstraintsList.helpers({    
  cliqueConstraints: function () {
    //let instance = Template.instance();

    //var env = instance.state.get('env');
    //return Scans.find({ environment: env });
    return CliqueConstraints.find({}); 
  },

  isAuthManageCliqueConstraints: function () {
    return Roles.userIsInRole(Meteor.userId(), 'manage-clique-constraints', Roles.GLOBAL_GROUP); 
  },
}); /// end: helpers


