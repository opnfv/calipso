/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { ValidatedMethod } from 'meteor/mdg:validated-method';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';
import { Roles } from 'meteor/alanning:roles';
import { Environments } from '/imports/api/environments/environments';

let userSchema = new SimpleSchema({
  _id: { type: String },
  username: { type: String },
  password: { type: String },
  viewEnvs: { type: [ String ] },
  editEnvs: { type: [ String ] },
});

export const insert = new ValidatedMethod({
  name: 'accounts.insert',
  validate: userSchema
    .pick([
      'username',
      'password',
      'viewEnvs',
      'viewEnvs.$',
      'editEnvs',
      'editEnvs.$',
    ]).validator({ clean: true, filter: false }),
  run({
    username,
    password,
    viewEnvs,
    editEnvs,
  }) {
    if (! Roles.userIsInRole(Meteor.userId(), 'manage-users', Roles.GLOBAL_GROUP)) {
      throw new Meteor.Error('unauthorized for removing users');
    }

    let userId = Accounts.createUser({
      username: username,
      password: password
    });

    addRole(viewEnvs, 'view-env', userId);
    addRole(editEnvs, 'edit-env', userId);
  }
});



export const update = new ValidatedMethod({
  name: 'accounts.update',
  validate: userSchema
    .pick([
      '_id',
     // 'password',
      'viewEnvs',
      'viewEnvs.$',
      'editEnvs',
      'editEnvs.$',
    ]).validator({ clean: true, filter: false }),
  run({
    _id,
    //_password,
    viewEnvs,
    editEnvs,
  }) {
    console.log('accounts - methods - update - start');
    //throw new Meteor.Error('unimplemented');
    if (! Roles.userIsInRole(Meteor.userId(), 'manage-users', Roles.GLOBAL_GROUP)) {
      throw new Meteor.Error('unauthorized for updating users');
    }

    /*
    let item = Meteor.users.findOne({ _id: _id });
    console.log('user for update: ', item);

    item = R.merge(R.pick([
      'password',
    ], item), {
      password
    });
    */

    /*
    let item = {
      //password
    };

    Meteor.users.update({ _id: _id }, { $set: item });
    */

    let currentViewEnvs = R.map((env) => {
      return env.name;
    }, Environments.find({ 'auth.view-env': { $in: [ _id  ] }}).fetch());

    let viewEnvsForDelete = R.difference(currentViewEnvs, viewEnvs);
    let viewEnvsForAdd = R.difference(viewEnvs, currentViewEnvs);

    removeRole(viewEnvsForDelete, 'view-env', _id);
    addRole(viewEnvsForAdd, 'view-env', _id);

    //

    let currentEditEnvs = R.map((env) => {
      return env.name;
    }, Environments.find({ 'auth.edit-env': { $in: [ _id  ] }}).fetch());

    let editEnvsForDelete = R.difference(currentEditEnvs, editEnvs);
    let editEnvsForAdd = R.difference(editEnvs, currentEditEnvs);

    removeRole(editEnvsForDelete, 'edit-env', _id);
    addRole(editEnvsForAdd, 'edit-env', _id);

    console.log('accounts - methods - update - end');
  }
});

export const remove = new ValidatedMethod({
  name: 'accounts.remove',
  validate: userSchema
    .pick([
      '_id',
    ]).validator({ clean: true, filter: false }),
  run({
    _id
  }) {
    if (! Roles.userIsInRole(Meteor.userId(), 'manage-users', Roles.GLOBAL_GROUP)) {
      throw new Meteor.Error('unauthorized for removing users');
    }

    let user = Meteor.users.findOne({ _id: _id });
    console.log('user for remove: ', user);

    Meteor.users.remove({ _id: _id });
  }
});

function removeRole(rolesForRemoval, roleName, userId) {
  R.forEach((envName) => {
    let env = Environments.findOne({ name: envName });
    let auth = env.auth;
    if (R.isNil(auth)) { auth = { }; }
    if (R.isNil(R.path([roleName], auth))) {
      auth = R.assoc(roleName, [], auth);
    }
    auth = R.assoc(roleName, R.reject(R.equals(userId), auth[roleName]), auth);

    updateEnv(auth, env);
    //let newEnv = R.merge(env, { auth: auth });

  }, rolesForRemoval);
}

function addRole(rolesForAdd, roleName, userId) {
  R.forEach((envName) => {
    let env = Environments.findOne({ name: envName });
    let auth = env.auth;
    if (R.isNil(auth)) { auth = { }; }
    if (R.isNil(R.path([roleName], auth))) {
      auth = R.assoc(roleName, [], auth);
    }
    auth = R.assoc(roleName, R.append(userId, auth[roleName]), auth);

    updateEnv(auth, env);
    //let newEnv = R.merge(env, { auth: auth });

  }, rolesForAdd);
}

function updateEnv(auth, env) {
  console.log('update env. set: ' + R.toString(auth));
  try {
    Environments.update(env._id, {
      $set: {
        auth: auth,
        configuration: env.configuration,
        //distribution: distribution,
        //name: name,
        type_drivers: env.type_drivers,
        mechanism_drivers: env.mechanism_drivers,
        listen: env.listen,
        enable_monitoring: env.enable_monitoring,
      }
    });
  } catch(e) {
    console.error('error in update: ' + R.toString(e));
    throw new Meteor.Error('enviornment update error',
      `unable to update ACL for environment - ${env.name}. Please check envrironment info. ${e.message}`);
  }
}
