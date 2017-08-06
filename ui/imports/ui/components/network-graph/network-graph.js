/*
 * Template Component: NetworkGraph 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';
import * as cola from 'webcola';
import { imagesForNodeType, defaultNodeTypeImage } from '/imports/lib/images-for-node-type';
        
import './network-graph.html';     
    
/*  
 * Lifecycles
 */   
  
Template.NetworkGraph.onCreated(function() {
  let instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    graphDataChanged: null,
  });
  instance.simpleState = {
    graphData: null
  };

  instance.autorun(function () {
    let data = Template.currentData();

    new SimpleSchema({
      graphData: { type: Object, blackbox: true },
      onNodeOver: { type: Function, optional: true },
      onNodeOut: { type: Function, optional: true },
      onNodeClick: { type: Function, optional: true },
      onDragStart: { type: Function, optional: true },
      onDragEnd: { type: Function, optional: true },
    }).validate(data);

    instance.simpleState.graphData = data.graphData;
    instance.state.set('graphDataChanged', Date.now());
    instance.onNodeOver = R.defaultTo(() => {}, data.onNodeOver);
    instance.onNodeOut = R.defaultTo(() => {}, data.onNodeOut);
    instance.onNodeClick = R.defaultTo(() => {}, data.onNodeClick);
    instance.onDragStart = R.defaultTo(() => {}, data.onDragStart);
    instance.onDragEnd = R.defaultTo(() => {}, data.onDragEnd);
  });
});  

Template.NetworkGraph.rendered = function() {
  let instance = Template.instance();

  instance.autorun(function () {
    //let _graphDataChanged = 
    instance.state.get('graphDataChanged');
    let graphEl = instance.$('.sm-graph')[0];

    renderGraph(graphEl, 
      graphEl.clientWidth, 
      graphEl.clientHeight,
      instance.simpleState.graphData,
      genConfig(),
      instance.onNodeOver,
      instance.onNodeOut, 
      instance.onNodeClick,
      instance.onDragStart,
      instance.onDragEnd
    );
  });
};  

/*
 * Events
 */

Template.NetworkGraph.events({
});
   
/*  
 * Helpers
 */

Template.NetworkGraph.helpers({    
}); // end: helpers


function genConfig() {
  let outline = false;
  let tocolor = 'fill';
  let towhite = 'stroke';
  if (outline) {
    tocolor = 'stroke';
    towhite = 'fill';
  }

  return {
    initialLinkLabelsFontSize: 18,
    tocolor: tocolor,
    towhite: towhite,
    text_center: false,
    outline: outline,
    min_score: 0,
    max_score: 1,
    highlight_color: 'blue',
    highlight_trans: 0.1,
    default_node_color: '#ccc',
    //var default_node_color: 'rgb(3,190,100)',
    default_link_color: '#888',
    nominal_base_node_size: 8,
    nominal_text_size: 10,
    max_text_size: 24,
    nominal_stroke: 1.5,
    max_stroke: 4.5,
    max_base_node_size: 36,
    min_zoom: 0.3,
    max_zoom: 5,
  };
}

function renderGraph(
  mainElement, 
  w, 
  h, 
  graph, 
  config, 
  onNodeOver, 
  onNodeOut, 
  onNodeClick,
  onDragStart,
  onDragEnd
) {

  let force = genForceCola(cola, d3, w, h);
  let drag = force.drag()
    .on('start', function (_d) {
      onDragStart();
    })
    .on('end', function (_d) {
      onDragEnd();
    })
  ;

  let svg = d3.select(mainElement).select('svg');
  svg.remove();
  svg = genSvg(d3, mainElement);

  let zoom = genZoomBehavior(d3, config);
  svg.call(zoom);

  let mainEl = svg.append('g');
  let groupsEl = mainEl.append('g').attr('class', 'groups-container');
  let linksEl = mainEl.append('g').attr('class', 'links-container');
  let nodesEl = mainEl.append('g').attr('class', 'nodes-container');
  
  renderView(force, {
    graph: graph, 
    viewGraph: {
      nodes: [], 
      links: [], 
      groups: []
    },  
  },
  mainEl, 
  groupsEl,
  nodesEl,
  linksEl,
  drag, zoom, config, 
  onNodeOver, onNodeOut, onNodeClick);
}

 // d3.select(window).on('resize', resize);

function genSvg(d3, mainElement) {
  let svg = d3.select(mainElement).append('svg');

  svg.style('cursor', 'move')
    .attr('width', '100%')
    .attr('height', '100%')
    .attr('pointer-events', 'all');

  return svg;
}

function genSvgLinks(g, links, nominal_stroke, default_link_color, initialLinkLabelsFontSize) {
  let svgLinks = g.selectAll('.link-group')
    .data(links, (d) => d._osid);

  let svgLinksEnter = svgLinks
    .enter()
      .append('g')
        .attr('class', 'link-group')
        .attr('data-link-id', function (d) {
          return d._osid;
        })
  ;

  //let svgLinksExit = 
  svgLinks
    .exit().remove();

  let svgLinkLines = svgLinksEnter
    .append('line')
    .attr('class', 'link-line')
    .style('stroke-width', nominal_stroke)
    .style('stroke', 
    function(_d) { 
      return default_link_color;
    });

  let svgLinkLabels = svgLinksEnter
    .append('text')
    .text(function(d) { 
      return d.label; 
    })
    .attr('class', 'link-label')
    .attr('x', function(d) { return (d.source.x + (d.target.x - d.source.x) * 0.5); })
    .attr('y', function(d) { return (d.source.y + (d.target.y - d.source.y) * 0.5); })
    .attr('dy', '.25em')
    .attr('text-anchor', 'right')
    .attr('font-size', initialLinkLabelsFontSize)
  ;

  return {svgLinks, svgLinkLines, svgLinkLabels};
}

function genSvgNodes(g, nodes, drag, onNodeOver, onNodeOut, onNodeClick, onGroupNodeClick) {
  let svgNodes = g.selectAll('.node')
    .data(nodes, (d) => d._osid);

  let svgNodesEnter = svgNodes
    .enter()
    .append('g')
      .attr('class', 'node')
      .attr('data-node-id', (d) => d._osid)
      .call(drag);

  //let svgNodesExit = 
  svgNodes
    .exit().remove();
  
  let imageLength = 36;
  let svgImages = svgNodesEnter.append('image')
    .attr('class', 'node-image')
    .attr('xlink:href', function(d) {
      return `/${calcImageForNodeType(d._osmeta.type)}`;
    })
    .attr('x', -(Math.floor(imageLength / 2)))
    .attr('y', -(Math.floor(imageLength / 2)))
    .attr('width', imageLength)
    .attr('height', imageLength)
    .on('mouseover', function (d) {
      onNodeOver(d._osmeta.nodeId, d3.event.pageX, d3.event.pageY);
    })
    .on('mouseout', function (d) {
      onNodeOut(d._osmeta.nodeId);
    })
    .on('click', function (d) {
      if (R.path(['_osmeta', 'type'], d) === 'view_group') {
        onGroupNodeClick(d._osmeta.nodeId);
      }
      onNodeClick(d._osmeta.nodeId);
    })
  ;

  return {svgNodes, svgImages};
  //return [svgNodes];
}

function calcImageForNodeType(nodeType) {
  return R.defaultTo(defaultNodeTypeImage, R.prop(nodeType, imagesForNodeType));
}

function genZoomBehavior(d3, config) {
  let zoom = d3.zoom().scaleExtent([config.min_zoom, config.max_zoom]);

  return zoom;
}

/*
function genForceD3(d3, w, h) {
  let force = d3.layout.force()
    .linkDistance(60)
    .charge(-300)
    .size([w,h]);

  return force;
}
*/

function genForceCola(cola, d3, w, h) {
  let force = cola.d3adaptor(d3)
    .convergenceThreshold(0.1)
  //  .convergenceThreshold(1e-9)
    .linkDistance(120)
    .size([w,h]);

  return force;
}

function activateForce(force, nodes, links, groups) {
  force
    .nodes(nodes)
    .links(links) 
    .groups(groups)
    //.symmetricDiffLinkLengths(25)
    .handleDisconnected(true)
    .avoidOverlaps(true)
    .start(50, 100, 200);
    //.start();
}

/*
function resize() {
  let width = mainElement.clientWidth;
  let height = mainElement.clientHeight;

  svg.attr('width', '100%') //width)
    .attr('height', '100%'); //height);

  force.size([
    force.size()[0] + (width - w) / zoom.scale(), 
    force.size()[1] + (height - h) / zoom.scale()
  ]).resume();

  w = width;
  h = height;
}
*/

function renderView(force, 
  state, 
  mainEl, 
  groupsEl,
  nodesEl,
  linksEl,
  drag, 
  zoom, 
  config, 
  onNodeOver, 
  onNodeOut, 
  onNodeClick) {

  state.viewGraph = calcViewGraph(state.graph, state.viewGraph);

  activateForce(force, state.viewGraph.nodes, state.viewGraph.links, state.viewGraph.groups);

  zoom.on('zoom', zoomFn);

  genSvgGroups(groupsEl, state.viewGraph.groups, drag, onRenderViewReq);

  genSvgLinks(
    linksEl, state.viewGraph.links, 
    config.nominal_stroke, 
    config.default_link_color,
    config.initialLinkLabelsFontSize
  );

  genSvgNodes(
    nodesEl, state.viewGraph.nodes, drag, onNodeOver, onNodeOut, onNodeClick, 
    function onGroupNodeClick(groupId) {
      let group = R.find(R.propEq('_osid', groupId), state.graph.groups);
      group.isExpanded = true;

      state.viewGraph = renderView(force, state, 
        mainEl, groupsEl, nodesEl, linksEl,
        drag, zoom, config, 
        onNodeOver, onNodeOut, onNodeClick);
    }); 

  force.on('tick', tickFn);
  
  function onRenderViewReq() {
    state.viewGraph = renderView(force, state, 
      mainEl, groupsEl, nodesEl, linksEl,
      drag, zoom, config, 
      onNodeOver, onNodeOut, onNodeClick);
  }

  function tickFn() {
    let svgGroups = mainEl.selectAll('.group');
    svgGroups
      .attr('transform', function (d) {
        let x = R.path(['bounds', 'x'], d);
        let y = R.path(['bounds', 'y'], d);
        return `translate(${x},${y})`;
      })
    ;
    /*
      .attr('x', function (d) { 
        return R.path(['bounds', 'x'], d); 
      })
      .attr('y', function (d) { 
        return R.path(['bounds', 'y'], d);
      })
      */

    svgGroups.selectAll('.group-shape')
      .attr('width', function (d) { 
        if (d.bounds) { return d.bounds.width(); } 
      })
      .attr('height', function (d) { 
        if (d.bounds) { return d.bounds.height(); } 
      });

    svgGroups.selectAll('.group-name')
      .attr('x', function(d) { 
        return (d.bounds.width() / 2);
      })
      .attr('y', function(_d) { 
        return 30;
      })
    ;

    let svgNodes = mainEl.selectAll('.node');
    svgNodes.attr('transform', function(d) {
      return 'translate(' + d.x + ',' + d.y + ')';
    });

    let svgLinkLines = mainEl.selectAll('.link-group').selectAll('.link-line');
    svgLinkLines
      .attr('x1', function(d) { 
        return d.source.x; 
      })
      .attr('y1', function(d) { return d.source.y; })
      .attr('x2', function(d) { return d.target.x; })
      .attr('y2', function(d) { return d.target.y; });

    let svgLinkLabels = mainEl.selectAll('.link-group').selectAll('.link-label');
    svgLinkLabels
      .attr('x', function(d) { 
        return (d.source.x + (d.target.x - d.source.x) * 0.5); 
      })
      .attr('y', function(d) { 
        return (d.source.y + (d.target.y - d.source.y) * 0.5); 
      });

  }

  function zoomFn() {
    mainEl.attr('transform', d3.event.transform);
    
    let trn = d3.event.transform;

    let maxZoomAllowedForNodes = 1.8;
    let imageInitialLength = 36;
    let imageLength;

    if (trn.k > maxZoomAllowedForNodes) {
      imageLength = (imageInitialLength / trn.k) * maxZoomAllowedForNodes;
    } else {
      imageLength = imageInitialLength;
    }

    let svgImages = mainEl.selectAll('.node-image');
    svgImages 
      .attr('x', -(Math.floor(imageLength / 2)))
      .attr('y', -(Math.floor(imageLength / 2)))
      .attr('width', imageLength)
      .attr('height', imageLength)
    ;

    let labelsFontSize;

    if (trn.k > maxZoomAllowedForNodes) {
      labelsFontSize = (config.initialLinkLabelsFontSize / trn.k) * maxZoomAllowedForNodes;
    } else {
      labelsFontSize = config.initialLinkLabelsFontSize;
    }

    let svgLinkLabels = mainEl.selectAll('.link-group').selectAll('.link-label');
    svgLinkLabels
      .attr('font-size', labelsFontSize);
  }

  return state.viewGraph;
}

function genSvgGroups(g, groups, drag, onRenderViewReq) {
  let svgGroups = g.selectAll('.group')
      .data(groups, (d) => d._osid);

  let enterGroups = svgGroups.enter();

  let groupsContainers = 
    enterGroups
      .append('g')
        .attr('class', 'group')
        .attr('data-group-id', (d) => d._osid)
        .call(drag)
        .on('click', function (d) {
          console.log('click', d);
          d.isExpanded = !d.isExpanded;
          onRenderViewReq();
        });

  groupsContainers
    .append('rect')
      .attr('class', 'group-shape')
      .attr('rx', 8)
      .attr('ry', 8)
      .style('fill', function (_d, _i) { return 'lightblue'; })
  ;

  groupsContainers
    .append('text')
    .text(function(d) { 
      return d.name;
    })
    .attr('class', 'group-name')
    .attr('x', function(d) { 
      return (d.bounds.width() / 2);
    })
    .attr('y', function(_d) { 
      return 30;
    })
    .attr('dy', '.25em')
    .attr('text-anchor', 'middle')
    .attr('font-size', 20)
  ;

  svgGroups.exit()
    .remove();

  return svgGroups;
}
function calcViewGraph(graph, prevViewGraph) {
  let {groups, rejectedGroups} = calcGroupsAndRejectedGroups(graph.groups);
  let newClosedGroupNodes = calcClosedGroupsNodes(rejectedGroups, prevViewGraph.nodes);
  let {nodes, rejectedNodes} = calcNodesAndRejectedNodes(graph.nodes, graph.groups);
  nodes = R.concat(newClosedGroupNodes, nodes);

  let {links, rejectedSourceLinks, rejectedTargetLinks, rejectedBothLinks} =
    calcLinksAndRejectedLinks(graph.links, rejectedNodes);

  let newLinksForRejectedSource = 
    calcNewLinksForRejectedSource(rejectedSourceLinks, nodes, prevViewGraph.links);

  let newLinksForRejectedTarget =
    calcNewLinksForRejectedTarget(rejectedTargetLinks, nodes, prevViewGraph.links);

  let newLinksForRejectedBoth = 
    calcNewLinksForRejectedBoth(rejectedBothLinks, nodes, prevViewGraph.links);

  links = R.pipe(
    R.concat(newLinksForRejectedSource),
    R.concat(newLinksForRejectedTarget),
    R.concat(newLinksForRejectedBoth)
  )(links);

  return {
    nodes,
    links,
    groups
  };
}

function calcGroupsAndRejectedGroups(originalGroups) {
  let rejectedGroups = R.filter(R.propEq('isExpanded', false), originalGroups);
  let groups = R.reject(R.propEq('isExpanded', false), originalGroups);

  return { groups, rejectedGroups };
}

function calcClosedGroupsNodes(rejectedGroups, prevViewNodes) {
  return R.reduce((acc, group) => {
    let nodeId = `${group._osid}-group-node`;
    let prevNode = R.find(R.propEq('_osid', nodeId), prevViewNodes);
    if (prevNode) {
      return R.append(prevNode, acc);
    }

    return R.append({
      _osid: nodeId,
      _osmeta: {
        type: 'view_group',
        nodeId: group._osid,
      },
      width: 60,
      height: 40,
      name: group._osid
    }, acc);
  }, [], rejectedGroups);
}

function calcNodesAndRejectedNodes(originalNodes, originalGroups) {
  let rejectedNodes = [];
  let nodes = R.reject((node) => {
    let groupId = R.path(['_osmeta', 'groupId'], node);
    if (R.isNil(groupId)) { return false; }

    let group = R.find(R.propEq('_osid', groupId), originalGroups);
    if (R.isNil(group)) { return false; }

    if (group.isExpanded) { return false; } 

    rejectedNodes = R.append(node, rejectedNodes);
    return true;
  }, originalNodes);

  return { nodes, rejectedNodes };
}

function calcLinksAndRejectedLinks(originalLinks, rejectedNodes) {
  return R.reduce((acc, link) => {
    let sourceRejected = R.contains(link.source, rejectedNodes);
    let targetRejected = R.contains(link.target, rejectedNodes);

    if (sourceRejected && targetRejected) {
      acc = R.assoc('rejectedBothLinks', R.append(link, acc.rejectedBothLinks), acc);
      return acc;
    }

    if (sourceRejected) {
      acc = R.assoc('rejectedSourceLinks', R.append(link, acc.rejectedSourceLinks), acc);
      return acc;
    }

    if (targetRejected) {
      acc = R.assoc('rejectedTargetLinks', R.append(link, acc.rejectedTargetLinks), acc);
      return acc;
    }

    acc = R.assoc('links', R.append(link, acc.links), acc);
    return acc;
  }, 
  {links: [], rejectedSourceLinks: [], rejectedTargetLinks: [], rejectedBothLinks: [] }, 
  originalLinks);
}

function calcNewLinksForRejectedSource(rejectedSourceLinks, nodes, prevLinks) {
  let newLinksForRejectedSource = R.reduce((acc, link) => {
    let groupId = R.path(['_osmeta', 'groupId'], link.source);
    let groupNodeId = `${groupId}-group-node`;
    let newSource = R.find(R.propEq('_osid', groupNodeId), nodes);
    if (R.isNil(newSource)) { 
      throw 'error in new links for rejected source function';
    }

    let newLinkId = `${newSource._osid}:${link.target._osid}:rejected-source`;

    let existingLink = R.find(R.propEq('_osid', newLinkId), acc);
    if (existingLink) { 
      return acc;
    }

    let prevExistingLink = R.find(R.propEq('_osid', newLinkId), prevLinks);
    if (prevExistingLink) {
      return R.append(prevExistingLink, acc);
    }

    return R.append({
      source: newSource ,
      target: link.target,
      label: link.label,
      _osid: newLinkId    
    }, acc);
  }, [], rejectedSourceLinks);

  return newLinksForRejectedSource;
}

function calcNewLinksForRejectedTarget(rejectedLinks, nodes, prevLinks) {
  let newLinks = R.reduce((acc, link) => {
    let groupId = R.path(['_osmeta', 'groupId'], link.target);
    let groupNodeId = `${groupId}-group-node`;
    let newTarget = R.find(R.propEq('_osid', groupNodeId), nodes);
    if (R.isNil(newTarget)) { 
      throw 'error in new links for rejected target function';
    }

    let newLinkId = `${link.source._osid}:${newTarget._osid}:rejected-target`;

    let existingLink = R.find(R.propEq('_osid', newLinkId), acc);
    if (existingLink) { 
      return acc;
    }

    let prevExistingLink = R.find(R.propEq('_osid', newLinkId), prevLinks);
    if (prevExistingLink) {
      return R.append(prevExistingLink, acc);
    }

    return R.append({
      source: link.source ,
      target: newTarget,
      label: link.label,
      _osid: newLinkId
    }, acc);
  }, [], rejectedLinks);

  return newLinks;
}

function calcNewLinksForRejectedBoth(rejectedLinks, nodes, prevLinks) {
  let newLinks = R.reduce((acc, link) => {
    let targetHost = R.path(['_osmeta', 'groupId'], link.target);
    let sourceHost = R.path(['_osmeta', 'groupId'], link.source);
    let groupSourceNodeId = `${sourceHost}-group-node`;
    let groupTargetNodeId = `${targetHost}-group-node`;

    if (targetHost === sourceHost) {
      return acc; 
    }

    let newLinkId = `${sourceHost}:${targetHost}:groups-link`;
    let existingNewLink = R.find(R.propEq('_osid', newLinkId), acc);
    if (existingNewLink) {
      return acc;
    }

    let prevExistingLink = R.find(R.propEq('_osid', newLinkId), prevLinks);
    if (prevExistingLink) {
      return R.append(prevExistingLink, acc);
    }

    let newSource = R.find(R.propEq('_osid', groupSourceNodeId), nodes);
    let newTarget = R.find(R.propEq('_osid', groupTargetNodeId), nodes);

    let newLink = {
      source: newSource,
      target: newTarget,
      label: 'hosts link',
      _osid: newLinkId
    };

    return R.append(newLink, acc);
  }, [], rejectedLinks);

  return newLinks;
}
