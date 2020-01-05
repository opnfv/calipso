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
 * Template Component: NetworkInfoBox 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { regexEscape } from '/imports/lib/regex-utils';
import { Inventory } from '/imports/api/inventories/inventories';
        
import './network-info-box.html';     
    
/*  
 * Lifecycles
 */   
  
Template.NetworkInfoBox.onCreated(function() {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    portsCount: 0
  });

  instance.autorun(function () {
    let network = instance.data.network;
    instance.subscribe('inventory?id_path_like&type', network.id_path, 'port');

    let idPathExp = new RegExp(regexEscape(network.id));
    instance.state.set('portsCount', Inventory.find({ 
      id_path: idPathExp,
      type: 'port'
    }).count());
  });

});  

/*
Template.NetworkInfoBox.rendered = function() {
};  
*/

/*
 * Events
 */

Template.NetworkInfoBox.events({
});
   
/*  
 * Helpers
 */

Template.NetworkInfoBox.helpers({    
  portsCount: function () {
    let instance = Template.instance();
    return instance.state.get('portsCount');
  }
});


