///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { portRegEx } from '/imports/lib/general-regex';

export const KubeSchema = new SimpleSchema({
  name: { type: String, autoValue: function () { return 'Kubernetes'; } },
  host: {
    type: String,
    defaultValue: '10.0.0.1',
  },
  port: {
    type: String,
    regEx: portRegEx,
    defaultValue: '6443',
  },
  user: {
    type: String,
    defaultValue: 'kube_user'
  },
  token: { type: String },
});
