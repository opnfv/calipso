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
 * Template Component: NetworkGraphManager 
 */

//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { Inventory } from '/imports/api/inventories/inventories';
import { Cliques } from '/imports/api/cliques/cliques.js';
import { Links } from '/imports/api/links/links.js';
import * as R from 'ramda';
import * as _ from 'lodash';
import { store } from '/imports/ui/store/store';
import { activateGraphTooltipWindow } from '/imports/ui/actions/graph-tooltip-window.actions';
import { closeGraphTooltipWindow } from '/imports/ui/actions/graph-tooltip-window.actions';
import { activateVedgeInfoWindow } from '/imports/ui/actions/vedge-info-window.actions';
import { EJSON } from 'meteor/ejson';

import '/imports/ui/components/network-graph/network-graph';

import './network-graph-manager.html';

/*  
 * Lifecycles
 */

// Supported object types for grouping
let groupTypes = ['host', 'switch'];

Template.NetworkGraphManager.onCreated(function () {
  let instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    id_path: null,
    graphDataChanged: null,
    isReady: false,
    inventoriesToFind: [],
    cliquesToFind: [],
    linksToFind: [],
    nodesToFind: [],
    graphLinks: [],
    graphNodes: [],
  });

  instance.simpleState = {
    graphData: {
      links: [],
      nodes: [],
      groups: [],
    },
    itemOfInterest: null
  };

  instance.autorun(function () {
    let data = Template.currentData();

    new SimpleSchema({
      id_path: { type: String },
      environment: { type: String },
    }).validate(data);

    instance.state.set('id_path', data.id_path);
    instance.state.set('environment', data.environment);
  });

  instance.autorun(function () {
    let id_path = instance.state.get('id_path');

    instance.simpleState.graphData = generateGraphData();
    instance.state.set('graphDataChanged', null);
    instance.state.set('isReady', false);
    instance.state.set('inventoriesToFind', []);
    instance.state.set('cliquesToFind', []);
    instance.state.set('linksToFind', []);
    instance.state.set('nodesToFind', []);
    instance.state.set('graphLinks', []);
    instance.state.set('graphNodes', []);

    //instance.subscribe('attributes_for_hover_on_data');
    //subscribeToNodeAndRelatedData(id_path, instance, instance.simpleState);
    instance.state.set('inventoriesToFind', [id_path]);
  });

  instance.autorun(function () {
    let inventories = instance.state.get('inventoriesToFind');
    if (inventories.length <= 0) {
      return;
    }

    instance.subscribe('inventory?id_path', inventories[0]);

    // id_path: assumption - unique
    Inventory.find({ id_path: inventories[0] }).forEach((inventory) => {
      if (!inventory.clique) {
        return;
      }

      instance.state.set('cliquesToFind', [inventory._id]);
    });
  });

  instance.autorun(function () {
    let cliques = instance.state.get('cliquesToFind');
    if (cliques.length <= 0) {
      return;
    }

    // focal point: assumption - unique per inventory node.
    let mainNodeIdStr = cliques[0]._str;
    instance.subscribe('cliques?focal_point', mainNodeIdStr);

    Cliques.find({ focal_point: new Mongo.ObjectID(mainNodeIdStr) }).forEach(function (cliqueItem) {
      instance.state.set('linksToFind', cliqueItem.links);
    });
  });

  instance.autorun(function () {
    let linksToFind = instance.state.get('linksToFind');
    if (linksToFind.length <= 0) {
      return;
    }

    // Find links for focal point.
    instance.subscribe('links?_id-in', linksToFind);

    instance.state.set('graphLinks', []);
    Links.find({ _id: { $in: linksToFind } }).forEach(function (link) {
      let graphLinks = EJSON.parse(instance.state.keys['graphLinks']);
      graphLinks = R.concat([link], graphLinks);
      instance.state.set('graphLinks', graphLinks);
    });

  });

  instance.autorun(function () {
    let graphLinks = instance.state.get('graphLinks');
    if (graphLinks.length <= 0) {
      return;
    }

    instance.simpleState.graphData = addLinksToGraph(graphLinks, instance.simpleState.graphData);
    instance.state.set('graphDataChanged', Date.now());

    // Find nodes for link
    // todo: remove dubplicates.
    let nodesIds = R.chain(link => {
      return [link['source'], link['target']];
    }, graphLinks);

    let nodesToFind = EJSON.parse(instance.state.keys['nodesToFind']);
    nodesToFind = R.concat(nodesIds, nodesToFind);
    instance.state.set('nodesToFind', nodesToFind);
  });

  instance.autorun(function () {
    let nodesToFind = instance.state.get('nodesToFind');
    if (nodesToFind.length <= 0) {
      return;
    }

    instance.subscribe('inventory?_id-in', nodesToFind);

    instance.state.set('graphNodes', []);
    Inventory.find({ _id: { $in: nodesToFind } }).forEach(function (node) {
      let graphNodes = EJSON.parse(instance.state.keys['graphNodes']);
      graphNodes = R.concat([node], graphNodes);
      instance.state.set('graphNodes', graphNodes);
    });

  });

  instance.autorun(function () {
    let graphNodes = instance.state.get('graphNodes');
    if (graphNodes.length <= 0) {
      return;
    }

    groupTypes.forEach(function (groupType) {
      instance.subscribe('inventory?env+type', instance.data.environment, groupType);
    });
    instance.simpleState.graphData = addNodesToGraph(graphNodes, instance.simpleState.graphData);

    let isReady = calcIsReady(instance.simpleState.graphData);
    instance.state.set('graphDataChanged', Date.now());
    instance.state.set('isReady', isReady);
  });
});

/*
Template.NetworkGraphManager.rendered = function() {
};  
*/

/*
 * Events
 */

Template.NetworkGraphManager.events({
});

/*  
 * Helpers
 */

Template.NetworkGraphManager.helpers({
  graphDataChanged: function () {
    let instance = Template.instance();
    return instance.state.get('graphDataChanged');
  },

  argsNetworkGraph: function (_graphDataChanged) {
    let instance = Template.instance();
    let graphData = instance.simpleState.graphData;
    let isDragging = false;

    return {
      graphData: graphData,
      onNodeOver: function (nodeId, x, y) {
        if (isDragging) {
          return;
        }

        if (instance.simpleState.itemOfInterest === nodeId) {
          instance.simpleState.itemOfInterest = null;
          return;
        }

        instance.simpleState.itemOfInterest = nodeId;

        Meteor.apply('inventoryFindNode?DataAndAttrs', [nodeId],
          { wait: false }, function (err, res) {
            if (err) {
              console.error(`error fetching attrs for node for showing: ${R.toString(err)}`);
              return;
            }

            store.dispatch(
              activateGraphTooltipWindow(res.nodeName, res.attributes, x + 30, y - 10));
          });
      },
      onNodeOut: function (_nodeId) {
        store.dispatch(closeGraphTooltipWindow());
      },
      onNodeClick: function (nodeId, nodeType, env, x, y) {

        if (nodeType === 'vedge') {
          Meteor.apply('inventoryFindNode?_id', [
            nodeId,
          ], {
              wait: false
            }, function (err, res) {
              if (err) {
                console.error(R.toString(err));
                return;
              }

              if (_.lowerCase(R.path(['node', 'agent_type'], res)) === 'vpp') {
                store.dispatch(activateVedgeInfoWindow(res.node, x, y));
              }
              return;
            });
        }
      },
      onDragStart: function () {
        isDragging = true;
        store.dispatch(closeGraphTooltipWindow());
      },
      onDragEnd: function () {
        isDragging = false;
      },
      onGroupOver: function (groupId, x, y) {
        if (isDragging) {
          return;
        }

        if (instance.simpleState.itemOfInterest === groupId) {
          instance.simpleState.itemOfInterest = null;
          return;
        }

        instance.simpleState.itemOfInterest = groupId;

        Meteor.apply('inventoryFindNode?DataAndAttrs', [groupId],
          { wait: false }, function (err, res) {
            if (err) {
              console.error(`error fetching attrs for node for showing: ${R.toString(err)}`);
              return;
            }

            store.dispatch(activateGraphTooltipWindow(res.nodeName, res.attributes, x + 30, y - 10));
          });
      },
      onLinkOver: function (linkId, x, y) {
        if (isDragging) {
          return;
        }

        if (instance.simpleState.itemOfInterest === linkId) {
          instance.simpleState.itemOfInterest = null;
          return;
        }

        instance.simpleState.itemOfInterest = linkId;

        Meteor.apply('linksFind?DataAndAttrs', [linkId],
          { wait: false }, function (err, res) {
            if (err) {
              console.error(`error fetching attrs for link for showing: ${R.toString(err)}`);
              return;
            }

            store.dispatch(
              activateGraphTooltipWindow(res.linkName, res.attributes, x - 30, y - 10));
          });
      },
    };
  },

  isReady: function () {
    let instance = Template.instance();
    return instance.state.get('isReady');
  }
}); // end: helpers

function generateGraphData() {
  return {
    nodes: [],
    links: [],
    groups: [],
  };
}

function genGraphLink(link) {
  let newLink = {
    sourceId: link.source,
    targetId: link.target,
    label: link.link_name,
    _osid: link._id,
    _osmeta: {
      status: link.status,
      linkId: link._id
    }
  };

  return newLink;
}

function addLinksToGraph(linksInfo, graphData) {
  let newLinks = R.map(link => genGraphLink(link), linksInfo);

  let links = R.unionWith(R.eqBy(R.prop('_osid')), graphData.links, newLinks);
  links = R.map((link) => {
    let newLink = R.find(R.pathEq(['_osid', '_str'], link._osid._str), newLinks);
    if (newLink) {
      link._osmeta.status = newLink._osmeta.status;
    }
    return link;
  }, links);
  links = expandLinks(links, graphData.nodes);

  return R.merge(graphData, {
    links: links
  });
}

/*
function addLinkToGraph(link, graphData) {
  let newLink = genGraphLink(link);

  let links = R.unionWith(R.eqBy(R.prop('_osid')), graphData.links, [newLink]);
  links = expandLinks(links, graphData.nodes);

  return R.merge(graphData, {
    links: links
  });
}
*/

function expandLinks(links, nodes) {
  return R.map((link) => {
    let newLink = link;

    let nodeSource = R.find(R.propEq('_osid', newLink.sourceId), nodes);
    if (!R.isNil(nodeSource)) {
      newLink = R.assoc('source', nodeSource, newLink);
    }

    let nodeTarget = R.find(R.propEq('_osid', newLink.targetId), nodes);
    if (!R.isNil(nodeTarget)) {
      newLink = R.assoc('target', nodeTarget, newLink);
    }

    return newLink;
  }, links);
}

function genGraphNode(node) {
  let newNode = {
    _osid: node._id,
    _osmeta: {
      type: node.type,
      nodeId: node._id,
      status: node.status,
      environment: node.environment,
    },
    width: 60,
    height: 40,
    name: node._id._str,
  };

  let groupKey = R.find((key) => {
    if (R.isNil(R.path([key], node))) { return false; }
    return true;
  })(groupTypes);
  if (groupKey) {
    newNode = R.assocPath(['_osmeta', 'groupName'], node[groupKey], newNode);
    newNode = R.assocPath(['_osmeta', 'groupType'], groupKey, newNode);
  }

  return newNode;
}

function addNodesToGraph(nodesInfo, graphData) {
  let newNodes = R.map((node) => genGraphNode(node), nodesInfo);

  let nodes = R.unionWith(R.eqBy(R.prop('_osid')), graphData.nodes, newNodes);
  nodes = R.map((node) => {
    let newNode = R.find(R.pathEq(['_osid', '_str'], node._osid._str), newNodes);
    if (newNode) {
      node._osmeta.status = newNode._osmeta.status;
    }
    return node;
  }, nodes);

  let links = expandLinks(graphData.links, nodes);
  let groups = calcGroups(nodes);

  return R.merge(graphData, {
    nodes: nodes,
    links: links,
    groups: groups,
  });
}

/*
function addNodeToGraph(node, graphData) {
  let newNode = genGraphNode(node);

  let nodes = R.unionWith(R.eqBy(R.prop('_osid')), graphData.nodes, [newNode]);
  let links = expandLinks(graphData.links, nodes);
  let groups = calcGroups(nodes);

  return R.merge(graphData, {
    nodes: nodes,
    links: links,
    groups: groups,
  });
}
*/

function calcIsReady(graphData) {
  return R.all((link) => {
    return (!(R.isNil(link.source) || R.isNil(link.target)));
  }, graphData.links);
}

function calcGroups(nodes) {
  return R.reduce((accGroups, node) => {
    let groupName = R.path(['_osmeta', 'groupName'], node);
    let groupObject = Inventory.findOne({ type: node._osmeta.groupType, environment: node._osmeta.environment, name: groupName });
    if (R.isNil(groupName) || R.isNil(groupObject)) {
      return accGroups;
    }

    let groupId = groupObject._id;
    node._osmeta.groupId = groupId;
    let groupIndex = R.findIndex(R.propEq('_osid', groupId), accGroups);
    let group = null;
    if (groupIndex < 0) {
      let group = {
        _osid: groupId,
        leaves: [node],
        isExpanded: true,
        name: groupName,
        type: node._osmeta.groupType,
      };
      accGroups = R.append(group, accGroups);

    } else {
      let group = accGroups[groupIndex];
      group = R.merge(group, {
        leaves: R.append(node, group.leaves)
      });
      accGroups = R.update(groupIndex, group, accGroups);
    }

    node.parent = group;
    return accGroups;
  }, [], nodes);
}
