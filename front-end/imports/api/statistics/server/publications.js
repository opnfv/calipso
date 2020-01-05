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
//import { Counts } from 'meteor/tmeasday:publish-counts';
import { Statistics } from '../statistics.js';
import { createGraphQuerySchema } from '../helpers';

Meteor.publish('statistics!graph-frames', function ({
  env, 
  object_id, 
  type,
  flowType, 
  timeStart,
  sourceMacAddress,
  destinationMacAddress,
  sourceIPv4Address,
  destinationIPv4Address
}) {
  console.log('server subscribe: statistics?graph-frames');

  let schema = createGraphQuerySchema(
    env, 
    object_id,
    type,
    flowType, 
    timeStart,
    null,
    sourceMacAddress,
    destinationMacAddress,
    sourceIPv4Address,
    destinationIPv4Address);

  console.log('statistics!graph-frames');
  console.log(`- env: ${env}`);
  console.log(`- object_id: ${object_id}`);
  console.log(`- type: ${type}`);
  console.log(`- flowType: ${flowType}`);
  console.log(`- timeStart: ${timeStart}`);
  console.log(`- sourceMacAddress: ${sourceMacAddress}`);
  console.log(`- destinationMacAddress: ${destinationMacAddress}`);
  console.log(`- sourceIPv4Address: ${sourceIPv4Address}`);
  console.log(`- destinationIPv4Address: ${destinationIPv4Address}`);

  return Statistics.find(schema);
});

