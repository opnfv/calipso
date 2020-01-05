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
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';
import { Constants } from '/imports/api/constants/constants';
import { MysqlSchema } from './configuration-groups/mysql-configuration';
import { OpenStackSchema } from './configuration-groups/open-stack-configuration';
import { MonitoringSchema } from './configuration-groups/monitoring-configuration';
import { CLISchema } from './configuration-groups/cli-configuration';
import { AMQPSchema } from './configuration-groups/amqp-configuration';
import { KubeSchema } from './configuration-groups/kubernetes-configuration';
//import { NfvProviderSchema } from './configuration-groups/nfv-provider-configuration';
import { AciSchema } from './configuration-groups/aci-configuration';
import {
  isMonitoringSupported,
  isListeningSupported,
} from '/imports/api/supported_environments/supported_environments';

export const Environments = new Mongo.Collection(
  'environments_config', { idGeneration: 'MONGO' });

export const envSpecificConfGroups = ['OpenStack', 'Kubernetes', 'mysql', 'CLI'];
export const requiredConfGroups = {
    'OpenStack': ['OpenStack', 'mysql', 'CLI'],
    'Kubernetes': ['Kubernetes', 'CLI']
};

export const optionalConfGroups = [
  // 'NFV_provider',
  'AMQP',
  'Monitoring',
  'ACI',
];

let simpleSchema = new SimpleSchema({
  _id: { type: { _str: { type: String, regEx: SimpleSchema.RegEx.Id } } },
  auth: {
    type: Object,
    blackbox: true,
    defaultValue: {
      'view-env': [
      ],
      'edit-env': [
      ]
    }
  },
  environment_type: {
    type: String,
    defaultValue: 'OpenStack',
    custom: function () {
        let that = this;
        let env_types = Constants.findOne({ name: 'environment_types' });

        if (R.isNil(env_types.data)) { return 'notAllowed'; }
        let types = env_types.data;

        if (R.isNil(R.find(R.propEq('value', that.value), types))) {
            return 'notAllowed';
        }
    },
  },
  configuration: {
    type: [Object],
    blackbox: true,
    autoValue: function () {
      console.log('start - autovalue - environment - configuration');
      //console.log(this);
      let that = this;
      let dbNode = getDbNode(that);
      let environmentType = extractValue('environment_type', that, dbNode);
      let requiredGroups = requiredConfGroups[environmentType];

      if (that.isSet) {
        let confGroups = that.value;

        let {
          isMonitoringSupportedRes,
          amqpConfigRequired,
          enable_monitoring, 
          listen 
        } = extractCalcEnvSupportedRelatedValues(that);
        let aci_enabled = extractValue('aci_enabled', that, dbNode);

        if (enable_monitoring && isMonitoringSupportedRes) {
          if (! R.find(R.propEq('name', 'Monitoring'), confGroups)) {
            confGroups = R.append(createNewConfGroup('Monitoring'), confGroups);
          }
        } else {
          console.log('env - configurations - autovalue - monitoring not supported');
          confGroups = R.reject(R.propEq('name', 'Monitoring'), confGroups);
        }

        if (listen && amqpConfigRequired) {
          if (! R.find(R.propEq('name', 'AMQP'), confGroups)) {
            confGroups = R.append(createNewConfGroup('AMQP'), confGroups);
          }
        } else {
          console.log('env - configurations - autovalue - AMQP not requested');
          confGroups = R.reject(R.propEq('name', 'AMQP'), confGroups);
        }

        if (aci_enabled) {
          if (! R.find(R.propEq('name', 'ACI'), confGroups)) {
            confGroups = R.append(createNewConfGroup('ACI'), confGroups);
          }
        } else {
          console.log('env - configurations - autovalue - aci not requested');
          confGroups = R.reject(R.propEq('name', 'ACI'), confGroups);
        }

        for (let i = 0; i < envSpecificConfGroups.length; i++) {
          let group = envSpecificConfGroups[i];
          if (requiredGroups.includes(group)) {
            if (!R.find(R.propEq('name', group), confGroups)) {
              confGroups = R.append(createNewConfGroup(group), confGroups);
            }
          }
          else {
              console.log('env - configurations - autovalue -', group, ' not requested');
              confGroups = R.reject(R.propEq('name', group), confGroups);
          }
        }

        confGroups = cleanOptionalGroups(confGroups, optionalConfGroups);
        console.log('env - configurations - autovalue - after clean optional groups');

        let newValue = R.map(function(confGroup) {
          let schema = getSchemaForGroupName(confGroup.name);
          return schema.clean(confGroup);
        }, confGroups);

        console.log('end - autovalue - environment - configurations');
        console.log(newValue);
        return newValue;

      } else {
        console.log('env - configurations - autovalue - is not set');
        let newValue = R.map((confName) => {
          let schema = getSchemaForGroupName(confName);
          return schema.clean({});
        }, requiredGroups);
        console.log('end - autovalue - environment - configurations');
        console.log(newValue);
        return newValue;
      }
    },
    custom: function () {
      console.log('start - custom - environment - configurations');
      //console.log(this);
      let that = this;
      let configurationGroups = that.value;

      let subErrors = [];

      let { 
        isMonitoringSupportedRes,
        amqpConfigRequired,
        enable_monitoring, 
        listen 
      } = extractCalcEnvSupportedRelatedValues(that);

      let dbNode = getDbNode(that);
      let environmentType = extractValue('environment_type', that, dbNode);
      let requiredGroups = requiredConfGroups[environmentType];
      let requiredConfGroupsTemp = R.clone(requiredGroups);
      if (enable_monitoring && isMonitoringSupportedRes) {
        requiredConfGroupsTemp = R.append('Monitoring', requiredConfGroupsTemp);
      }
      if (listen && amqpConfigRequired) {
        requiredConfGroupsTemp = R.append('AMQP', requiredConfGroupsTemp);
      }

      console.log('env - configurations - custom - after mon & listen check');

      let invalidResult = R.find(function(groupName) {
        subErrors = checkGroup(groupName, configurationGroups, true);
        if (subErrors.length > 0) { return true; }
        return false;
      }, requiredConfGroupsTemp);

      console.log(`env - configurations - custom - after require groups check`);

      if (R.isNil(invalidResult)) {
        invalidResult = R.find(function(groupName) {
          subErrors = checkGroup(groupName, configurationGroups, false);
          if (subErrors.length > 0) { return true; }
          return false;
        }, optionalConfGroups);
      }

      console.log(`env - configurations - custom - after optional groups check`);

      if (! R.isNil(invalidResult)) {
        console.log(`env - configrations - custom - invalid result end: ${R.toString(subErrors)}`);
        throw {
          isError: true,
          type: 'subGroupError',
          data: subErrors,
          message: constructSubGroupErrorMessage(subErrors)
        };
      }
    },

  },
  user: {
    type: String,
  },
  distribution: {
    type: String,
    defaultValue: 'Mirantis',
    custom: function () {
      let that = this;
      let constsDist = Constants.findOne({ name: 'distributions' });

      if (R.isNil(constsDist.data)) { return 'notAllowed'; }
      let distributions = constsDist.data;

      if (R.isNil(R.find(R.propEq('value', that.value), distributions))) {
        return 'notAllowed';
      }
    },
  },
  distribution_version: {
    type: String,
    defaultValue: '',
    custom: function () {
      let that = this;
      let constsDist = Constants.findOne({ name: 'distribution_versions' });

      if (R.isNil(constsDist.data)) { return 'notAllowed'; }
      let dist_versions = constsDist.data;

      if (R.isNil(R.find(R.propEq('value', that.value), dist_versions))) {
        return 'notAllowed';
      }
    },
  },
  last_scanned: {
    type: String, defaultValue: ''
  },
  name: {
    type: String,
    defaultValue: 'MyEnvironmentName',
    min: 6,
    custom: function () {
      let that = this;

      let existing = Environments.findOne({
          'name': that.value
      });

      if (!R.isNil(existing) && existing._id !== that.field('_id').value) {
        return "alreadyExists";
      }
    }
  },
  type_drivers: {
    type: String,
    defaultValue: '',
    custom: function () {
      let that = this;
      let TypeDriversRec = Constants.findOne({ name: 'type_drivers' });

      if (R.isNil(TypeDriversRec.data)) { return 'notAllowed'; }
      let TypeDrivers = TypeDriversRec.data;

      if (R.isNil(R.find(R.propEq('value', that.value), TypeDrivers))) {
        return 'notAllowed';
      }
    },
  },

  mechanism_drivers: {
    type: [String],
    defaultValue: [],
    minCount: 1,
    custom: function () {
      let that = this;
      let consts = Constants.findOne({ name: 'mechanism_drivers' });

      if (R.isNil(consts.data)) { return 'notAllowed'; }
      let mechanismDrivers = consts.data;

      let result = R.find((driver) => {
        if (R.find(R.propEq('value', driver), mechanismDrivers)) {
          return false;
        }
        return true;
      }, that.value);

      if (result) { return 'notAllowed'; }

    },
  },

  operational: {
    type: String,
    allowedValues: ['stopped', 'running', 'error'],
    defaultValue: 'stopped'
  },

  scanned: { type: Boolean, defaultValue: false },

  type: {
    type: String,
    autoValue: function () {
      return 'environment';
    },
  },

  app_path: {
    type: String,
    defaultValue: '/home/scan/calipso_prod/app'
  },

  listen: {
    type: Boolean,
    autoValue: function () {
      console.log('env - listen - autoValue - start');
      let that = this;
      let newValue = that.value;
      console.log(`- current value: ${R.toString(newValue)}`);

      let { isListeningSupportedRes } = extractCalcEnvSupportedRelatedValues(that);

      if (!isListeningSupportedRes) {
        console.log('* listening not supported');
        console.log(`* ${R.toString(isListeningSupportedRes)}`);
        newValue = false;
      }

      return newValue;
    },
  },

  enable_monitoring: {
    type: Boolean,
    autoValue: function () {
      console.log('env - enable_monitoring - autoValue - start');
      let that = this;
      let newValue = that.value;
      console.log(`- current value: ${R.toString(newValue)}`);

      let { isMonitoringSupportedRes } = extractCalcEnvSupportedRelatedValues(that);

      if (!isMonitoringSupportedRes) {
        console.log('* monitoring not supported');
        console.log(`* ${R.toString(isMonitoringSupportedRes)}`);
        newValue = false;
      }

      return newValue;
    },
  },
  aci_enabled: {
    type: Boolean,
    defaultValue: false,
  },
});

/*
simpleSchema.addValidator(function () {
  //let that = this;
});
*/

// Bug in simple schema. cant add custom message to instance specific
// schema.
// https://github.com/aldeed/meteor-simple-schema/issues/559
// Version 2 fixes it but it is rc.
//Environments.schema.messages({
SimpleSchema.messages({
  confGroupInvalid: 'Configuration group is invalid.'
});

Environments.schema = simpleSchema;
Environments.attachSchema(Environments.schema);

Environments.findAllNames = function () {
  return Environments.find({}).map((elem) => {return elem.name;});
};

export function getSchemaForGroupName(groupName) {
  switch (groupName) {
  case 'mysql':
    return MysqlSchema;
  case 'OpenStack':
    return OpenStackSchema;
  case 'CLI':
    return CLISchema;
  case 'AMQP':
    return AMQPSchema;
  //  case 'NFV_provider':
  //    return NfvProviderSchema;
  case 'ACI':
    return AciSchema;
  case 'Monitoring':
    return MonitoringSchema;
  case 'Kubernetes':
    return KubeSchema;
  default:
    throw 'group name is not recognized. group: ' + groupName;
  }
}

function constructSubGroupErrorMessage(errors) {
  let message = 'Validation errors on sub groups:';
  message = message + R.reduce((acc, item) => {
    return acc + '\n- ' + item.group + ': ' + item.message;
  }, '', errors);

  return message;
}

function checkGroup(groupName, configurationGroups, groupRequired) {
  let subErrors = [];
  let confGroup = R.find(R.propEq('name', groupName), configurationGroups);

  if (R.isNil(confGroup)) {
    if (groupRequired) {
      subErrors = R.append({
        field: 'configuration',
        group: groupName,
        message: 'group ' + groupName + ' is required'
      }, subErrors);
    }
    return subErrors;
  }

  let validationContext = getSchemaForGroupName(groupName).newContext();

  if (! validationContext.validate(confGroup)) {
    subErrors = R.reduce(function (acc, invalidField) {
      return R.append({
        field: invalidField,
        group: groupName,
        message: validationContext.keyErrorMessage(invalidField.name),
      }, acc);
    }, [], validationContext.invalidKeys());

    return subErrors;
  }

  return subErrors;
}

export function createNewConfGroup(groupName) {
  let schema = getSchemaForGroupName(groupName);
  return schema.clean({});
}

function cleanOptionalGroups(confGroups, optionalConfGroups) {
  return R.filter((conf) => {
    if (R.contains(conf.name, optionalConfGroups)) {
      return !isConfEmpty(conf);
    }

    return true;
  }, confGroups);
}

function isConfEmpty(conf) {
  return ! R.any((key) => {
    if (key === 'name') { return false; } // We ignore the key 'name'. It is a 'type' key.
    let val = conf[key];
    return ! ( R.isNil(val) || R.isEmpty(val));
  })(R.keys(conf));
}

function extractValue(name, schemaValidator, dbNode) {
  console.log('env - extract value');
  console.log(`-name: ${R.toString(name)}`);
  //console.log(`-schemaValidator: ${R.toString(schemaValidator)}`);
  console.log(`-dbNode: ${R.toString(dbNode)}`);

  let field = schemaValidator.field(name);
  let value = field.value;

  console.log(`extract value - schema value: ${R.toString(value)}`);

  if (R.isNil(field.value) && !field.isSet && dbNode) {
    console.log(`extract value - db value: ${R.toString(dbNode[name])}`);
    value = dbNode[name];
  }

  console.log(`extract value - result: ${R.toString(value)}`);
  return value;
}

function getDbNode(schemaHelper) {
  let _id = R.defaultTo(schemaHelper.docId, R.path(['value'], schemaHelper.field('_id')));
  let dbNode = R.defaultTo(null, Environments.findOne({ _id: _id }));
  return dbNode;
}

function extractCalcEnvSupportedRelatedValues(schemaHelper) {
  let dbNode = getDbNode(schemaHelper);

  let dist = extractValue('distribution', schemaHelper, dbNode);
  let dist_version = extractValue('distribution_version', schemaHelper, dbNode);
  let typeDrivers = extractValue('type_drivers', schemaHelper, dbNode);
  let mechDrivers = extractValue('mechanism_drivers', schemaHelper, dbNode);
  let enable_monitoring = extractValue('enable_monitoring', schemaHelper, dbNode);
  let listen = extractValue('listen', schemaHelper, dbNode);
  let environmentType = extractValue('environment_type', schemaHelper, dbNode);

  let isMonitoringSupportedRes = isMonitoringSupported(dist, dist_version, typeDrivers, mechDrivers);
  let isListeningSupportedRes = isListeningSupported(dist, dist_version, typeDrivers, mechDrivers);
  let amqpConfigRequired = isListeningSupportedRes && environmentType === 'OpenStack';

  return {
    enable_monitoring,
    listen,
    isMonitoringSupportedRes,
    isListeningSupportedRes,
    amqpConfigRequired,
  };
}
