/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { ValidatedMethod } from 'meteor/mdg:validated-method';
import * as R from 'ramda';

import { Scans } from './scans';

export const insert = new ValidatedMethod({
  name: 'scans.insert',
  validate: Scans.simpleSchema()
    .pick([
      'environment',
      'object_id',
      'log_level',
      'clear',
      'loglevel',
      'scan_only_inventory',
      'scan_only_links',
      'scan_only_cliques',
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
  }) {
    let scan = Scans.schema.clean({
      status: 'pending'
    });
    scan = R.merge(scan, {
      environment,
      object_id,
      log_level,
      clear,
      loglevel,
      scan_only_inventory,
      scan_only_links,
      scan_only_cliques,
      submit_timestamp: Date.now()
    });

    Scans.insert(scan);
  },

});
