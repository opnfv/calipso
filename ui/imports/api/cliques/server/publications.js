/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { Meteor } from 'meteor/meteor';

import { Cliques } from '../cliques.js';

Meteor.publish('cliques', function () {
  console.log('server subscribtion to: cliques');
  //return Inventory.find({$where: 'this.id_path.match('^/WebEX-Mirantis@Cisco/')'});
  return Cliques.find({});
});

Meteor.publish('cliques?focal_point', function (objId) {
  var query = {
    focal_point: new Mongo.ObjectID(objId) 
  };
/*
  var counterName = 'inventory?env+type!counter?env=' + env + '&type=' + type;

  console.log('server subscribing to counter: ' + counterName);
  Counts.publish(this, counterName, Inventory.find(query));
*/

  console.log('server subscribtion to: cliques?focal_point');
  console.log('- focal_point: ' + objId);
  return Cliques.find(query); 
});
