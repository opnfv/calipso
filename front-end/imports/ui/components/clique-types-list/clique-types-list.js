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
 * Template Component: CliqueTypesList 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { CliqueTypes } from '/imports/api/clique-types/clique-types';
import { Roles } from 'meteor/alanning:roles';
import * as R from 'ramda';
        
import './clique-types-list.html';     
    
/*  
 * Lifecycles
 */   
  
Template.CliqueTypesList.onCreated(function() {
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
    instance.state.set('env', env);

    instance.subscribe('clique_types?env*', env);
  });
});  

/*
Template.CliqueTypesList.rendered = function() {
};  
*/

/*
 * Events
 */

Template.CliqueTypesList.events({
});
   
/*  
 * Helpers
 */

Template.CliqueTypesList.helpers({    
  cliqueTypes: function () {
    //let instance = Template.instance();

    //var env = instance.state.get('env');
    //return Scans.find({ environment: env });
    let cliqueTypes = CliqueTypes.find({}).fetch();
    let [anyTypes, specificTypes] = R.partition((ct) => {
      return R.prop('environment', ct) === "ANY"
    }, cliqueTypes);
    return R.concat(specificTypes, anyTypes);
  },

  isManageable: function(cliqueType) {
      return Roles.userIsInRole(Meteor.userId(), 'manage-clique-types', Roles.GLOBAL_GROUP)
             && R.prop('environment', cliqueType) !== 'ANY';
  }
});


