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
 * Template Component: FlowGraph 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
// We import d3 v4 not into d3 because old code network visualization use globaly d3 v3.
import * as d3v4 from 'd3';
import * as R from 'ramda';
import { Statistics } from '/imports/api/statistics/statistics';
import { createGraphQuerySchema } from '/imports/api/statistics/helpers';
//import * as BSON from 'bson';
        
import './flow-graph.html';     
    
/*  
 * Lifecycles
 */   
  
Template.FlowGraph.onCreated(function() {
  let instance = this;
  
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    environment: instance.data.environment,
    object_id: instance.data.object_id,
    type: instance.data.type,
    flowType: instance.data.flowType,
    sourceMacAddress: instance.data.sourceMacAddress,
    destinationMacAddress: instance.data.destinationMacAddress,
    sourceIPv4Address: instance.data.sourceIPv4Address,
    destinationIPv4Address: instance.data.destinationIPv4Address,
    simulateGraph: instance.data.simulateGraph,
    yScale: instance.data.yScale,
    timeDeltaNano: 0,
    timeDeltaSeconds: 0
  });

  instance.autorun(() => {
    new SimpleSchema({
      env: { type: String },
      object_id: { type: String },
      type: { type: String },
      flowType: { type: String },
      sourceMacAddress: { type: String, optional: true },
      destinationMacAddress: { type: String, optional: true },
      sourceIPv4Address: { type: String, optional: true },
      destinationIPv4Address: { type: String, optional: true },
      simulateGraph: { type: Boolean, optional: true },
      yScale: { type: Number, optional: true },
      startDateTime: { type: String, optional: true },
    }).validate(Template.currentData());

    let data = Template.currentData();

    instance.state.set('environment', data.env);
    instance.state.set('object_id', data.object_id);
    instance.state.set('type', data.type);
    instance.state.set('flowType', data.flowType);
    instance.state.set('sourceMacAddress', data.sourceMacAddress);
    instance.state.set('destinationMacAddress', data.destinationMacAddress);
    instance.state.set('sourceIPv4Address', data.sourceIPv4Address);
    instance.state.set('destinationIPv4Address', data.destinationIPv4Address);
    instance.state.set('simulateGraph', data.simulateGraph);
    instance.state.set('yScale', data.yScale);

    let startDateTime = R.ifElse(R.isNil, (_p) => { return moment();}, moment)(data.startDateTime);
    let deltaSeconds = moment().diff(startDateTime, 'seconds');
    //let deltaNano = deltaMili * 1000000;
    //instance.state.set('timeDeltaNano', deltaNano);
    instance.state.set('timeDeltaSeconds', deltaSeconds);

    //let timeStart = startDateTime.valueOf() * 1000000;
    let timeStart = startDateTime.unix();

    //debugger;
    // debug purpose: 
    //let timeStart = 1486661034810432900;//  1486661034810432945;
    //let timeDeltaNano = Date.now() * 1000000 - timeStart;
    //instance.state.set('timeDeltaNano', timeDeltaNano);
    // debug end

    instance.subscribe('statistics!graph-frames', {
      env: data.env, 
      object_id: data.object_id, 
      type: data.type,
      flowType: data.flowType, 
      timeStart: timeStart,
      sourceMacAddress: data.sourceMacAddress,
      destinationMacAddress: data.destinationMacAddress,
      sourceIPv4Address: data.sourceIPv4Address,
      destinationIPv4Address: data.destinationIPv4Address
    });
  });

});  

Template.FlowGraph.onDestroyed(function () {
  (function (d3) {
    let instance = Template.instance();
    let graphContainer = instance.$('.sm-graph');
    var svg = d3.select(graphContainer[0]);

    svg.interrupt();
    var lineSvg = svg.select('g g path.line');
    lineSvg.interrupt();
  })(d3v4);
});

Template.FlowGraph.rendered = function() {
  let instance = Template.instance();

  instance.autorun(() => {

    let environment = instance.state.get('environment');
    let object_id = instance.state.get('object_id');
    let type = instance.state.get('type');
    let flowType = instance.state.get('flowType');
    let sourceMacAddress = instance.state.get('sourceMacAddress');
    let destinationMacAddress = instance.state.get('destinationMacAddress');
    let sourceIPv4Address = instance.state.get('sourceIPv4Address');
    let destinationIPv4Address = instance.state.get('destinationIPv4Address');
    let simulateGraph = instance.state.get('simulateGraph');
    let yScale = instance.state.get('yScale');
    //let timeDeltaNano = instance.state.get('timeDeltaNano');
    let timeDeltaSeconds = instance.state.get('timeDeltaSeconds');

    let graphContainer = instance.$('.sm-graph');

    generateAllGraph(
      d3v4,
      graphContainer,
      environment,
      object_id,
      type,
      flowType,
      sourceMacAddress,
      destinationMacAddress,
      sourceIPv4Address,
      destinationIPv4Address,
      simulateGraph,
      yScale,
      //timeDeltaNano
      timeDeltaSeconds
    );

  });
};  

/*
 * Events
 */

Template.FlowGraph.events({
});
   
/*  
 * Helpers
 */

Template.FlowGraph.helpers({    
});

function generateAllGraph(
  d3,
  graphContainer,
  environment,
  object_id,
  type,
  flowType,
  sourceMacAddress,
  destinationMacAddress,
  sourceIPv4Address,
  destinationIPv4Address,
  simulateGraph,
  yScale,
  //timeDeltaNano) {
  timeDeltaSeconds) {

  let dataRetrivalFn = createDataRetrivalFn(
    d3,
    simulateGraph,
    environment, 
    object_id,
    type,
    flowType, 
    sourceMacAddress,
    destinationMacAddress,
    sourceIPv4Address,
    destinationIPv4Address,
    yScale
  );

  generateGraph(
    d3,
    dataRetrivalFn,
    graphContainer,
    //timeDeltaNano,
    timeDeltaSeconds,
    yScale
  );
}

function createDataRetrivalFn(
  d3,
  simulateGraph,
  environment, 
  object_id,
  type,
  flowType, 
  sourceMacAddress,
  destinationMacAddress,
  sourceIPv4Address,
  destinationIPv4Address,
  yScale
) {

  if (simulateGraph) {
    let random = d3.randomNormal(0, yScale);
    return function (_start, _end) {
      return {
        averageThroughput: random()
      };
    };
  }

  //return function (startNano, endNano) {
  return function (startSeconds, endSeconds) {
    //let startBson = BSON.Long.fromNumber(startNano);
    //let endBson = BSON.Long.fromNumber(endNano);
    //let startBson = startNano;
    //let endBson = endNano;

    let query = createGraphQuerySchema(
      environment, 
      object_id,
      type,
      flowType, 
      //startBson,
      //endBson,
      startSeconds,
      endSeconds,
      sourceMacAddress,
      destinationMacAddress,
      sourceIPv4Address,
      destinationIPv4Address);

    return Statistics.findOne(query);
  };

/*
  return function (timeStart, timeEnd, callback) {
    Meteor.call('statistics!graph-frames', { 
      env: environment, 
      object_id: object_id, 
      type: type, 
      flowType: flowType, 
      timeStart: timeStart, 
      timeEnd: timeEnd, 
      sourceMacAddress: sourceMacAddress, 
      destinationMacAddress: destinationMacAddress, 
      sourceIPv4Address: sourceIPv4Address, 
      destinationIPv4Address: destinationIPv4Address 
    }, (_err, res) => { 
      callback(res);
    });

  };
  */
}

function generateGraph(
  d3,
  dataRetrivalFn,
  graphContainer,
  //timeDeltaNano,
  timeDeltaSeconds,
  yScale
) { 
  var n = 40;

  let data = d3.range(n).map(R.always(0));
  let svg = d3.select(graphContainer[0]);
  let margin = {top: 20, right: 20, bottom: 20, left: 80};
  let width = +svg.attr('width') - margin.left - margin.right;
  let height = +svg.attr('height') - margin.top - margin.bottom;
    
  svg.interrupt();
  var lineSvg = svg.select('g g path.line');
  lineSvg.interrupt();

  svg.select('g').remove();

  var g = svg.append('g').attr(
      'transform', 'translate(' + margin.left + ',' + margin.top + ')');

  var x = d3.scaleLinear()
    .domain([0, n - 1])
    .range([0, width]);

  var y = d3.scaleLinear()
    .domain([0, yScale])
    .range([height, 0]);

  var line = d3.line()
    .x(function(d, i) { return x(i); })
    .y(function(d, _i) { return y(d); });

  g.append('defs').append('clipPath')
    .attr('id', 'clip')
  .append('rect')
    .attr('width', width)
    .attr('height', height);

  g.append('g')
    .attr('class', 'axis axis--x')
    .attr('transform', 'translate(0,' + y(0) + ')')
    .call(d3.axisBottom(x));

  g.append('g')
    .attr('class', 'axis axis--y')
    .call(d3.axisLeft(y));

  g.append('g')
    .attr('clip-path', 'url(#clip)')
  .append('path')
    .datum(data)
    .attr('class', 'line')
  .transition()
    .duration(500)
    .ease(d3.easeLinear)
    .on('start', tick);

  //let timeStart = (Date.now() * 1000000) - timeDeltaNano;
  let timeStart = moment().unix() - timeDeltaSeconds;
  let timeEnd;
  let dataPoint;
  let lastDataPoint = 0;

  function tick() {
    //timeEnd = (Date.now() * 1000000) - timeDeltaNano;
    timeEnd = (moment().unix()) - timeDeltaSeconds;

    let statItem = dataRetrivalFn(timeStart, timeEnd);

    if (!R.isNil(statItem)) {
      dataPoint = statItem.averageThroughput;
    } else {
      dataPoint = lastDataPoint;
    }

    data.push(dataPoint);

    //timeStart = timeEnd - (4 * 1000000000);
    timeStart = timeEnd;

    // Redraw the line.
    d3.select(this)
        .attr('d', line)
        .attr('transform', null);

    // Slide it to the left.
    d3.active(this)
        .attr('transform', 'translate(' + x(-1) + ',0)')
      .transition()
        .on('start', tick);

    // Pop the old data point off the front.
    data.shift();

    lastDataPoint = dataPoint;
  }
}
