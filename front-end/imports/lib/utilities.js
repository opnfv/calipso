///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import * as R from 'ramda';

export function idToStr(orgId) {
  return R.ifElse(R.is(Mongo.ObjectID),
    function (id) { return id.toHexString() + ':' + 'objectid'; },
    R.identity
  )(orgId);
}

export function parseReqId(pId) {
  let idMatch = R.match(/(.*):objectid$/, pId);
  if (idMatch.length === 0) {
    return {
      type: 'string',
      id: pId
    };
  } else {
    return {
      type: 'objectid',
      id: new Mongo.ObjectID(idMatch[1])
    };
  }
}

function calcColor(level) {
  if (level === 1)
    return "#FFFFFF";

  let r = 255;
  let g = 255;
  let b = 255;
  //let a = 1;
  let factor = level / 27;
  factor = factor < 0 ? 0 : 1 - factor;

  let nR = Math.floor(r * factor);
  let nG = Math.floor(g * factor);
  let nB = Math.floor(b * factor);
  //let nA = a;
  let colorStr = R.reduce((acc, colorPart) => {
    let digits = colorPart.toString(16);
    if (colorPart < 16) { digits = '0' + digits; }
    return acc + digits;
  }, '#', [nR, nG, nB]);

  return colorStr;
}

export let calcColorMem = R.memoize(calcColor);

export function toOptions(options) {
  return options.map(elem => ({ 'label': elem, 'value': elem }));
}

export function callApiValidators(context, validators) {
  if (R.isNil(context.docId)) {
    context.docId = context.field('_id').value;
  }
  for (let i = 0; i < validators.length; i++) {
    let error = validators[i](context);
    if (!R.isNil(error)) {
      return error;
    }
  }
}

export function isReferenceType(object_type) {
  return R.endsWith("_ref", object_type);
}

export function dereferenceType(object_type) {
  return R.split("_ref", object_type)[0];
}

export function isNullOrEmpty(objVal) {
  return R.or(R.isNil(objVal), R.isEmpty(objVal));
}
