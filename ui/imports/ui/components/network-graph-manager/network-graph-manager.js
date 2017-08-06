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
import { store } from '/imports/ui/store/store';
import { activateGraphTooltipWindow } from '/imports/ui/actions/graph-tooltip-window.actions';
import { closeGraphTooltipWindow } from '/imports/ui/actions/graph-tooltip-window.actions';
//import { activateVedgeInfoWindow } from '/imports/ui/actions/vedge-info-window.actions';
        
import '/imports/ui/components/network-graph/network-graph';

import './network-graph-manager.html';     
    
/*  
 * Lifecycles
 */   
  
Template.NetworkGraphManager.onCreated(function() {
  let instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    id_path: null,
    graphDataChanged: null,
    isReady: false,
  });
  instance.simpleState = {
    graphData: {
      links: [],
      nodes: [],
      groups: [],
    }
  };

  instance.autorun(function () {
    let data = Template.currentData();

    new SimpleSchema({
      id_path: { type: String },
    }).validate(data);

    instance.state.set('id_path', data.id_path);
  });

  instance.autorun(function () {
    let id_path = instance.state.get('id_path');

    instance.simpleState.graphData = generateGraphData();
    instance.state.set('isReady', false);

    instance.subscribe('attributes_for_hover_on_data');
    subscribeToNodeAndRelatedData(id_path, instance, instance.simpleState);
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

        Meteor.apply('inventoryFindNode?DataAndAttrs', [ nodeId ], 
          { wait: false }, function (err, res) {
            if (err) {
              console.error(`error fetching attrs for node for showing: ${R.toString(err)}`);
              return;
            }

            store.dispatch(
              activateGraphTooltipWindow(res.nodeName, res.attributes, x, y));
          });
      },
      onNodeOut: function (_nodeId) {
        store.dispatch(closeGraphTooltipWindow());
      },
      onNodeClick: function (_nodeId) {
      },
      onDragStart: function () {
        isDragging = true;
        store.dispatch(closeGraphTooltipWindow());
      },
      onDragEnd: function () {
        isDragging = false;
      },
    };
  },

  isReady: function () {
    let instance = Template.instance();
    return instance.state.get('isReady');
  }
}); // end: helpers

function subscribeToNodeAndRelatedData(id_path, instance, simpleState) {
  instance.subscribe('inventory?id_path', id_path);

  // id_path: assumption - unique
  Inventory.find({ id_path: id_path }).forEach((inventory) => {
    if (! inventory.clique) {
      return;
    }

    // focal point: assumption - unique per inventory node.
    let mainNodeIdStr = inventory._id._str;
    instance.subscribe('cliques?focal_point', mainNodeIdStr);

    Cliques.find({ focal_point: new Mongo.ObjectID(mainNodeIdStr) }).forEach( function (cliqueItem) {

      // Find links for focal point.
      instance.subscribe('links?_id-in', cliqueItem.links);

      Links.find({ _id: {$in: cliqueItem.links} }).forEach(function(link) {
        simpleState.graphData = addLinkToGraph(link, simpleState.graphData);
        instance.state.set('graphDataChanged', Date.now());

        // Find nodes for link
        let nodesIds = [ link['source'], link['target'] ];
        instance.subscribe('inventory?_id-in', nodesIds);

        Inventory.find({ _id: { $in: nodesIds } }).forEach(function (node) {
          simpleState.graphData = addNodeToGraph(node, simpleState.graphData);
          let isReady = calcIsReady(simpleState.graphData);
          instance.state.set('graphDataChanged', Date.now());
          instance.state.set('isReady', isReady);

          // Find nodes attributes for links nodes.
          instance.subscribe('attributes_for_hover_on_data?type', node.type);
        });
      });
    });
  });
}

function generateGraphData() {
  return {
    nodes: [],
    links: [],
    groups: [],
  };
}

function addLinkToGraph(link, graphData) {
  let newLink = {
    sourceId: link.source, 
    targetId: link.target, 
    label: link.link_name,
    _osid: link._id
  };

  let links = R.unionWith(R.eqBy(R.prop('_osid')), graphData.links, [newLink]);
  links = expandLinks(links, graphData.nodes);

  return R.merge(graphData, {
    links: links
  });
}

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

function addNodeToGraph(node, graphData) {
  let newNode = {
    _osid: node._id,
    _osmeta: {
      type: node.type,
      nodeId: node._id,
    },
    width: 60,
    height: 40,
    name: node._id._str,
  };

  let groupMarkers = ['host', 'switch'];
  let groupKey = R.find((key) => {
    if (R.isNil(R.path([key], node))) { return false; }
    return true;
  })(groupMarkers);
  if (groupKey) {
    newNode = R.assocPath(['_osmeta', 'groupId'], node[groupKey], newNode);
  }

  let nodes = R.unionWith(R.eqBy(R.prop('_osid')), graphData.nodes, [newNode]);
  let links = expandLinks(graphData.links, nodes);
  let groups = calcGroups(nodes);

  return R.merge(graphData, {
    nodes: nodes,
    links: links,
    groups: groups,
  });
}

function calcIsReady(graphData) {
  return R.all((link) => {
    return (!(R.isNil(link.source) || R.isNil(link.target)));
  }, graphData.links);
}

function calcGroups(nodes) {
  return R.reduce((accGroups, node) => {
    let groupId = R.path(['_osmeta', 'groupId'], node);
    if (R.isNil(groupId)) {
      return accGroups;
    }

    let groupIndex = R.findIndex(R.propEq('_osid', groupId), accGroups);
    let group = null;
    if (groupIndex < 0) {
      let group = { 
        _osid: groupId,
        leaves: [node],
        isExpanded: true,
        name: groupId,
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
