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

import { CliqueConstraints } from './clique-constraints';

export const insert = new ValidatedMethod({
  name: 'clique_constraints.insert',
  validate: CliqueConstraints.simpleSchema()
    .pick([
      'focal_point_type',
      'environment',
      'constraints',
      'constraints.$',
    ]).validator({ clean: true, filter: false }),
  run({
 //   environment,
    focal_point_type,
    environment,
    constraints,
  }) {
    if (! Roles.userIsInRole(Meteor.userId(), 'manage-clique-constraints', Roles.GLOBAL_GROUP)) {
      throw new Meteor.Error('unauthorized for inserting clique constraints');
    }

    let cliqueConstraint = CliqueConstraints.schema.clean({});

    cliqueConstraint = R.merge(cliqueConstraint, {
  //    environment,
      focal_point_type,
      environment,
      constraints,
    });

    CliqueConstraints.insert(cliqueConstraint);
  }
});

export const remove = new ValidatedMethod({
  name: 'clique_constraints.remove',
  validate: CliqueConstraints.simpleSchema()
    .pick([
      '_id',
    ]).validator({ clean: true, filter: false }),
  run({
    _id
  }) {
    if (! Roles.userIsInRole(Meteor.userId(), 'manage-clique-constraints', Roles.DEFAULT_GROUP)) {
      throw new Meteor.Error('unauthorized for removing clique constraints');
    }

    let cliqueConstraint = CliqueConstraints.findOne({ _id: _id });
    console.log('clique constraint for remove: ', cliqueConstraint);

    CliqueConstraints.remove({ _id: _id });
  }
});

export const update = new ValidatedMethod({
  name: 'clique_constraints.update',
  validate: CliqueConstraints.simpleSchema()
    .pick([
      '_id',
      'focal_point_type',
      'environment',
      'constraints',
      'constraints.$',
    ]).validator({ clean: true, filter: false }),
  run({
    _id,
    focal_point_type,
    environment,
    constraints,
  }) {

    if (! Roles.userIsInRole(Meteor.userId(), 'manage-clique-constraints', Roles.DEFAULT_GROUP)) {
      throw new Meteor.Error('unauthorized for removing clique constraints');
    }

    let item = CliqueConstraints.findOne({ _id: _id });
    console.log('clique constraints for update: ', item);
    console.log('current user', Meteor.userId());

    item = R.merge(
      R.pick([
        'focal_point_type',
        'environment',
        'constraints',
      ], item), {
        focal_point_type,
        environment,
        constraints,
      });

    CliqueConstraints.update({ _id: _id }, { $set: item });
  }
});
