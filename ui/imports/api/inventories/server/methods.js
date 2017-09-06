/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { check } from 'meteor/check';
import * as R from 'ramda';
import { Inventory } from '../inventories';
import { Environments } from '/imports/api/environments/environments';
import { regexEscape } from '/imports/lib/regex-utils';
import { NodeHoverAttr, calcAttrsForItem } from '/imports/api/attributes_for_hover_on_data/attributes_for_hover_on_data';

const AUTO_COMPLETE_RESULTS_LIMIT = 15;

Meteor.methods({
  'inventorySearch': function(searchTerm, envId, opCounter) {
    console.log('inventorySearch');
    console.log('searchTerm', R.toString(searchTerm));
    console.log('envId', R.toString(envId));
    console.log('opCounter', R.toString(opCounter));

    this.unblock();

    if (R.anyPass([R.isNil, R.isEmpty])(searchTerm)) {
      return {
        searchResults: [],
        opCounter: opCounter
      };
    }

    let searchExp = new RegExp(regexEscape(searchTerm), 'i');

    let query = {
      name: searchExp 
    };

    if (! R.isNil(envId)) {
      let env = Environments.findOne({ _id: envId });
      query = R.merge(query, {
        environment: env.name  
      });
    }

    let searchResults = Inventory.find(query, {
      limit: AUTO_COMPLETE_RESULTS_LIMIT 
    }).fetch();

    searchResults = R.map((inventory) => {
      console.log('search result');
      console.log(R.toString(inventory));

      let itemEnv = Environments.findOne({ name: inventory.environment });

      return R.merge(inventory, {
        _envId: itemEnv._id
      });
    }, searchResults);

    return {
      opCounter: opCounter, 
      searchResults: searchResults,
    };
  },

  'expandNodePath': function(nodeId) {
    console.log('method server: expandNodePath', R.toString(nodeId));

    //check(nodeId, MongoI);
    this.unblock();

    let node = Inventory.findOne({ _id: nodeId });
    if (R.isNil(node)) { 
      console.log('method server: expandNodePath - no node');
      return null; 
    }

    let idList = R.pipe(R.split('/'), R.drop(2))(node.id_path);
    let result = R.map((partId) => {
      return Inventory.findOne({ environment: node.environment, id: partId });
    }, idList);
    
    console.log('method server: expandNodePath - results', result);
    return result;
  },

  'inventoryFindNode?type&env&name': function(type, envName, nodeName) {
    console.log('method server: inventoryFindNode', 
      R.toString(type), R.toString(envName), R.toString(nodeName));

    check(envName, String);
    check(nodeName, String);
    this.unblock();

    let query = { type: type, environment: envName, name: nodeName };
    let node = Inventory.findOne(query);

    return {
      node: node
    };
  },
  
  'inventoryFindNode?env&id': function (envName, nodeId) {
    console.log('method server: inventoryFindNode?env&id', 
      R.toString(envName), R.toString(nodeId));

    check(envName, String);
    check(nodeId, String);
    this.unblock();

    let query = { environment: envName, id: nodeId };
    let node = Inventory.findOne(query);

    return {
      node: node
    };
  },

  'inventoryFindNode?DataAndAttrs': function (nodeId) {
    console.log(`method server: inventoryFindNode?DataAndAttrs. ${R.toString(nodeId)}`);
    //check(nodeId, ObjectId);
    this.unblock();

    let query = { _id: nodeId };
    let node = Inventory.findOne(query);
    let attrsDefs = NodeHoverAttr.findOne({ 'type': node.type });
    let attributes = calcAttrsForItem(node, attrsDefs);

    return {
      node: node,
      nodeName: node.name,
      attributes: attributes
    };
  },
});
