/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import * as R from 'ramda';

export function createGraphQuerySchema(
  env, 
  object_id, 
  type,
  flowType, 
  timeStart,
  timeEnd,
  sourceMacAddress,
  destinationMacAddress,
  sourceIPv4Address,
  destinationIPv4Address) {

  let schema = {
    environment: env, 
    object_id: object_id, 
    type: type,
    flowType: flowType, 
		/*
    averageArrivalNanoSeconds: {
      $gte: timeStart,
      //$lt: timeEnd
    }
		*/
    data_arrival_avg: {
      $gte: timeStart,
    }
  };

  if (! R.isNil(timeEnd)) {
    //schema = R.assocPath(['averageArrivalNanoSeconds', '$lt'], timeEnd, schema);
    schema = R.assocPath(['data_arrival_avg', '$lt'], timeEnd, schema);
  }

  switch (flowType) {
  case 'L2':
    schema = R.merge(schema, {
      sourceMacAddress: sourceMacAddress,
      destinationMacAddress: destinationMacAddress  
    });
    break;

  case 'L3':
    schema = R.merge(schema, {
      sourceIPv4Address: sourceIPv4Address,
      destinationIPv4Address: destinationIPv4Address
    });
    break;

  default:
    break;
  }

  return schema;
}
