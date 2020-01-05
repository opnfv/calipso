///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import { ValidatedMethod } from 'meteor/mdg:validated-method';
import * as R from 'ramda';
import { Roles } from 'meteor/alanning:roles';

import { CliqueTypes } from './clique-types';

export const insert = new ValidatedMethod({
  name: 'clique_types.insert',
  validate: CliqueTypes.simpleSchema()
    .pick([
      'environment',
      'focal_point_type',
      'environment_type',
      'distribution',
      'distribution_version',
      'mechanism_drivers',
      'type_drivers',
      'link_types',
      'link_types.$',
      'name',
      'use_implicit_links'
    ]).validator({ clean: true, filter: false }),
  run({
    environment,
    focal_point_type,
    environment_type,
    distribution,
    distribution_version,
    mechanism_drivers,
    type_drivers,
    link_types,
    name,
    use_implicit_links
  }) {
    if (! Roles.userIsInRole(Meteor.userId(), 'manage-clique-types', Roles.DEFAULT_GROUP)) {
      throw new Meteor.Error('unauthorized for adding clique type');
    }

    let cliqueType = CliqueTypes.schema.clean({});

    cliqueType = R.merge(cliqueType, {
      environment,
      focal_point_type,
      environment_type,
      distribution,
      distribution_version,
      mechanism_drivers,
      type_drivers,
      link_types,
      name,
      use_implicit_links
    });

    CliqueTypes.insert(cliqueType);
  }
});

export const remove = new ValidatedMethod({
  name: 'clique_types.remove',
  validate: CliqueTypes.simpleSchema()
    .pick([
      '_id',
    ]).validator({ clean: true, filter: false }),
  run({
    _id
  }) {

    if (! Roles.userIsInRole(Meteor.userId(), 'manage-clique-types', Roles.DEFAULT_GROUP)) {
      throw new Meteor.Error('unauthorized for removing clique type');
    }

    let cliqueType = CliqueTypes.findOne({ _id: _id });
    console.log('clique type for remove: ', cliqueType);

    CliqueTypes.remove({ _id: _id });
  }
});

export const update = new ValidatedMethod({
  name: 'clique_types.update',
  validate: CliqueTypes.simpleSchema()
    .pick([
      '_id',
      'environment',
      'focal_point_type',
      'environment_type',
      'distribution',
      'distribution_version',
      'mechanism_drivers',
      'type_drivers',
      'link_types',
      'link_types.$',
      'name',
      'use_implicit_links'
    ]).validator({ clean: true, filter: false }),
  run({
    _id,
    environment,
    focal_point_type,
    environment_type,
    distribution,
    distribution_version,
    mechanism_drivers,
    type_drivers,
    link_types,
    name,
    use_implicit_links
  }) {
    if (! Roles.userIsInRole(Meteor.userId(), 'manage-clique-types', Roles.DEFAULT_GROUP)) {
      throw new Meteor.Error('unauthorized for updating clique type');
    }

    let cliqueType = CliqueTypes.findOne({ _id: _id });
    console.log('clique type for update: ', cliqueType);

    cliqueType = R.merge(R.pick([
      'environment',
      'focal_point_type',
      'environment_type',
      'distribution',
      'distribution_version',
      'mechanism_drivers',
      'type_drivers',
      'link_types',
      'name',
      'use_implicit_links'],
    cliqueType), {
      environment,
      focal_point_type,
      environment_type,
      distribution,
      distribution_version,
      mechanism_drivers,
      type_drivers,
      link_types,
      name,
      use_implicit_links
    });

    CliqueTypes.update({ _id: _id }, { $set: cliqueType });
  }
});
