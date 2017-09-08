/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
import { Mongo } from 'meteor/mongo';
import * as R from 'ramda';

export const NodeHoverAttr = new Mongo.Collection(
  'attributes_for_hover_on_data', { idGeneration: 'MONGO' });

export const calcAttrsForItem = function (node, attrsDefsRec) {
  if (R.isNil(attrsDefsRec)) {
    return [];
  }

  let attrsDefs = attrsDefsRec.attributes;

  return R.reduce((acc, attrDef) => {
    if (R.is(Array, attrDef)) {
      let value = R.path(attrDef, node);
      if (R.isNil(value)) { return acc; }
      let name = R.join('.', attrDef);
      return R.append(R.assoc(name, value, {}), acc);

    } else {
      return R.ifElse(R.isNil, 
        R.always(acc), 
        (attrVal) => R.append(R.assoc(attrDef, attrVal, {}), acc)
      )(R.prop(attrDef, node));
    }
  }, [], attrsDefs);
};
