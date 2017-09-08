/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////

import { Links } from '../links';
import { NodeHoverAttr, calcAttrsForItem } from '/imports/api/attributes_for_hover_on_data/attributes_for_hover_on_data';
import * as R from 'ramda';

Meteor.methods({
  'linksFind?DataAndAttrs': function (id) {
    console.log(`method server: linksFind?DataAndAttrs. ${R.toString(id)}`);
    //check(nodeId, ObjectId);
    this.unblock();

    let query = { _id: id };
    let link = Links.findOne(query);
    let attrsDefs = NodeHoverAttr.findOne({ 'type': 'link' });
    let attributes = calcAttrsForItem(link, attrsDefs);

    return {
      link: link,
      linkName: link.link_name,
      attributes: attributes
    };
  },
});
