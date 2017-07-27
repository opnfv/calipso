/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { Meteor } from 'meteor/meteor';
import { Links } from '../links.js';

Meteor.publish('links', function () {
  console.log('server subscribtion to: links');
  //return Inventory.find({$where: 'this.id_path.match('^/WebEX-Mirantis@Cisco/')'});
  return Links.find({});
});

Meteor.publish('links?_id-in', function (idsList) {
  var query = {
    _id: { $in: idsList}
  };
/*
  var counterName = 'inventory?env+type!counter?env=' + env + '&type=' + type;

  console.log('server subscribing to counter: ' + counterName);
  Counts.publish(this, counterName, Inventory.find(query));
*/

  console.log('server subscribtion to: links?_id-in');
  console.log('- _id-in: ' + idsList);
  return Links.find(query); 
});
