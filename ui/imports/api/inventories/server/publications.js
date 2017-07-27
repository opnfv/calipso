/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { Meteor } from 'meteor/meteor';
import { Counts } from 'meteor/tmeasday:publish-counts';
import { check } from 'meteor/check';
import * as R from 'ramda';

import { Inventory } from '../inventories.js';
import { regexEscape } from '/imports/lib/regex-utils';

Meteor.publish('inventory', function () {
  console.log('server subscribtion to: inventory');
    //return Inventory.find({$where: 'this.id_path.match('^/WebEX-Mirantis@Cisco/')'});
    //return Inventory.find({ 'show_in_tree': true });
  return Inventory.find({});
});

Meteor.publish('inventory?_id', function (_id) {
  console.log('server subscribtion to: inventory?_id');
  console.log('_id:', R.toString(_id));

  return Inventory.find({ _id: _id });
});

Meteor.publish('inventory?id', function (id) {
  console.log('server subscribtion to: inventory?id');
  return Inventory.find({id: id});
});

Meteor.publish('inventory?env&id', function (env, id) {
  console.log('server subscribtion to: inventory?env&id');
  console.log(`-env: ${R.toString(env)}`);
  console.log(`-id: ${R.toString(id)}`);

  return Inventory.find({environment: env, id: id});
});

Meteor.publish('inventory?id_path', function (id_path) {
  console.log('server subscribtion to: inventory?id_path');
  return Inventory.find({id_path: id_path});
});

Meteor.publish('inventory?name&env&type', function (name, env, type) {
  console.log('server subscribtion to: inventory?name&env&type');
  console.log('-name:', R.toString(name));
  console.log('-env:', R.toString(env));
  console.log('-type:', R.toString(type));

  let query = {
    name: name,
    environment: env,
    type: type
  };

  console.log('query', R.toString(query));
  return Inventory.find(query);
});

Meteor.publish('inventory?_id-in', function (idsList) {
  var query = {
    _id: { $in: idsList }
  };
  /*
    var counterName = 'inventory?env+type!counter?env=' + env + '&type=' + type;

    console.log('server subscribing to counter: ' + counterName);
    Counts.publish(this, counterName, Inventory.find(query));
  */
  console.log('server subscribtion to: inventory?_id-in');
  console.log('- id-in: ' + idsList);

  return Inventory.find(query); 
});

Meteor.publish('inventory?env+type', function (env, type) {
  var query = {
    environment: env,
    type: type
  };
  var counterName = 'inventory?env+type!counter?env=' + env + '&type=' + type;

  console.log('server subscribing to counter: ' + counterName);
  Counts.publish(this, counterName, Inventory.find(query));

  console.log('server subscribtion to: inventory-by-env-and-type');
  console.log('-env: ' + env);
  console.log('-type: ' + type);

  return Inventory.find(query); 
});

Meteor.publish('inventory?env&binding:host_id&type', function (env, host_id, type) {
  var query = {
    environment: env,
    'binding:host_id': host_id,
    type: type
  };
  console.log('server subscribtion to: inventory?env&binding:host_id&type');
  console.log('-env: ' + env);
  console.log('-binding:host_id: ' + host_id);
  console.log('-type: ' + type);

  return Inventory.find(query); 
});

Meteor.publish('inventory?env+name', function (env, name) {
  var query = {
    name: name,
    environment: env
  };

  console.log('server subscribtion to: inventory?env+name');
  console.log('- name: ' + name);
  console.log('- env: ' + env);

  return Inventory.find(query); 
});

Meteor.publish('inventory?type+host', function (type, host) {
  var query = {
    type: type,
    host: host
  };
/*
  var counterName = 'inventory?env+type!counter?env=' + env + '&type=' + type;

  console.log('server subscribing to counter: ' + counterName);
  Counts.publish(this, counterName, Inventory.find(query));
*/

  console.log('server subscribtion to: inventory?type+host');
  console.log('- type: ' + type);
  console.log('- host: ' + host);
  return Inventory.find(query); 
});

Meteor.publish('inventory?id_path_start&type', function (id_path, type) {
  check(id_path, String);
  check(type, String);

  let idPathExp = new RegExp(`^${regexEscape(id_path)}`);

  let query = {
    id_path: idPathExp,
    type: type
  };

  var counterName = 'inventory?id_path_start&type!counter?id_path_start=' + 
    id_path + '&type=' + type;

  console.log('server subscribing to counter: ' + counterName);
  Counts.publish(this, counterName, Inventory.find(query));

  console.log('server subscribtion to: inventory?id_path_start&type');
  console.log('-id_path_start: ' + id_path);
  console.log('-type: ' + type);
  return Inventory.find(query);
});


Meteor.publish('inventory.children', function (id, type, name, env) {
  console.log('server subscribtion to: inventory.children');
  console.log('node id: ' + R.toString(id));
  console.log('node type: ' + R.toString(type));
  console.log('node name: ' + R.toString(name));
  console.log('node env: ' + R.toString(env));

  let query = {
    $or: 
    [
      {
        environment: env,
        parent_id: id
      }, 
    ]
  };

  if (R.equals('host_ref', type)) {
    let realParent = Inventory.findOne({ 
      name: name,
      environment: env,
      type: 'host'
    });

    query = R.merge(query, {
      $or: R.append({
        environment: env,
        parent_id: realParent.id
      }, query.$or)
    });
  }

  console.log('query: ', R.toString(query));

  return Inventory.find(query);    
});

Meteor.publish('inventory.first-child', function (id, type, name, env) {
  console.log('server subscribing to: inventory.first-child');
  console.log('node id: ' + R.toString(id));
  console.log('node type: ' + R.toString(type));
  console.log('node name: ' + R.toString(name));
  console.log('node env: ' + R.toString(env));

  var counterName = 'inventory.first-child!counter!id=' + id;
  var query = {
    $or: [
      {
        environment: env,
        parent_id: id
      }
    ]
  };

  if (R.equals('host_ref', type)) {
    let realParent = Inventory.findOne({ 
      name: name,
      environment: env,
      type: 'host'
    });

    query = R.merge(query, {
      $or: R.append({
        environment: env,
        parent_id: realParent.id
      }, query.$or)
    });
  }

  Counts.publish(this, counterName, Inventory.find(query, { limit: 1 }));
  console.log('server subscribing to counter: ' + counterName);

// todo: eyaltask: all criteria
  console.log('query: ', R.toString(query));
  return Inventory.find(query, { limit: 1 });
});

Meteor.publish('inventoryByEnv', function (env) {
  console.log('server subscribtion to: inventoryByEnv');
  //return Inventory.find({$where: 'this.id_path.match('^/WebEX-Mirantis@Cisco/')'});
  //return Inventory.find({ 'show_in_tree': true });
  return Inventory.find({'environment':env});
});

