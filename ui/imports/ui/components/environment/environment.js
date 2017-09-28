/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Tempalte Component: Environment
 */

/*
 * Lifecycles methods
 */

import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { ReactiveVar } from 'meteor/reactive-var';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';
import { EJSON } from 'meteor/ejson';
import factory from 'reactive-redux';
import { _idFieldDef } from '/imports/lib/simple-schema-utils';
//import { idToStr } from '/imports/lib/utilities';

import { Environments } from '/imports/api/environments/environments';
import { Inventory } from '/imports/api/inventories/inventories';
//import { Messages } from '/imports/api/messages/messages';

import { store } from '/imports/ui/store/store';
//import { setCurrentNode } from '/imports/ui/actions/navigation';
import { 
  setEnvEnvId,
  setEnvName, 
  updateEnvTreeNode, 
  startOpenEnvTreeNode,
  setEnvSelectedNodeInfo,
  setEnvAsLoaded,
  setEnvAsNotLoaded,
  setEnvSelectedNodeAsEnv,
  toggleEnvShow,
  endOpenEnvTreeNode,
  reportEnvNodePositionRetrieved,
  setEnvScrollToNodeIsNeededAsOn,
  reportEnvScrollToNodePerformed,
  resetEnvNeedChildDetection,
  setShowDashboard,
//  setShowGraph,
} from '/imports/ui/actions/environment-panel.actions';
import { setMainAppSelectedEnvironment } from '/imports/ui/actions/main-app.actions';
import { closeVedgeInfoWindow } from '/imports/ui/actions/vedge-info-window.actions';
import { setEnvSelectedNode } 
  from '/imports/ui/actions/environment-panel.actions';

import '/imports/ui/components/accordion-nav-menu/accordion-nav-menu';
import '/imports/ui/components/graph-tooltip-window/graph-tooltip-window';
import '/imports/ui/components/vedge-info-window/vedge-info-window';
import '/imports/ui/components/env-delete-modal/env-delete-modal';
import '/imports/ui/components/environment-dashboard/environment-dashboard';
import '/imports/ui/components/general-folder-node-dashboard/general-folder-node-dashboard';
import '/imports/ui/components/general-node-dashboard/general-node-dashboard';
import '/imports/ui/components/network-graph-manager/network-graph-manager';

import './environment.html';

let maxOpenTreeNodeTrialCount = 3;

/*
var nodeTypesForSelection = [
  'project', 
  'availability_zone',
  'host',
  'environment',
  'aggregate',
  'host',
  'region',
  'instance',
  'network'
];
*/

/*
 * Lifecycles
 */

Template.Environment.onCreated(function () {
  var instance = this;

  instance.collapsedSideMenu = false;

  // reactive state
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    graphTooltipWindow: { label: '', title: '', left: 0, top: 0, show: false },
    vedgeInfoWindow: { node: null, left: 0, top: 0, show: false },
    dashboardName: 'environment',
    collapsedSideMenu: instance.collapsedSideMenu,
    isLoading: false,
  });

  instance.currentData = new ReactiveVar(null, EJSON.equals);
  instance.onNodeOpeningDone = _.debounce(() => {
    scrollTreeToLastOpenedChild(instance);
  }, 400);

  createAttachedFns(instance);

  const envIdSelector = (state) => (state.components.environmentPanel._id);
  instance.rdxEnvId = factory(envIdSelector, store);  

  const mainNodeSelector = (state) => (state.components.environmentPanel.treeNode);
  instance.rdxMainNode = factory(mainNodeSelector, store);

  const selectedNodeIdSelector = 
    (state) => (state.components.environmentPanel.selectedNode._id);
  instance.rdxSelectedNodeId = factory(selectedNodeIdSelector, store);

  const selectedNodeTypeSelector = 
    (state) => (state.components.environmentPanel.selectedNode.type);
  instance.rdxSelectedNodeType = factory(selectedNodeTypeSelector, store);

  const envNameSelector = (state) => (state.components.environmentPanel.envName);
  instance.rdxEnvName = factory(envNameSelector, store);

  const isLoadedSelector = (state) => (state.components.environmentPanel.isLoaded);
  instance.rdxIsLoaded = factory(isLoadedSelector, store);

  const showTypeSelector = (state) => (state.components.environmentPanel.showType);
  instance.rdxShowType = factory(showTypeSelector, store);

  const selectedNodeCliqueSelector = 
    (state) => (state.components.environmentPanel.selectedNode.clique);
  instance.rdxSelectedNodeClique = factory(selectedNodeCliqueSelector, store);

  const selectedNodeIdPathSelector = 
    (state) => (state.components.environmentPanel.selectedNode.id_path);
  instance.rdxSelectedNodeIdPath = factory(selectedNodeIdPathSelector, store);

  const i18nSelector = (state) => (state.api.i18n);
  instance.rdxI18n = factory(i18nSelector, store);

  instance.autorun((function(_this) {
    return function(_computation) {
      return _this.currentData.set(Template.currentData());
    };
  })(instance));

  let lastData = null;

  // Autorun component input
  instance.autorun(function () {
    let data = instance.currentData.get();

    if (R.equals(data, lastData)) { return; }
    lastData = data;  
    
    new SimpleSchema({
      _id: _idFieldDef, 
      selectedNodeId: R.assoc('optional', true, _idFieldDef),
      refresh: { type: String, optional: true }, 
    }).validate(data);

    store.dispatch(setEnvEnvId(data._id));
    if (R.isNil(data.selectedNodeId)) {
      store.dispatch(setEnvSelectedNodeAsEnv());
    } else {
      store.dispatch(setEnvSelectedNode(data.selectedNodeId));
    }
  });

  // Autorun object id
  instance.autorun(function () {
    let _id = instance.rdxEnvId.get();
    store.dispatch(setEnvAsNotLoaded());

    instance.subscribe('environments?_id', _id);
    Environments.find({ _id: _id }).forEach((env) => {
      store.dispatch(setEnvName(env.name));
      store.dispatch(updateEnvTreeNode(env));
      store.dispatch(setEnvAsLoaded());
      store.dispatch(startOpenEnvTreeNode([]));
      store.dispatch(setMainAppSelectedEnvironment(env._id));
      store.dispatch(setShowDashboard());
    });
  });

  // Autorun selected node
  instance.autorun(function () {
    let selectedNodeId = instance.rdxSelectedNodeId.get(); 
    //let selectedNodeType = instance.rdxSelectedNodeType.get();

    if (R.isNil(selectedNodeId)) { return; }
    //if (selectedNodeType === 'environment') { return; }

    instance.subscribe('inventory?_id', selectedNodeId);
    Inventory.find({ _id: selectedNodeId }).forEach((selectedNode) => {
      store.dispatch(setEnvSelectedNodeInfo(selectedNode));

      Meteor.apply('expandNodePath', 
        [ selectedNode._id ], 
        { wait: false }, 
        function (err, res) {
          if (err) { 
            console.error(err);
            return;
          }

          if (R.isNil(res)) { return; }
          
          let idList = R.map(R.path(['_id', '_str']), res);
          openTreeNode([R.head(idList)], R.tail(idList), 0);
        });
    });
  });

  /////////////////

  instance.storeUnsubscribe = store.subscribe(() => {
    let state = store.getState();

    let graphTooltipWindow = state.components.graphTooltipWindow;
    instance.state.set('graphTooltipWindow', graphTooltipWindow);

    let vedgeInfoWindow = state.components.vedgeInfoWindow;
    instance.state.set('vedgeInfoWindow', vedgeInfoWindow);
    
  });

  /*
  (() => {
    if (R.isNil(controller.params.query.selectedNodeId) &&
        R.isNil(selectedNodeId)) {
      return;
    }

    let srlSelectedNodeId = idToStr(selectedNodeId);
    if (R.equals(controller.params.query.selectedNodeId, srlSelectedNodeId)) {
      return;
    }

    setTimeout(() => {
      Router.go('environment', 
        { _id: controller.params._id }, 
        { query: { selectedNodeId: srlSelectedNodeId } });
    }, 1);

  })();
  */

  let prevIdPath = null;
  instance.autorun(function () {
    let idPath = instance.rdxSelectedNodeIdPath.get();
    if (prevIdPath !== idPath) {
      prevIdPath = idPath;
      instance.state.set('isLoading', true);
    }
  });

  instance.autorun(function () {
    let isLoading = instance.state.get('isLoading');
    if (isLoading) {
      setTimeout(() => {
        instance.state.set('isLoading', false);
      }, 200);
    }
  });
});

Template.Environment.onDestroyed(function () {
  let instance = this;
  instance.storeUnsubscribe();
  instance.rdxMainNode.cancel();
  instance.rdxEnvId.cancel();
  instance.rdxSelectedNodeId.cancel();
  instance.rdxEnvName.cancel();
  instance.rdxIsLoaded.cancel();
  instance.rdxShowType.cancel();
  instance.rdxSelectedNodeIdPath.cancel();
});

Template.Environment.rendered = function(){
};

/*
 * Helpers
 */

Template.Environment.helpers({
  isLoaded: function () {
    let instance = Template.instance();
    return instance.rdxIsLoaded.get();
  },

  envName: function(){
    let instance = Template.instance();
    return instance.rdxEnvName.get();
  },

  mainNode: function () {
    let instance = Template.instance();
    return instance.rdxMainNode.get();
  },

  selectedNodeType: function () {
    let instance = Template.instance();
    return instance.rdxSelectedNodeType.get();
  },

  getState: function (key) {
    let instance = Template.instance();
    return instance.state.get(key);
  },

  isLoading: function () {
    let instance = Template.instance();
    return instance.state.get('isLoading');
  },

  argsNavMenu: function (envName, mainNode) {
    let instance = Template.instance();
    return {
      envName: envName,
      mainNode: mainNode,
      onOpeningDone: instance._fns.onOpeningDone,
      onNodeSelected: instance._fns.onNodeSelected,
      onToggleGraphReq: function () {
        store.dispatch(toggleEnvShow());
      },
      onResetSelectedNodeReq: function () {
        store.dispatch(setEnvSelectedNodeAsEnv());
      },
      onPositionRetrieved: instance._fns.onPositionRetrieved,
      onScrollToNodePerformed: instance._fns.onScrollToNodePerformed,
      onOpenLinkReq: instance._fns.onOpenLinkReq,
      onResetNeedChildDetection: instance._fns.onResetNeedChildDetection,
      onToggleMenu: function () {
        instance.collapsedSideMenu = !instance.collapsedSideMenu;
        instance.state.set('collapsedSideMenu', 
          instance.collapsedSideMenu);
      },
      showCollapsed: instance.state.get('collapsedSideMenu'),
    };
  },

  graphTooltipWindow: function () {
    let instance = Template.instance();
    let graphTooltipWindow = instance.state.get('graphTooltipWindow');

    return graphTooltipWindow; 
  },

  vedgeInfoWindow: function () {
    let instance = Template.instance();
    let vedgeInfoWindow = instance.state.get('vedgeInfoWindow');

    return vedgeInfoWindow; 
  },

  argsGraphTooltipWindow: function (graphTooltipWindow) {
    return {
      label: R.path(['label'], graphTooltipWindow),
      title: R.path(['title'], graphTooltipWindow),
      left: R.path(['left'], graphTooltipWindow),
      top: R.path(['top'], graphTooltipWindow),
      show: R.path(['show'], graphTooltipWindow)
    };
  },

  argsVedgeInfoWindow: function (vedgeInfoWindow) {
    return {
      environment: R.path(['node', 'environment'], vedgeInfoWindow),
      object_id: R.path(['node', 'id'], vedgeInfoWindow),
      name: R.path(['node', 'name'], vedgeInfoWindow),
      left: R.path(['left'], vedgeInfoWindow),
      top: R.path(['top'], vedgeInfoWindow),
      show: R.path(['show'], vedgeInfoWindow),
      onCloseRequested: function () {
        store.dispatch(closeVedgeInfoWindow());
      }
    };
  },

  argsD3Graph: function () {
    let instance = Template.instance();
    let idPath = instance.rdxSelectedNodeIdPath.get();

    return {
      id_path: idPath
    };
  },

  argsNetworkGraphManager: function () {
    let instance = Template.instance();
    let idPath = instance.rdxSelectedNodeIdPath.get();

    return {
      id_path: idPath
    };
  },

  showVedgeInfoWindow: function () {
    let instance = Template.instance();
    let node = instance.state.get('vedgeInfoWindow').node;
    return ! R.isNil(node);
  },

  isSelectedNodeAGraph: function () {
    let instance = Template.instance();
    let nodeClique = instance.rdxSelectedNodeClique.get();

    return !R.isNil(nodeClique);
  },

  dashboardTemplate: function () {
    let instance = Template.instance();
    let selectedNodeType = instance.rdxSelectedNodeType.get();
    let dashTemplate = 'EnvironmentDashboard';

    switch (selectedNodeType) {
    case 'project':
      dashTemplate = 'ProjectDashboard';
      break;

    case 'region':
      dashTemplate = 'RegionDashboard';
      break;

    case 'aggregate':
      dashTemplate = 'AggregateDashboard';
      break;

    case 'host':
      dashTemplate = 'HostDashboard';
      break;

    case 'availability_zone':
      dashTemplate = 'ZoneDashboard';
      break;

    case 'environment':
      dashTemplate = 'EnvironmentDashboard';
      break;

    case 'vservice_routers_folder':
    case 'vnics_folder':
    case 'regions_folder':
    case 'vedges_folder':
    case 'network_agents_folder':
    case 'network_services_folder':
    case 'availability_zones_folder':
    case 'pnics_folder':
    case 'networks_folder':
    case 'vconnectors_folder':
    case 'projects_folder':
    case 'aggregates_folder':
    case 'vservices_folder':
    case 'vservice_dhcps_folder':
    case 'ports_folder':
    case 'instances_folder':
      dashTemplate = 'GeneralFolderNodeDashboard';
      break;

    default:
      dashTemplate = 'GeneralNodeDashboard';
    }

    return dashTemplate;
  },

  rdxSelectedNodeId: function () {
    let instance = Template.instance();
    return instance.rdxSelectedNodeId.get();
  },

  argsDashboard: function (nodeId) {
    //let instance = Template.instance();

    return {
      _id: nodeId,
      onNodeSelected: function (selectedNodeId) {
        store.dispatch(setEnvSelectedNode(selectedNodeId, null));
      }
    };
  },

  argsBreadCrumb: function (selectedNodeId) {
    return {
      nodeId: selectedNodeId,
      onNodeSelected: function (node) {
        store.dispatch(setEnvSelectedNode(node._id, null));
      }
    };
  },

  getShow: function (qShowType) {
    let instance = Template.instance();
    let showType = instance.rdxShowType.get();

    return R.equals(showType, qShowType);
  },

  i18n: function () {
    let instance = Template.instance();
    return instance.rdxI18n.get();

  },
}); // end: helpers


Template.Environment.events({
});

function openTreeNode(path, rest, trialCount) {
  if (trialCount > maxOpenTreeNodeTrialCount) {
    return;
  }

  let tree = store.getState().components.environmentPanel
    .treeNode;

  let node = getNodeInTree(path, tree);
  if (R.isNil(node)) { 
    setTimeout(() => {
      openTreeNode(path, rest, trialCount + 1);
    }, 800);
    return; 
  }
  
  if (node.openState === 'closed') {
    store.dispatch(startOpenEnvTreeNode(path)); 
    setTimeout(() => {
      openTreeNode(path, rest, trialCount + 1);
    }, 200);
    return;
  }

  if (R.length(rest) === 0) { return; } 

  let newPath = R.append(R.head(rest), path);
  let newRest = R.drop(1, rest);
  openTreeNode(newPath, newRest, 0);
}

function getNodeInTree(path, tree) {
  if (R.length(path) === 0) { return tree; }

  let first = R.head(path);
  let rest = R.tail(path);
  let child = R.find(R.pathEq(['nodeInfo', '_id', '_str'], first), 
    tree.children); 

  if (R.isNil(child)) { return null; }
 
  return getNodeInTree(rest, child);  
}

function createAttachedFns(instance) {
  instance._fns = {
    onOpeningDone: (nodePath, _nodeInfo) => {
      store.dispatch(endOpenEnvTreeNode(R.tail(nodePath)));
      instance.lastOpenedNodePath = nodePath;
      instance.onNodeOpeningDone();
    },

    onNodeSelected: (nodeInfo) => {
      //if (R.contains(nodeInfo.type, nodeTypesForSelection)) {
      store.dispatch(setEnvSelectedNode(nodeInfo._id, null));
      //}
    },

    onPositionRetrieved: (nodePath, rect) => {
      store.dispatch(
        reportEnvNodePositionRetrieved(R.tail(nodePath), rect));
    },

    onScrollToNodePerformed: (nodePath) => {
      store.dispatch(reportEnvScrollToNodePerformed(R.tail(nodePath)));
    },

    onOpenLinkReq: (envName, nodeName) => {
      Meteor.apply('inventoryFindNode?type&env&name', [
        'host', envName, nodeName
      ], {
        wait: false
      }, function (err, res) {
        if (err) { 
          console.log('error in inventoryFindNode', err);
          return;
        }
        
        store.dispatch(setEnvSelectedNode(res.node._id, null));
      });
    },

    onResetNeedChildDetection: (nodePath) => {
      store.dispatch(resetEnvNeedChildDetection(R.tail(nodePath)));
    }
  };
}

function scrollTreeToLastOpenedChild(instance) {
  store.dispatch(setEnvScrollToNodeIsNeededAsOn(R.tail(instance.lastOpenedNodePath)));
}
