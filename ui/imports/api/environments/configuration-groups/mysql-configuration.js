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

export const MysqlSchema = new SimpleSchema({
  name: { 
    type: String, 
    autoValue: function () { return 'mysql'; } 
  },
  host: { 
    type: String,
    regEx: SimpleSchema.RegEx.IP,
    defaultValue: '10.0.0.1'
  },
  pwd: { type: String },
  port: { 
    type: String,
    regEx: portRegEx,
    defaultValue: '3307'
  },
  user: { 
    type: String, 
    min: 3,
    defaultValue: 'mysqluser'
  },
});
