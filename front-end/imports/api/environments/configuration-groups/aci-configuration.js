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

export const AciSchema = new SimpleSchema({
  name: { 
    type: String, 
    autoValue: function () { return 'ACI'; } 
  },
  host: { 
    type: String,
    defaultValue: '10.0.0.1',
  },
  user: { 
    type: String, 
    defaultValue: 'admin'
  },
  pwd: { 
    type: String,
    defaultValue: '123456'
  },
});
