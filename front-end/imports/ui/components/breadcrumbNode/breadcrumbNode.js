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
 * Template Component: breadcrumbNode
 */

import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';

import './breadcrumbNode.html';

Template.breadcrumbNode.onCreated(function () {
  let instance = this;
  instance.state = new ReactiveDict();

  instance.autorun(function () {
    let data = Template.currentData();
    new SimpleSchema({
      node: { type: Object, blackbox: true },
      onClick: { type: Function },
    }).validate(data);
  });

});

Template.breadcrumbNode.helpers({
});

Template.breadcrumbNode.events({
  'click': function(event, instance) {
    event.stopPropagation();
    event.preventDefault();
    
    instance.data.onClick();
  }
});
