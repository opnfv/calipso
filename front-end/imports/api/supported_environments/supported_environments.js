///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import { Mongo } from 'meteor/mongo';
import * as R from 'ramda';

export const SupportedEnvironments = new Mongo.Collection(
  'supported_environments', { idGeneration: 'MONGO' });

export const subsNameSupportedEnvs = 'supported-environments';

export function isMonitoringSupported(
  distribution, 
  distribution_version, 
  type_drivers, 
  mechanism_drivers
) {
  console.log('isMonitoringSupported');
  console.log(`distribution: ${R.toString(distribution)}`);
  console.log(`distribution_version: ${R.toString(distribution_version)}`);
  console.log(`type_drivers: ${R.toString(type_drivers)}`);
  console.log(`mechanism_drivers: ${R.toString(mechanism_drivers)}`);

  let result = SupportedEnvironments.find({
    'environment.distribution': distribution,
    'environment.distribution_version': { $in: [ distribution_version ] },
    'environment.type_drivers': type_drivers,
    'environment.mechanism_drivers': { $in: mechanism_drivers },
    'features.monitoring': true
  }).count() > 0;

  console.log(`result: ${R.toString(result)}`);
  return result;
}

export function isListeningSupported(
  distribution, 
  distribution_version, 
  type_drivers, 
  mechanism_drivers
) {
  console.log('isListeningSupported');
  console.log(`distribution: ${R.toString(distribution)}`);
  console.log(`distribution: ${R.toString(distribution)}`);
  console.log(`type_drivers: ${R.toString(type_drivers)}`);
  console.log(`mechanism_drivers: ${R.toString(mechanism_drivers)}`);

  let result = SupportedEnvironments.find({
    'environment.distribution': distribution,
    'environment.distribution_version': { $in: [ distribution_version ] },
    'environment.type_drivers': type_drivers,
    'environment.mechanism_drivers': { $in: mechanism_drivers },
    'features.listening': true
  }).count() > 0;

  console.log(`result: ${R.toString(result)}`);
  return result;
}
