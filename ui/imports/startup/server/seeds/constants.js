/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { Constants } from '/imports/api/constants/constants';
import * as R from 'ramda';
import { Distributions } from '/imports/api/constants/data/distributions';
//import { NetworkPlugins } from './data/network-plugins';
import { LogLevels } from '/imports/api/constants/data/log-levels';
import { MechanismDrivers } from '/imports/api/constants/data/mechanism-drivers';
import { ObjectTypesForLinks } from '/imports/api/constants/data/object-types-for-links';
import { TypeDrivers } from '/imports/api/constants/data/type-drivers';
import { EnvTypes } from '/imports/api/constants/data/env-types';
import { Statuses as ScansStatuses } from '/imports/api/constants/data/scans-statuses';
import { EnvironmentMonitoringTypes } from '/imports/api/constants/data/environment-monitoring-types';
import { EnvProvisionTypes } from '/imports/api/constants/data/environment-provision-types';
import { MessageSourceSystems } from '/imports/api/constants/data/message-source-systems';

let constantsDefaults = [{
  name: 'env_types',
  values: EnvTypes
}, {
  name: 'scans_statuses', 
  values: ScansStatuses
}, {
  name: 'environment_monitoring_types',
  values: EnvironmentMonitoringTypes
}, {
  name: 'distributions',
  values: Distributions
}, {
  name: 'log_levels',
  values: LogLevels
}, {
  name: 'mechanism_drivers',
  values: MechanismDrivers
}, {
  name: 'object_types_for_links',
  values: ObjectTypesForLinks
}, {
  name: 'type_drivers',
  values: TypeDrivers
}, {
  name: 'environment_provision_types',
  values: EnvProvisionTypes
}, {
  name: 'message_source_systems',
  values: MessageSourceSystems
}];

if (Meteor.server) {
  R.forEach((def) => {
    insertConstants(Constants, def.name, def.values);
  }, constantsDefaults);
}

function insertConstants(collection, name, values) {
  if (collection.find({ name: name}).count() === 0) {
    Constants.insert({
      name: name,
      data: values
    });
  }
}
