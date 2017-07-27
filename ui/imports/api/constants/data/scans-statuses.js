/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
export const Statuses = [{
  value: 'draft',
  label: 'Draft',
}, {
  value: 'pending',
  label: 'Pending',
}, {
  value: 'running',
  label: 'Running',
}, {
  value: 'completed',
  label: 'Completed',
}, { 
  value: 'failed',
  label: 'Failed',
}, {
  value: 'aborted',
  label: 'Aborted',
} 
]; 

export const StatusesInOperation = ['pending', 'running'];
