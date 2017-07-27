/////////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others /
//                                                                                      /
// All rights reserved. This program and the accompanying materials                     /
// are made available under the terms of the Apache License, Version 2.0                /
// which accompanies this distribution, and is available at                             /
// http://www.apache.org/licenses/LICENSE-2.0                                           /
/////////////////////////////////////////////////////////////////////////////////////////
/*
 * file: input-model.js
 */

import * as R from 'ramda'; 

export const createInputArgs = function (params) {
  let instance = Template.instance();

  return {
    value: params.hash.value,
    type: params.hash.type,
    placeholder: params.hash.placeholder,
    disabled: params.hash.disabled,
    setModel: function (value) {
      let mainModel = instance.data.model; 
      let newMainModel = R.assoc(params.hash.key, value, mainModel);
      if (instance.data.setModel) {
        instance.data.setModel(newMainModel); 
      }
    },
  };
};
