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
