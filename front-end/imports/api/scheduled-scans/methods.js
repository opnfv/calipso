///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import { ValidatedMethod } from 'meteor/mdg:validated-method';
import * as R from 'ramda';

import { ScheduledScans } from './scheduled-scans';

export const insert = new ValidatedMethod({
  name: 'scheduled-scans.insert',
  validate: ScheduledScans.simpleSchema()
    .pick([
      'environment',
      'object_id',
      'log_level',
      'clear',
      'loglevel',
      'scan_only_inventory',
      'scan_only_links',
      'scan_only_cliques',
      'es_index',
      'freq',
    ]).validator({ clean: true, filter: false }),
  run({
    environment,
    object_id,
    log_level,
    clear,
    loglevel,
    scan_only_inventory,
    scan_only_links,
    scan_only_cliques,
    es_index,
    freq,
  }) {
    let scan = ScheduledScans.schema.clean({ });

    scan = R.merge(scan, {
      environment,
      object_id,
      log_level,
      clear,
      loglevel,
      scan_only_inventory,
      scan_only_links,
      scan_only_cliques,
      es_index,
      freq, 
      submit_timestamp: Date.now()
    });

    ScheduledScans.insert(scan);
  },

});

export const update = new ValidatedMethod({
  name: 'scheduled_scans.update',
  validate: ScheduledScans.simpleSchema()
    .pick([
      '_id',
      'environment',
      'object_id',
      'log_level',
      'clear',
      'loglevel',
      'scan_only_inventory',
      'scan_only_links',
      'scan_only_cliques',
      'es_index',
      'freq',
    ]).validator({ clean: true, filter: false }),
  run({
    _id,
    environment,
    object_id,
    log_level,
    clear,
    loglevel,
    scan_only_inventory,
    scan_only_links,
    scan_only_cliques,
    es_index,
    freq,
  }) {
    let item = ScheduledScans.findOne({ _id: _id });
    console.log('scheduled scan for update: ', item);

    item = R.merge(R.pick([
      'environment',
      'object_id',
      'log_level',
      'clear',
      'loglevel',
      'scan_only_inventory',
      'scan_only_links',
      'scan_only_cliques',
      'es_index',
      'submit_timestamp', 
      'freq',
    ], item), {
      environment,
      object_id,
      log_level,
      clear,
      loglevel,
      scan_only_inventory,
      scan_only_links,
      scan_only_cliques,
      es_index,
      freq,
      submit_timestamp: Date.now()
    });

    ScheduledScans.update({ _id: _id }, { $set: item });
  }
});

export const remove = new ValidatedMethod({
  name: 'scheduled_scans.remove',
  validate: ScheduledScans.simpleSchema()
    .pick([
      '_id',
    ]).validator({ clean: true, filter: false }),
  run({
    _id
  }) {
    let item = ScheduledScans.findOne({ _id: _id });
    console.log('scheduled scan for remove: ', item);

    ScheduledScans.remove({ _id: _id });
  }
});
