/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { portRegEx } from '/imports/lib/general-regex';

export const OpenStackSchema = new SimpleSchema({
  name: { type: String, autoValue: function () { return 'OpenStack'; } },
  host: { 
    type: String,
    regEx: SimpleSchema.RegEx.IP,
    defaultValue: '10.0.0.1',
  },
  admin_token: { type: String },
  port: { 
    type: String, 
    regEx: portRegEx,
    defaultValue: '5000',
  },
  user: { 
    type: String,
    defaultValue: 'adminuser'
  },
  pwd: { type: String },
});
