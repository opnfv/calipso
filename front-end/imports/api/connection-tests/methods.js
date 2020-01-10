///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////

import * as R from 'ramda';
import { ValidatedMethod } from 'meteor/mdg:validated-method';
import { ConnectionTests } from './connection-tests';
import { getSchemaForGroupName } from '/imports/api/environments/environments';

export const insert = new ValidatedMethod({
  name: 'connection_tests.insert',
  validate: ConnectionTests.simpleSchema()
    .pick([
      'environment',
      'targets_configuration',
      'targets_configuration.$',
    ]).validator({ clean: true, filter: false }), 
  run({
    environment,
    targets_configuration,
  }) {
    let connection_test = ConnectionTests.schema.clean({});

    targets_configuration = R.filter((config) => {
      let validationContext = getSchemaForGroupName(config.name).newContext();
      try {
        let result = validationContext.validate(config);
        return result;
      } catch (_e) {
        return false;
      }
    }, targets_configuration);

    let test_targets = R.map((config) => config.name, targets_configuration);
    let submit_timestamp = Date.now()

    connection_test = R.merge(connection_test, {
      environment,
      test_targets,
      targets_configuration,
      submit_timestamp
    });

    let insertResult = ConnectionTests.insert(connection_test);
    return insertResult;
  },
});
