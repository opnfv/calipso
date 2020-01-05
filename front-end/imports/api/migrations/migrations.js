///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import { CliqueTypes } from '/imports/api/clique-types/clique-types';

Migrations.add({
  version: 1,
  up: () => {
    console.log('migrating: add clique type constaints for env+name, env+focal_point_type');
    CliqueTypes._ensureIndex({ environment: 1, name: 1 });
    CliqueTypes._ensureIndex({ environment: 1, focal_point_type: 1 });
  },
  down: () => {
  }
});
