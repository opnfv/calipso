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
 * Template Component: EnvironmentBox 
 */

import { Template } from 'meteor/templating';

import '/imports/ui/components/environment-box-first-section/environment-box-regions';
import '/imports/ui/components/environment-box-first-section/environment-box-networks';
import '/imports/ui/components/environment-box-first-section/environment-box-projects';
import '/imports/ui/components/environment-box-first-section/environment-box-hosts';
import '/imports/ui/components/environment-box-first-section/environment-box-namespaces';

import './environment-box.html';     
    
/*  
 * Lifecycles
 */   
  
Template.EnvironmentBox.onCreated(function() {
});  

/*
Template.EnvironmentBox.rendered = function() {
};  
*/

/*
 * Events
 */

Template.EnvironmentBox.events({
});
   
/*  
 * Helpers
 */

Template.EnvironmentBox.helpers({
    equals: function(item, value) {
        return item === value;
    },

    assoc: function() {
        let results = {};
        for (let i = 0; i < arguments.length; i += 2) {
            if (arguments[i + 1]) {
                results[arguments[i]] = arguments[i + 1];
            }
        }
        return results;
    }
}); // end: helpers
