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
 * Template Component: d3graph 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import * as R from 'ramda';
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { Inventory } from '/imports/api/inventories/inventories';
import { Cliques } from '/imports/api/cliques/cliques.js';
import { Links } from '/imports/api/links/links.js';
        
import { d3Graph } from '/imports/lib/d3-graph';

import './d3graph.html';     
    
/*  
 * Lifecycles
 */   
  
Template.d3graph.onCreated(function() {
  let instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    id_path: null,
    ready: false
  });

  instance.autorun(function () {
    let data = Template.currentData();

    new SimpleSchema({
      id_path: { type: String },
    }).validate(data);

    instance.state.set('ready', false);
    let id_path = data.id_path;

    instance.subscribe('inventory?id_path', id_path);
    instance.subscribe('attributes_for_hover_on_data');

    Inventory.find({ id_path: id_path }).forEach((inventory) => {
      instance.state.set('_id', inventory._id);

      if (inventory.clique) {

        if (inventory.id === 'aggregate-WebEx-RTP-SSD-Aggregate-node-24') {
          let objId = 'node-24';
          instance.subscribe('inventory?type+host', 'instance', objId);

        } else {
          let objId = inventory._id._str;
          instance.subscribe('cliques?focal_point', objId);

          Cliques.find({
            focal_point: new Mongo.ObjectID(objId)
          })
          .forEach(
            function (cliqueItem) {
              instance.subscribe('links?_id-in', cliqueItem.links);

              Links.find({ _id: {$in: cliqueItem.links} })
              .forEach(function(linkItem) {
                let idsList = [ linkItem['source'], linkItem['target'] ];
                instance.subscribe('inventory?_id-in', idsList);

                Inventory.find({ _id: { $in: idsList } })
                .forEach(function (invItem) {
                  instance.subscribe('attributes_for_hover_on_data?type', invItem.type);
                });
              });

              instance.state.set('ready', true);
            });
        }
      }
    });
  });
});  

Template.d3graph.rendered = function () {
  let instance = Template.instance();
  let element = instance.$('#dgraphid')[0];
  d3Graph.createGraphData(element.clientWidth, element.clientHeight);

  Tracker.autorun(function () {
    var nodeId = instance.state.get('_id');
    var ready = instance.state.get('ready');

    if (! ready) { return; }
    if(R.isNil(nodeId)) { return; }

    setTimeout(() => {
      let graphData = d3Graph.getGraphDataByClique(nodeId._str);
      setTimeout(() => {
        d3Graph.updateNetworkGraph(graphData);
      }, 100);
    }, 500);
  });
};

/*
 * Events
 */

Template.d3graph.events({
});
   
/*  
 * Helpers
 */

Template.d3graph.helpers({    
});


