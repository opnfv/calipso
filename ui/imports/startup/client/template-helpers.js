/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import * as R from 'ramda';
import * as utils from '/imports/lib/utilities';
import { Counter } from 'meteor/natestrauser:publish-performant-counts';

Template.registerHelper('asHash', function (params) {
  return params.hash;
});

Template.registerHelper('idToStr', utils.idToStr);

Template.registerHelper('rPath', function (source, pathStr) {
  let path = R.split('.', pathStr);
  return R.path(path, source);
});

Template.registerHelper('asArray', function (val) {
  return [val];
});

Template.registerHelper('countOf', function (name) {
  if (name) {
    return Counter.get(name);
  }
});


Template.registerHelper('jsonAsString', function (val) {
  let str = JSON.stringify(val, null, 4);
  return str;
});
