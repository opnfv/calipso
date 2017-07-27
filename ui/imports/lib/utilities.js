/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
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
  let r = 11;
  let g = 122;
  let b = 209;
  //let a = 1;
  let factor = level / 15;
  factor = factor < 0 ? 0 : 1 - factor;

  let nR = Math.floor(r * factor);
  let nG = Math.floor(g * factor);
  let nB = Math.floor(b * factor);
  //let nA = a;
  let colorStr = R.reduce((acc, colorPart) => { 
    let digits =  colorPart.toString(16); 
    if (colorPart < 16) { digits = '0' + digits; }
    return acc + digits;
  }, '#', [nR, nG, nB]); 
  
  return colorStr;
}

export let calcColorMem = R.memoize(calcColor);
