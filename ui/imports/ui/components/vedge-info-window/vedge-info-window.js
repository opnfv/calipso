/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: VedgeInfoWindow 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
//import { VedgeFlows } from '/imports/api/vedge_flows/vedge_flows';
import * as R from 'ramda';
//import * as moment from 'moment';
        
import '/imports/ui/components/flow-graph/flow-graph';
import '/imports/ui/components/time-selection-widget/time-selection-widget';
import './vedge-info-window.html';     
    
/*  
 * Lifecycles
 */   
  
Template.VedgeInfoWindow.onCreated(function() {
  let instance = this;
  
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    showMessage: false,
    messageType: null,
    message: null,
    environment: null,
    object_id: null,
    flowTypes: [],
    name: null,
    srcMacAddresses: [],
    dstMacAddresses: [],
    srcIPv4Addresses: [],
    dstIPv4Addresses: [],
    selectedFlowType: null,
    selectedSrcMacAddress: null,
    selectedDstMacAddress: null,
    selectedSrcIPv4Address: null,
    selectedDstIPv4Address: null,
    simulateGraph: false,
    show: false,
    yScale: 5000000,
    startDateTime: null
  });

  instance.autorun(() => {
    new SimpleSchema({
      environment: { type: String },
      object_id: { type: String },
      name: { type: String },
      left: { type: Number },
      top: { type: Number },
      show: { type: Boolean },
      onCloseRequested: { type: Function }
    }).validate(Template.currentData());

    instance.state.set('show', Template.currentData().show);
    instance.state.set('environment', Template.currentData().environment);
    instance.state.set('object_id', Template.currentData().object_id);
  });

  instance.autorun(() => {
    let environment = instance.state.get('environment');
    let object_id = instance.state.get('object_id');
    let flowType = instance.state.get('selectedFlowType');

    Meteor.call('statistics.flowTypes?env&object_id&type', { 
      env: environment,
      object_id: object_id,
      type: 'vedge_flows'
    }, (err, res) => {
      if (! R.isNil(err)) {
        showMessage(instance, 'danger', 
          'error in query for: flowTypes' + '\n' + err);
        return;
      }

      let flowTypes = R.pipe(
        R.map(R.prop('flowType')),
        R.map((name) => { return { name: name }; })
      )(res);
      instance.state.set('flowTypes', flowTypes);
    });

    switch (flowType) {
    case 'L2':
      fetchL2Addressess(
        environment, 
        object_id, 
        flowType,
        instance
      );
      break;

    case 'L3':
      fetchL3Addressess(
        environment, 
        object_id,
        flowType,
        instance
      );
      break;


    default:
      break;
    }
  });
});  

Template.VedgeInfoWindow.rendered = function() {
  this.$('.sm-start-datetime-group').datetimepicker({
    format: 'YYYY-MM-DD HH:mm'
  });
};  

/*
 * Events
 */

Template.VedgeInfoWindow.events({
  'click .sm-close-button': function (event, instance) {
    event.stopPropagation();
    instance.data.onCloseRequested();
  },

  'change .sm-flow-type-select': function (event, instance) {
    event.stopPropagation();
    event.preventDefault();

    let selections = R.map(function (optionEl) {
      return optionEl.value;
    }, event.target.selectedOptions);

    instance.state.set('selectedFlowType', selections[0]);
  },

  'change .sm-source-mac-address-select': function (event, instance) {
    event.stopPropagation();
    event.preventDefault();

    let selections = R.map(function (optionEl) {
      return optionEl.value;
    }, event.target.selectedOptions);

    instance.state.set('selectedSrcMacAddress', selections[0]);
  },

  'change .sm-destination-mac-address-select': function (event, instance) {
    event.stopPropagation();
    event.preventDefault();

    let selections = R.map(function (optionEl) {
      return optionEl.value;
    }, event.target.selectedOptions);

    instance.state.set('selectedDstMacAddress', selections[0]);
  },

  'click .sm-simulate-graph': function (event, instance) {
    let element = instance.$('.sm-simulate-graph')[0];
    instance.state.set('simulateGraph', element.checked);
  },

  'input .sm-y-scale-input': function (event, instance) {
    let element = instance.$('.sm-y-scale-input')[0];
    let val = R.ifElse(isNaN, R.always(5000000), Number)(element.value);
    instance.state.set('yScale', val);
  },

  'dp.change .sm-start-datetime-group': function (event, instance) {
    let element = instance.$('.sm-start-datetime')[0];
    //let startDateTime = moment(element.value);
    instance.state.set('startDateTime', element.value);
  }
});
   
/*  
 * Helpers
 */

Template.VedgeInfoWindow.helpers({    
  flowTypes: function () {
    let instance = Template.instance();
    return instance.state.get('flowTypes');
  },

  srcMacAddresses: function () {
    let instance = Template.instance();
    return instance.state.get('srcMacAddresses');
  },

  dstMacAddresses: function () {
    let instance = Template.instance();
    return instance.state.get('dstMacAddresses');
  },

  srcIPv4Addresses: function () {
    let instance = Template.instance();
    return instance.state.get('srcIPv4Addresses');
  },

  dstIPv4Addresses: function () {
    let instance = Template.instance();
    return instance.state.get('dstIPv4Addresses');
  },

  selectedFlowType: function () {
    let instance = Template.instance();
    return instance.state.get('selectedFlowType');
  },

  is: function (src, trg) {
    return src === trg;
  },

  isShow: function () {
    let instance = Template.instance();
    return instance.state.get('show');
  },

  isShowGraph: function () {
    let instance = Template.instance();

    let show = instance.state.get('show');
    if (! show) { return false; }

    let info = {
      env: instance.state.get('environment'),
      object_id: instance.state.get('object_id'),
      flowType: instance.state.get('selectedFlowType'),
      sourceMacAddress: instance.state.get('selectedSrcMacAddress'),
      destinationMacAddress: instance.state.get('selectedDstMacAddress'),
      sourceIPv4Address: instance.state.get('selectedSrcIPv4Address'),
      destinationIPv4Address: instance.state.get('selectedDstIPv4Address')
    };

    if (R.any(R.either(R.isNil, R.isEmpty))([info.env, info.object_id, info.flowType])) {
      return false;
    }

    let sourceDestVals = R.cond([
      [R.equals('L2'), R.always([info.sourceMacAddress, info.destinationMacAddress])],
      [R.equals('L3'), R.always([info.sourceIPv4Address, info.destinationIPv4Address])]
    ])(info.flowType);

    if (R.any(R.either(R.isNil, R.isEmpty))(sourceDestVals)) { 
      return false;
    }

    return true;
  },

  argsFlowGraph: function () {
    let instance = Template.instance();

    return {
      env: instance.state.get('environment'),
      object_id: instance.state.get('object_id'),
      type: 'vedge_flows',
      flowType: instance.state.get('selectedFlowType'),
      sourceMacAddress: instance.state.get('selectedSrcMacAddress'),
      destinationMacAddress: instance.state.get('selectedDstMacAddress'),
      sourceIPv4Address: instance.state.get('selectedSrcIPv4Address'),
      destinationIPv4Address: instance.state.get('selectedDstIPv4Address'),
      simulateGraph: instance.state.get('simulateGraph'),
      yScale: instance.state.get('yScale'),
      startDateTime: instance.state.get('startDateTime')
    };
  },

  showMessage: function () {
    let instance = Template.instance();
    return instance.state.get('showMessage');
  },

  message: function () {
    let instance = Template.instance();
    return instance.state.get('message');
  },

  messageType: function () {
    let instance = Template.instance();
    return instance.state.get('messageType');
  },
});

function showMessage(instance, type, message) {
  instance.state.set('showMessage', true);
  instance.state.set('messageType', type);
  instance.state.set('message', message);
}

function fetchL2Addressess(
  environment, 
  id, 
  flowType,
  instance) {

  Meteor.call('statistics.srcMacAddresses?env&object_id&type&flowType', {
    env: environment,
    object_id: id,
    type: 'vedge_flows',
    flowType: flowType
  }, (err, res) => {
    if (!R.isNil(err)) { 
      showMessage(instance, 'danger', 'error in query for: srcMacAddresses');
      return; 
    }

    let addresses = R.map((address) => { return address.sourceMacAddress; } )(res);
    instance.state.set('srcMacAddresses', addresses);
  });

  Meteor.call('statistics.dstMacAddresses?env&object_id&type&flowType', {
    env: environment,
    object_id: id,
    type: 'vedge_flows',
    flowType: flowType
  }, (err, res) => {
    if (!R.isNil(err)) { 
      showMessage(instance, 'danger', 
        `error in query for: dstMacAddresses
        message: ${err.message}` );
      return; 
    }

    let addresses = R.map((address) => { 
      return address.destinationMacAddress; 
    })(res);
    instance.state.set('dstMacAddresses', addresses);
  });
}

function fetchL3Addressess(
  environment, 
  id, 
  flowType,
  instance) {

  Meteor.call('statistics.srcIPv4Addresses?env&object_id&type&flowType', {
    env: environment,
    object_id: id,
    type: 'vedge_flows',
    flowType: flowType
  }, (err, res) => {
    if (!R.isNil(err)) { 
      showMessage(instance, 'danger', 'error in query for: src ip addresses');
      return; 
    }

    let addresses = R.map((address) => { return address.sourceIPv4Address; } )(res);
    instance.state.set('srcIPv4Addresses', addresses);
  });

  Meteor.call('statistics.dstIPv4Addresses?env&object_id&type&flowType', {
    env: environment,
    object_id: id,
    type: 'vedge_flows',
    flowType: flowType
  }, (err, res) => {
    if (!R.isNil(err)) { 
      showMessage(instance, 'danger', 'error in query for: dst ip addresses');
      return; 
    }

    let addresses = R.map((address) => { return address.destinationIPv4Address; } )(res);
    instance.state.set('dstIPv4Addresses', addresses);
  });
}
