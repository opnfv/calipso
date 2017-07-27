/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { Meteor } from 'meteor/meteor';
//import { Counts } from 'meteor/tmeasday:publish-counts';
import { Counter } from 'meteor/natestrauser:publish-performant-counts';
import { Messages } from '../messages.js';
import * as R from 'ramda';

Meteor.publish('messages', function () {
  console.log('server subscribtion to: messages');
  //return Inventory.find({$where: 'this.id_path.match('^/WebEX-Mirantis@Cisco/')'});
  //return Inventory.find({ 'show_in_tree': true });
  return Messages.find({});
});

Meteor.publish('messages?_id', function (_id) {
  console.log('server subscribtion to: messages?_id');
  console.log('_id', _id);

  let query = { _id: _id };
  return Messages.find(query);
});

Meteor.publish('messages?level', function (level) {
  var query = {
    level: level
  };

  /*
  var counterName = 'messages?level!counter?' +
    'level=' + level;

  console.log('server subscription to: ' + counterName);
  Counts.publish(this, counterName, Messages.find(query));
  */

  console.log('server subscribtion to: messages?level');
  console.log('- level: ' + level);
  return Messages.find(query);
});

Meteor.publish('messages?env+level', function (env, level) {
  var query = {
    environment: env,
    level: level
  };
  /*
  var counterName = 'messages?env+level!counter?env=' +
    env + '&level=' + level;

  console.log('server subscription to: messages - counter');
  console.log(' - name: ' + counterName);
  Counts.publish(this, counterName, Messages.find(query));
  */

  console.log('server subscribtion to: messages');
  console.log('- env: ' + env);
  console.log('- level: ' + level);
  return Messages.find(query);
});

Meteor.publish('messages/count', function () {
  const counterName = `messages/count`; 
  console.log(`subscribe - counter: ${counterName}`);

  return new Counter(counterName, Messages.find({ }));
});

Meteor.publish('messages/count?env', function (env) {
  const counterName = `messages/count?env`; 
  console.log(`subscribe - counter: ${counterName}`);

  let query = {};
  query = R.ifElse(R.isNil, R.always(query), R.assoc('environment', R.__, query))(env);
  return new Counter(counterName, Messages.find(query));
});

Meteor.publish('messages/count?level', function (level) {
  const counterName = `messages/count?level=${level}`; 
  console.log(`subscribe - counter: ${counterName}`);

  return new Counter(counterName, Messages.find({ level: level }));
});

Meteor.publish('messages/count?level&env', function (level, env) {
  const counterName = `messages/count?level=${level}&env=${env}`; 
  console.log(`subscribe - counter: ${counterName}`);

  let query = { level: level };
  query = R.ifElse(R.isNil, R.always(query), R.assoc('environment', R.__, query))(env);

  return new Counter(counterName, Messages.find(query)); });
