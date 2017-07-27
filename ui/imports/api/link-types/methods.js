/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { ValidatedMethod } from 'meteor/mdg:validated-method';
import * as R from 'ramda';
import { Roles } from 'meteor/alanning:roles';

import { LinkTypes } from './link-types';

export const insert = new ValidatedMethod({
  name: 'links_types.insert',
  validate: LinkTypes.simpleSchema()
    .pick([
      //'environment',
      'description',
      'endPointA',
      'endPointB',
    ]).validator({ clean: true, filter: false }),
  run({
    //environment,
    description,
    endPointA,
    endPointB
  }) {
    if (! Roles.userIsInRole(Meteor.userId(), 'manage-link-types', Roles.GLOBAL_GROUP)) {
      throw new Meteor.Error('unauthorized for inserting link type');
    }

    let linkType = LinkTypes.schema.clean({
    });

    let type = calcTypeFromEndPoints(endPointA, endPointB);

    linkType = R.merge(linkType, {
      description,
      endPointA,
      endPointB,
      type 
    });

    LinkTypes.insert(linkType);
  }
});

export const remove = new ValidatedMethod({
  name: 'links_types.remove',
  validate: LinkTypes.simpleSchema()
    .pick([
      '_id',
    ]).validator({ clean: true, filter: false }),
  run({
    _id
  }) {
    if (! Roles.userIsInRole(Meteor.userId(), 'manage-link-types', Roles.DEFAULT_GROUP)) {
      throw new Meteor.Error('unauthorized for removing link type');
    }

    let linkType = LinkTypes.findOne({ _id: _id });
    console.log('link type for remove: ', linkType);
    console.log('current user', Meteor.userId());

    LinkTypes.remove({ _id: _id });
  }
});

export const update = new ValidatedMethod({
  name: 'links_types.update',
  validate: LinkTypes.simpleSchema()
    .pick([
      '_id',
      'description',
      'endPointA',
      'endPointB',
    ]).validator({ clean: true, filter: false }),
  run({
    _id,
    description,
    endPointA,
    endPointB
  }) {
    if (! Roles.userIsInRole(Meteor.userId(), 'manage-link-types', Roles.DEFAULT_GROUP)) {
      throw new Meteor.Error('unauthorized for updating link type');
    }

    let linkType = LinkTypes.findOne({ _id: _id });
    console.log('link type for update: ', linkType);
    console.log('current user', Meteor.userId());

    let type = calcTypeFromEndPoints(endPointA, endPointB);

    linkType = R.merge(R.pick([
      'description', 
      'endPointA', 
      'endPointB', 
      'type'
    ], linkType), {
      description,
      endPointA,
      endPointB,
      type 
    });

    LinkTypes.update({ _id: _id }, { $set: linkType });
  }
});

function calcTypeFromEndPoints(endPointA, endPointB) {
  return `${endPointA}-${endPointB}`;
}
