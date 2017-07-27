/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { Inventory } from '/imports/api/inventories/inventories';
import { Cliques } from '/imports/api/cliques/cliques';
import { Links } from '/imports/api/links/links';
import { NodeHoverAttr } from '/imports/api/attributes_for_hover_on_data/attributes_for_hover_on_data';
import * as cola from 'webcola';
import { store } from '/imports/ui/store/store';
import { activateGraphTooltipWindow } from '/imports/ui/actions/graph-tooltip-window.actions';
import { closeGraphTooltipWindow } from '/imports/ui/actions/graph-tooltip-window.actions';
import { activateVedgeInfoWindow } from '/imports/ui/actions/vedge-info-window.actions';
import * as R from 'ramda';

let d3Graph = {
  color:'',

  zoomer:function(){
    var width = '100%',
      height = '100%';
    var xScale = d3.scale.linear()
        .domain([0,width]).range([0,width]);
    var yScale = d3.scale.linear()
        .domain([0,height]).range([0, height]);
    return d3.behavior.zoom().
    scaleExtent([0.1,10]).
    x(xScale).
    y(yScale).
    on('zoomstart', d3Graph.zoomstart).
    on('zoom', d3Graph.redraw);
  },

  svg:'',
  force:'',
  link:'',
  node:'',
  linkText:'',

  graph:{
    nodes:[],
    links:[],
  },

  zoomstart:function () {
    var node = d3Graph.svg.selectAll('.node');
    node.each(function(d) {
      d.selected = false;
      d.previouslySelected = false;
    });
    node.classed('selected', false);
  },

  /* depreacted - not used ?
  getGraphData:function(nodeId){

    var invNodes = Inventory.find({ 'type': 'instance', $and: [ { 'host': nodeId } ] });

    var edges = [];
    var nodes = [];

    invNodes.forEach(function(n){
      nodes =  n['Entities'];
      edges =  n['Relations'];
    });

    nodes.forEach(function(n){
      n.name = n.object_name;
    });

    var edges_new = [];
    edges.forEach(function(e) {
      var sourceNode = nodes.filter(function(n) { return n.id === e.from; })[0],
        targetNode = nodes.filter(function(n) { return n.id === e.to; })[0];

      edges_new.push({source: sourceNode, target: targetNode, value: 1,label: e.label,attributes: e.attributes});
    });
//any links with duplicate source and target get an incremented 'linknum'
    for (var i=0; i<edges_new.length; i++) {
      if (i != 0 &&
          edges_new[i].source == edges_new[i-1].source &&
          edges_new[i].target == edges_new[i-1].target) {

        edges_new[i].linknum = edges_new[i-1].linknum + 1;
      }
      else {edges_new[i].linknum = 1;}
    }
    //var graph = {};
    this.graph.nodes = nodes;
    this.graph.links = edges_new;

  },
  */

  getGraphDataByClique:function(nodeObjId){
    // Clique: one instance per graph. A focal point describing a node, and with links data.
    // TODO: findOne or .each.
    var cliques = Cliques.find({ focal_point: new Mongo.ObjectID(nodeObjId) }).fetch();


    var nodes = [];
    var edges_new = [];
    
    if (R.length(cliques) === 0) {
      return;
    }

    // CliquesLinks: All the links for a specific clique
    var cliquesLinks = [];
    cliques[0].links.forEach(function(n){
      cliquesLinks.push(n);
    });

    // LinksList = Map(Clique.links -> links collection)
    var linksList = Links.find({ _id: {$in: cliquesLinks}}).fetch();
    //console.log(linksList);

    // Create nodes from the links endpoints.
    // Nodes = link source & target (objectid)
    linksList.forEach(function(linkItem){
      nodes.push(linkItem['source']);
      nodes.push(linkItem['target']);
    });

    // NodesList = Nodes exapneded.
    var nodesList = Inventory.find({ _id: {$in: nodes}}).fetch();

    // Links list: expanend source/target nodes to create in memory data graph - links,nodes.
    linksList.forEach(function(linkItem){
      var sourceNode = nodesList.filter(function(n) { 
        return n._id._str === linkItem.source._str; 
      })[0];

      var targetNode = nodesList.filter(function(n) { 
        return n._id._str === linkItem.target._str; 
      })[0];

      edges_new.push({
        source: sourceNode, 
        target: targetNode, 
        value: 1,
        label: linkItem.link_name,
        attributes: linkItem
      });

    });
    
    // Expend nodeslist to include linked attributes.
    nodesList.forEach(function(nodeItem){
      nodeItem.attributes = [];
      var attrHoverFields = NodeHoverAttr.find({ 'type': nodeItem['type']}).fetch();
      if(attrHoverFields.length){
        attrHoverFields[0].attributes.forEach(function(field){
          if(nodeItem[field]){
            var object = {};
            object[field] = nodeItem[field];
            nodeItem.attributes.push(object);
          }
        });
      }
    });

    this.graph.nodes = nodesList;
    this.graph.links = edges_new;

  },

  createGraphData: function (width, height){
    //var self = this;
    //var width = 500;
    //var height = 900;

    this.color = d3.scale.category20();
    /*
     this.svg = d3.select('#dgraphid').append('svg')
     .attr('width', '100%')
     .attr('height', '100%')
     .attr('pointer-events', 'all')
     //.attr('transform', 'translate(250,250) scale(0.3)')
     .call(d3.behavior.zoom().on('zoom', this.redraw))
     .append('svg:g');

     //.append('g');

     this.force = cola.d3adaptor().convergenceThreshold(0.1)
     //.linkDistance(200)
     .size([width, height]);
     */
    //var focused = null;

    this.force = cola.d3adaptor().convergenceThreshold(0.1)
    //.linkDistance(200)
        .size([width, height]);

    var outer = d3.select('#dgraphid')
        .append('svg')
        .attr({ 
          width: '100%', 
          height: '100%', 
          'pointer-events': 'all', 
          class: 'os-d3-graph' 
        });

    outer.append('rect')
        .attr({ class: 'background', width: '100%', height: '100%' })
        .call(this.zoomer());
        /*.call(d3.behavior.zoom()
            .on('zoom', function(d) {
            d3Graph.svg.attr('transform', 'translate(' + d3.event.translate + ')' + ' scale(' + d3.event.scale + ')');
        }))*/
        //.on('mouseover', function () { focused = this; });

    //d3.select('body').on('keydown', function () { d3.select(focused); /* then do something with it here */ });
    //d3.select('#dgraphid').on('keydown', d3Graph.keydown());

    let scale = 0.5;

    this.svg = outer
        .append('g')
        //.attr('transform', 'translate(250,250) scale(0.3)');
        .attr('transform', 'translate(250,250) scale(' + scale.toString() + ')');

    let fontSize = Math.floor(16 / scale);
    d3Graph.svg.selectAll('.link-group text')
      .style('font-size', fontSize + 'px');
    d3Graph.svg.selectAll('.node text')
      .style('font-size', fontSize + 'px');

  },

  redraw: function(){
      //console.log('here', d3.event.translate, d3.event.scale);

    d3Graph.svg.attr('transform',
        'translate(' + d3.event.translate + ')'
        + ' scale(' + d3.event.scale + ')');

    let fontSize = Math.floor(16 / d3.event.scale);
    d3Graph.svg.selectAll('.link-group text')
      .style('font-size', fontSize + 'px');
    d3Graph.svg.selectAll('.node text')
      .style('font-size', fontSize + 'px');

  },

  updateNetworkGraph:function (){
    var self = this;

    if (R.isNil(this.svg)) {
      return;
    }

    this.svg.selectAll('g').remove();
    //this.svg.exit().remove();

    this.force
        .nodes(this.graph.nodes)
        .links(this.graph.links)
        .symmetricDiffLinkLengths(250)
        //.jaccardLinkLengths(300)
        //.jaccardLinkLengths(80,0.7)
        .handleDisconnected(true)
        .avoidOverlaps(true)
        .start(50, 100, 200);

    /*
     this.force
     .on('dragstart', function (d) { d3.event.sourceEvent.stopPropagation(); d3.select(this).classed('dragging', true); } )
     .on('drag', function (d) { d3.select(this).attr('cx', d.x = d3.event.x).attr('cy', d.y = d3.event.y); } )
     .on('dragend', function (d) { d3.select(this).classed('dragging', false); });
     */


    // Define the div for the tooltip

    //svg.exit().remove();
    //graph.constraints = [{'axis':'y', 'left':0, 'right':1, 'gap':25},];

    //.start(10,15,20);
    /*var path = svg.append('svg:g')
     .selectAll('path')
     .data(force.links())
     .enter().append('svg:path')
     .attr('class', 'link');;
     */
    var link = this.svg.selectAll('.link')
      .data(this.force.links())
      .enter()
      .append('g')
      .attr('class', 'link-group')
      .append('line')
      .attr('class', 'link')
      .style('stroke-width', function(_d) { return 3; })
      //.style('stroke-width', function(d) { return Math.sqrt(d.stroke); })
      .attr('stroke', function (d) {
        if(d.attributes.state == 'error'){
          self.blinkLink(d);
          return 'red';
        }
        else if(d.attributes.state == 'warn'){
          self.blinkLink(d);
          return 'orange';
        }
        else if(d.source.level === d.target.level) {
          return self.color(d.source.level);
        }
        else {
          return self.color(d.level);
          //d3.select(this).classed('different-groups', true);
        }
      });
    /*.style('stroke', function(d) {
     if(d.label == 'net-103'){
     self.blinkLink(d);
     return 'red';
     }
     //return 'red';
     //return self.color(d.level);
     })*/

    var linkText = this.svg.selectAll('.link-group')
      .append('text')
      .data(this.force.links())
      .text(function(d) { return d.label; })
      .attr('x', function(d) { return (d.source.x + (d.target.x - d.source.x) * 0.5); })
      .attr('y', function(d) { return (d.source.y + (d.target.y - d.source.y) * 0.5); })
      .attr('dy', '.25em')
      .attr('text-anchor', 'right')
      .on('mouseover', function(d) {
        store.dispatch(activateGraphTooltipWindow(
          d.label, 
          d.attributes,
          d3.event.pageX,
          d3.event.pageY
        ));
      })
      .on('mouseout', function(_d) {
        store.dispatch(closeGraphTooltipWindow());
      });

    var node = this.svg.selectAll('.node')
      .data(this.force.nodes())
      .enter().append('g')
      .attr('class', 'node')
      .call(this.force.drag);

    // A map from group ID to image URL.
    var imageByGroup = {
      'instance': 'ic_computer_black_48dp_2x.png',
      'pnic': 'ic_dns_black_48dp_2x.png',
      'vconnector': 'ic_settings_input_composite_black_48dp_2x.png',
      // 'network': 'ic_cloud_queue_black_48dp_2x.png',
      'network': 'ic_cloud_queue_black_48dp_2x.png',
      'vedge': 'ic_gamepad_black_48dp_2x.png',
      'vservice': 'ic_storage_black_48dp_2x.png',
      'vnic': 'ic_settings_input_hdmi_black_48dp_2x.png',
      'otep':'ic_keyboard_return_black_48dp_2x.png',
      'default':'ic_lens_black_48dp_2x.png'
    };

    node.append('image')
    //.attr('xlink:href', 'https://github.com/favicon.ico')
        .attr('xlink:href', function(d) {
          if(imageByGroup[d.type]){
            return `/${imageByGroup[d.type]}`;
          }
          else{
            return `/${imageByGroup['default']}`;
          }

        })
        .attr('x', -8)
        .attr('y', -8)
        .attr('width', 36)
        .attr('height', 36)
        //node.append('circle')
        .attr('class', 'node')
        //.attr('r', function(d){return 13;})
        .on('mouseover', function(d) {
          store.dispatch(activateGraphTooltipWindow(
            d.name, 
            d.attributes,
            d3.event.pageX,
            d3.event.pageY));
        })
        .on('mouseout', function(_d) {
          store.dispatch(closeGraphTooltipWindow());
        })
        .on('click', function(d) {
          if (d.type === 'vedge') {
            store.dispatch(activateVedgeInfoWindow(
              d,
              d3.event.pageX,
              d3.event.pageY));
          }
        })
        .style('fill', function(d) {
          if(d.state == 'error'){
            self.blinkNode(d);
            return 'red';
          }
          return self.color(d.group);
        })
        .call(this.force.drag);


    /*
     .each(function() {
     var sel = d3.select(this);
     var state = false;
     sel.on('dblclick', function () {
     state = !state;
     if (state) {
     sel.style('fill', 'black');
     } else {
     sel.style('fill', function (d) {
     return d.colr;
     });
     }
     });
     });
     */

    node.append('text')
        .attr('dx', 0)
        .attr('dy', 40)
        .text(function(d) { return d.object_name; });


    this.force.on('tick', function() {
      link.attr('x1', function(d) { return d.source.x; })
          .attr('y1', function(d) { return d.source.y; })
          .attr('x2', function(d) { return d.target.x; })
          .attr('y2', function(d) { return d.target.y; });
      /*
       .attr('dr1', function(d) { return 75/d.source.linknum; })
       .attr('dr2', function(d) { return 75/d.target.linknum; });
       */

      node.attr('transform', function(d) { 
        return 'translate(' + d.x + ',' + d.y + ')'; 
      });

      linkText
          .attr('x', function(d) { 
            return (d.source.x + (d.target.x - d.source.x) * 0.5); 
          })
          .attr('y', function(d) { 
            return (d.source.y + (d.target.y - d.source.y) * 0.5); 
          });
    });

  },

  centerview: function () {
    // Center the view on the molecule(s) and scale it so that everything
    // fits in the window
    var width = 500;
    var height = 500;

    if (this.graph === null) return;

    var nodes = this.graph.nodes;

    //no molecules, nothing to do
    if (nodes.length === 0) return;

    // Get the bounding box
    var min_x = d3.min(nodes.map(function(d) {return d.x;}));
    var min_y = d3.min(nodes.map(function(d) {return d.y;}));

    var max_x = d3.max(nodes.map(function(d) {return d.x;}));
    var max_y = d3.max(nodes.map(function(d) {return d.y;}));


    // The width and the height of the graph
    var mol_width = max_x - min_x;
    var mol_height = max_y - min_y;

    // how much larger the drawing area is than the width and the height
    var width_ratio = width / mol_width;
    var height_ratio = height / mol_height;

    // we need to fit it in both directions, so we scale according to
    // the direction in which we need to shrink the most
    var min_ratio = Math.min(width_ratio, height_ratio) * 0.8;

    // the new dimensions of the molecule
    var new_mol_width = mol_width * min_ratio;
    var new_mol_height = mol_height * min_ratio;

    // translate so that it's in the center of the window
    var x_trans = -(min_x) * min_ratio + (width - new_mol_width) / 2;
    var y_trans = -(min_y) * min_ratio + (height - new_mol_height) / 2;


    // do the actual moving
    d3Graph.svg.attr('transform',
        'translate(' + [x_trans, y_trans] + ')' + ' scale(' + min_ratio + ')');

    // tell the zoomer what we did so that next we zoom, it uses the
    // transformation we entered here
    //d3Graph.zoomer.translate([x_trans, y_trans ]);
    //d3Graph.zoomer.scale(min_ratio);
  },
  
  keydown:function() {
/*
      shiftKey = d3.event.shiftKey || d3.event.metaKey;
      ctrlKey = d3.event.ctrlKey;
*/
    if(d3.event===null) return;

    console.log('d3.event', d3.event);

    if (d3.event.keyCode == 67) {   //the 'c' key
      this.centerview();
    }

  },

  blinkNode: function(node){
    var nodeList = this.svg.selectAll('.node');
    var selected = nodeList.filter(function (d, _i) {
      return d.id == node.id;
      //return d.name != findFromParent;
    });
    selected.forEach(function(n){
      for (var i = 0; i != 30; i++) {
        $(n[1]).fadeTo('slow', 0.1).fadeTo('slow', 5.0);
      }
    });
  },

  blinkLink: function(link){
    var linkList = this.svg.selectAll('.link');
    var selected = linkList.filter(function (d, _i) {
      return d.label == link.label;
      //return d.id == link.id;
      //return d.name != findFromParent;
    });
    selected.forEach(function(n){
      for (var i = 0; i != 30; i++) {
        $(n[0]).fadeTo('slow', 0.1).fadeTo('slow', 5.0);
      }
    });
  },

  tick:function(obj){
    obj.link.attr('x1', function(d) { return d.source.x; })
      .attr('y1', function(d) { return d.source.y; })
      .attr('x2', function(d) { return d.target.x; })
      .attr('y2', function(d) { return d.target.y; });

    obj.node.attr('transform', function(d) { 
      return 'translate(' + d.x + ',' + d.y + ')'; 
    });

    obj.linkText
      .attr('x', function(d) { 
        return (d.source.x + (d.target.x - d.source.x) * 0.5); 
      })
      .attr('y', function(d) { 
        return (d.source.y + (d.target.y - d.source.y) * 0.5); 
      });
  }
};

export { d3Graph };
