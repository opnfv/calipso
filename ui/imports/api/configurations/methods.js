/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { ValidatedMethod } from 'meteor/mdg:validated-method';
import { Configurations } from '/imports/api/configurations/configurations';
import * as R from 'ramda';

export const save = new ValidatedMethod({
  name: 'configurations.save',
  validate: Configurations.simpleSchema()
    .pick([
      'messages_view_backward_delta'
    ]).validator({ clean: true, filter: false }),
  run({
    messages_view_backward_delta
  }) {

    let userId = this.userId;
    let conf = Configurations.findOne({ user_id: userId });

    if (conf) {
      Configurations.update({ _id: conf._id}, { $set: {
        messages_view_backward_delta: messages_view_backward_delta
      }});
    } else {
      let item =  Configurations.schema.clean({});
      item = R.merge(item, {
        user_id: userId,
        messages_view_backward_delta: messages_view_backward_delta
      });
      Configurations.insert(item);
    }
  }
});
