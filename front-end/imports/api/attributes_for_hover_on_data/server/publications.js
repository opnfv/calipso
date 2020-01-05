///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import { Meteor } from 'meteor/meteor';

import { NodeHoverAttr } from '../attributes_for_hover_on_data.js';

Meteor.publish('attributes_for_hover_on_data', function () {
  console.log('server subscribtion to: attributes_for_hover_on_data');
  //return Inventory.find({$where: 'this.id_path.match('^/WebEX-Mirantis@Cisco/')'});
  return NodeHoverAttr.find({});
});

Meteor.publish('attributes_for_hover_on_data?type', function (type) {
  console.log('server subscribtion to: attributes_for_hover_on_data?type');
  console.log('- type: ' + type);

  //return Inventory.find({$where: 'this.id_path.match('^/WebEX-Mirantis@Cisco/')'});
  return NodeHoverAttr.find({ 'type': type});
});
