/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
//import { Meteor } from 'meteor/meteor';
import * as R from 'ramda';
import { ValidatedMethod } from 'meteor/mdg:validated-method';

//import { SimpleSchema } from 'meteor/aldeed:simple-schema';

import { Environments } from './environments';
import { Inventory } from '/imports/api/inventories/inventories';
import { Links } from '/imports/api/links/links';
import { Cliques } from '/imports/api/cliques/cliques';
import { CliqueTypes } from '/imports/api/clique-types/clique-types';
import { Messages } from '/imports/api/messages/messages';
import { Scans } from '/imports/api/scans/scans';
import { Roles } from 'meteor/alanning:roles';

export const insert = new ValidatedMethod({
  name: 'environments.insert',
  validate: Environments.simpleSchema()
    .pick([
      'configuration', 
      'configuration.$', 
      'distribution', 
      'name', 
      'type_drivers',
      'mechanism_drivers',
      'mechanism_drivers.$',
      'listen',
      'enable_monitoring', 
      'aci',
    ]).validator({ clean: true, filter: false }), 
  //validate: null, 
  run({
    configuration,
    distribution,
    name,
    type_drivers,
    mechanism_drivers,
    listen,
    enable_monitoring,
    aci,
  }) {
    // todo: create clean object instance.
    let environment = Environments.schema.clean({
      user: Meteor.userId()
    });

    let auth = {
      'view-env': [
        Meteor.userId()
      ],
      'edit-env': [
        Meteor.userId()
      ]
    };

    environment = R.merge(environment, {
      configuration,
      distribution,
      name,
      type_drivers,
      mechanism_drivers,
      listen,
      enable_monitoring,
      auth,
      aci,
    });

    Environments.insert(environment);
  },
});

export const update = new ValidatedMethod({
  name: 'environments.update',
  validate: Environments.simpleSchema().pick([
    '_id',
    'configuration', 
    'configuration.$', 
    //'distribution', 
    //'name', 
    'type_drivers', 
    'mechanism_drivers', 
    'mechanism_drivers.$',
    'listen',
    'enable_monitoring',
    'aci',
  ]).validator({ clean: true, filter: false }),
  run({
    _id,
    configuration,
    //distribution,
    //name,
    type_drivers,
    mechanism_drivers,
    listen,
    enable_monitoring,
    aci,
  }) {
    let env = Environments.findOne({ _id: _id });

    if (! Roles.userIsInRole(Meteor.userId(), 'edit-env', 'default-group')) {
      if (! R.contains(Meteor.userId(), R.path(['auth', 'edit-env'], env) )) {
        throw new Meteor.Error('not-auth', 'unauthorized for updating env');
      }
    }

    Environments.update(_id, {
      $set: {
        configuration: configuration,
        //distribution: distribution,
        //name: name,
        type_drivers,
        mechanism_drivers,
        listen,
        enable_monitoring,
        aci,
      },
    });
  }
});

export const remove = new ValidatedMethod({
  name: 'environments.remove',
  validate: Environments.simpleSchema().pick([
    '_id',
  ]).validator({ clean: true, filter: false }),
  run({
    _id,
  }) {
    const env = Environments.findOne({ _id: _id });
    console.log('environment for remove: ', env);

    if (! Roles.userIsInRole(Meteor.userId(), 'edit-env', 'default-group')) {
      if (! R.contains(Meteor.userId(), R.path(['auth', 'edit-env'], env) )) {
        throw new Meteor.Error('not-auth', 'unauthorized for updating env');
      }
    }

    Inventory.remove({ environment: env.name }); 
    Links.remove({ environment: env.name });
    Cliques.remove({ environment: env.name });
    CliqueTypes.remove({ environment: env.name });
    Messages.remove({ environment: env.name });
    Scans.remove({ environment: env.name });
    Environments.remove({ _id: _id });
  }
});
