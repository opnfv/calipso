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

export const NfvProviderSchema = new SimpleSchema({
  name: { type: String, autoValue: function () { return 'NFV_provider'; } },
  host: { 
    type: String,
    regEx: SimpleSchema.RegEx.IP,
  },
  nfv_token: { type: String },
  port: { 
    type: String, 
    regEx: portRegEx
  },
  user: { type: String },
  pwd: { type: String },
});
