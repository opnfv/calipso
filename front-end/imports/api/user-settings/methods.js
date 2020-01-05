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
import { UserSettings } from '/imports/api/user-settings/user-settings';
import * as R from 'ramda';

export const save = new ValidatedMethod({
  name: 'user-settings.save',
  validate: UserSettings.simpleSchema()
    .pick([
      'messages_view_backward_delta'
    ]).validator({ clean: true, filter: false }),
  run({
    messages_view_backward_delta
  }) {

    let userId = this.userId;
    let userSettings = UserSettings.findOne({ user_id: userId });

    if (userSettings) {
      UserSettings.update({ _id: userSettings._id}, { $set: {
        messages_view_backward_delta: messages_view_backward_delta
      }});
    } else {
      let item =  UserSettings.schema.clean({});
      item = R.merge(item, {
        user_id: userId,
        messages_view_backward_delta: messages_view_backward_delta
      });
      UserSettings.insert(item);
    }
  }
});
