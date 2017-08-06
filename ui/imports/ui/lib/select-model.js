import * as R from 'ramda'; 

export const createSelectArgs = function (params) {
  let instance = Template.instance();

  return {
    values: params.hash.values,
    type: params.hash.type,
    placeholder: params.hash.placeholder,
    options: params.hash.options,
    multi: params.hash.multi ? params.hash.multi : false, 
    disabled: params.hash.disabled,
    setModel: params.hash.setModel ? params.hash.setModel.fn : 
      function (values) {
        let model = instance.data.model; 
        let newModel = R.assoc(params.hash.key, values, model);
        if (instance.data.setModel) {
          instance.data.setModel(newModel); 
        }
      },
    showNullOption: R.isNil(params.hash.showNullOption) ? false : params.hash.showNullOption
  };
};
