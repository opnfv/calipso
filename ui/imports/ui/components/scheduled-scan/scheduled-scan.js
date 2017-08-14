/*
 * Template Component: ScheduledScan 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { ReactiveDict } from 'meteor/reactive-dict';
import * as R from 'ramda';
import { RRule } from 'rrule';
import { ScheduledScans, 
  scansOnlyFields, 
  subsScheduledScansId,
} from '/imports/api/scheduled-scans/scheduled-scans';
import { Environments } from '/imports/api/environments/environments';
import { Constants } from '/imports/api/constants/constants';
import { insert, remove, update } from '/imports/api/scheduled-scans/methods';

import '/imports/ui/components/mt-select/mt-select';
import '/imports/ui/components/mt-input/mt-input';
import '/imports/ui/components/mt-radios/mt-radios';
        
import './scheduled-scan.html';     
    
/*  
 * Lifecycles
 */   
  
Template.ScheduledScan.onCreated(function() {
  var instance = this;

  instance.state = new ReactiveDict();
  instance.state.setDefault({
    action: null,
    _id: null,
    model: null,
    isError: false,
    isSuccess: false,
    isMessage: false,
    message: null,
    envsAsOptions: [],
    logLevelsAsOptions: [],
    pageHeader: 'Schedule a Scan',
    reload: null,
  });

  instance.autorun(function () {
    let data = Template.currentData();
    instance.state.get('reload');

    new SimpleSchema({
      _id: { 
        type: { _str: { type: String, regEx: SimpleSchema.RegEx.Id } }, 
        optional: true 
      },
      action: { type: String },
      env: { type: String, optional: true },
    }).validate(data);

    instance.state.set('action', data.action);
    instance.state.set('isError', false);
    instance.state.set('isSuccess', false);
    instance.state.set('isMessage', false);
    instance.state.set('message', null);
    instance.state.set('disabled', false);

    R.when(R.pipe(R.isNil, R.not), x => instance.state.set('_id', x))(data._id);
    R.when(R.pipe(R.isNil, R.not), x => instance.state.set('env', x))(data.env);
  });

  instance.autorun(function () {
    let currentOptions = instance.state.get('envsAsOptions');
    instance.subscribe('environments_config');
    let tempOptions = [];

    let addToOptionsDebounced = _.debounce(() => {
      if (currentOptions.length === tempOptions.length) {
        let result = R.intersectionWith(R.eqBy(R.prop('value')), tempOptions, currentOptions);
        if (result.length === currentOptions.length) {
          return;
        }
      }

      instance.state.set('envsAsOptions', tempOptions);
    }, 250);

    Environments.find({}).forEach((env) => {
      let option = envToOption(env);
      tempOptions = R.unionWith(R.eqBy(R.prop('value')), [option], tempOptions);
      addToOptionsDebounced();
    });
  });

  instance.autorun(function () {
    let currentOptions = instance.state.get('logLevelsAsOptions');
    instance.subscribe('constants');

    let tempOptions = [];

    let addToOptionsDebounced = _.debounce(() => {
      if (currentOptions.length === tempOptions.length) {
        let result = R.intersectionWith(R.eqBy(R.prop('value')), tempOptions, currentOptions);
        if (result.length === currentOptions.length) {
          return;
        }
      }

      instance.state.set('logLevelsAsOptions', tempOptions);
    }, 250);

    Constants.find({ name: 'log_levels' }).forEach((logLevelsRec) => {
      let logLevels = logLevelsRec.data;
      R.map((logLevel) => {
        let option = logLevelToOption(logLevel);
        tempOptions = R.unionWith(R.eqBy(R.prop('value')), [option], tempOptions);
        addToOptionsDebounced();
      }, logLevels);
    });

  });

  instance.autorun(function () {
    let action = instance.state.get('action');
    let _id = instance.state.get('_id');
    let env = instance.state.get('env');

    R.cond([
      [R.equals('insert'), _x => initInsertView(instance, env)],
      [R.equals('update'), _x => initUpdateView(instance, _id)],
      [R.equals('view'), _x => initViewView(instance, _id)],
      [R.equals('remove'), _x => initRemoveView(instance, _id)],
      [R.T, x => { throw `unimplemented action: ${R.toString(x)}`; }]
    ])(action);
  });
});  

/*
Template.ScheduledScan.rendered = function() {
};  
*/

/*
 * Events
 */

Template.ScheduledScan.events({
  'submit .sm-item-form': function(event, instance) {
    event.preventDefault(); 
    let model = instance.state.get('model');

    submitItem(instance, model);
  }
});
   
/*  
 * Helpers
 */

Template.ScheduledScan.helpers({    
  isUpdateableAction() {
    let instance = Template.instance();
    let action = instance.state.get('action');

    return R.contains(action, ['insert', 'update', 'remove']);
  },

  actionLabel: function () {
    let instance = Template.instance();
    let action = instance.state.get('action');
    return calcActionLabel(action);
  },

  asJson: function (val) {
    return JSON.stringify(val);
  },

  getState: function (key) {
    let instance = Template.instance();
    return instance.state.get(key);
  },

  modelField: function (fieldName) {
    let instance = Template.instance();
    return R.path([fieldName], instance.state.get('model'));
  },

  envsAsOptions: function () {
    let instance = Template.instance();
    return instance.state.get('envsAsOptions');
  },

  onInputInventoryFn: function () {
    let instance = Template.instance();
    return { fn: createSetModelFn(instance, 'inventory') };
  },

  onInputObjectIdFn: function () {
    let instance = Template.instance();
    return { fn: createSetModelFn(instance, 'object_id') };
  },

  onInputClearFn: function () {
    let instance = Template.instance();
    return { fn: createSetModelFn(instance, 'clear') };
  },

  onInputEnvFn: function () {
    let instance = Template.instance();
    return { fn: createSetModelFn(instance, 'environment') };
  },

  onInputLogLevelFn: function () {
    let instance = Template.instance();
    return { fn: createSetModelFn(instance, 'log_level') };
  },

  onInputFreqFn: function () {
    let instance = Template.instance();
    return { fn: createSetModelFn(instance, 'freq') };
  },

  argsSelect: function (args) {
    //let instance = Template.instance();
    let classStr = args.hash.classStr;
    let options = args.hash.options;
    let selectedValue = args.hash.selectedValue;
    let onInput = args.hash.onInput;
    let disabled = args.hash.disabled;

    return {
      classStr: classStr,
      selectedValue: selectedValue,
      isDisabled: disabled,
      options: options,
      onInput: onInput,
    };
  },

  scanOnlyFieldOptions: function () {
    return [
      { label: 'Full scan', value: '_full_scan' },
      { label: 'Scan only inventory', value: 'scan_only_inventory' },
      { label: 'Scan only links', value: 'scan_only_links' },
      { label: 'Scan only cliques', value: 'scan_only_cliques' },
    ];
  },

  scanOnlyFieldInputFn: function () {
    let instance = Template.instance();

    return { 
      fn: function (newFieldName) {
        let model = instance.state.get('model');
        model = R.reduce((acc, fieldName) => {
          return R.assoc(fieldName, false, acc);
        }, model, scansOnlyFields);

        if (newFieldName === '_full_scan') {
          console.log('full scan selected. all scan_only_ fields are reset');
        } else {
          model = R.assoc(newFieldName, true, model);
        }
        instance.state.set('model', model);
      }
    };
  },

  scanOnlyFieldsSelectedValue: function () {
    let instance = Template.instance();
    let model = instance.state.get('model');
    if (R.isNil(model)) { return null; }

    let selectedValue = R.find((fieldName) => {
      return R.prop(fieldName, model) === true;
    }, scansOnlyFields);

    if (R.isNil(selectedValue)) {
      selectedValue = '_full_scan';
    }
    return selectedValue;
  },

  argsRadios: function (options, onInputFn, selectedValue) {
    return {
      inputClasses: 'cl-input',
      options: options,
      selectedValue: selectedValue,
      onInput: onInputFn,
    };
  },

  freqsAsOptions: function () {
    return [
      { label: 'Yearly', value: 'YEARLY' },
      { label: 'Monthly', value: 'MONTHLY' },
      { label: 'Weekly', value: 'WEEKLY' },
      { label: 'Daily', value: 'DAILY' },
      { label: 'Hourly', value: 'HOURLY' },
    ];
  },

  argsInput: function (args) {
    let classStr = args.hash.classStr;
    let placeholder = args.hash.placeholder;
    let inputValue = args.hash.inputValue;
    let inputType = args.hash.inputType;
    let onInput = args.hash.onInput;
    let disabled = args.hash.disabled;

    return {
      inputValue: inputValue,
      inputType: inputType,
      classStr: classStr,
      placeholder: placeholder,
      isDisabled: disabled,
      onInput: onInput,
    };
  },

  getEnvsAsOptions: function () {
    let instance = Template.instance();
    return instance.state.get('envsAsOptions');
  },

  logLevelsAsOptions: function () {
    let instance = Template.instance();
    return instance.state.get('logLevelsAsOptions');
  },

  isGenDisabled: function () {
    let instance = Template.instance();
    let action = instance.state.get('action');
    if (R.contains(action, ['view', 'remove'])) {
      return true;
    }

    return false;
  },

  getRecurrenceText: function (model) {
    if (R.isNil(model)) { return ''; }

    let rule = new RRule({
      freq: RRule[model.freq]
    });

    return rule.toText();
  },

  getNextRunText: function (model) {
    if (R.isNil(model)) { return ''; }
    if (R.isNil(model.scheduled_timestamp)) { return ''; }

    let next = moment(model.scheduled_timestamp);
    return next.fromNow();
  },
}); // end: helpers


function initInsertView(instance, env) {
  instance.state.set('model', ScheduledScans.schema.clean({
    environment: env,
  }));

  subscribeToOptionsData(instance);
}

function initExistingItemView(instance, _id) {
  subscribeToOptionsData(instance);
  instance.subscribe(subsScheduledScansId, _id);

  ScheduledScans.find({ _id: _id }).forEach((model) => {
    instance.state.set('model', model);
  });
}

function initViewView(instance, _id) {
  initExistingItemView(instance, _id); 
}

function initUpdateView(instance, _id) {
  initExistingItemView(instance, _id); 
}

function initRemoveView(instance, _id) {
  initExistingItemView(instance, _id); 
}

function subscribeToOptionsData(_instance) {

}

function envToOption(env) {
  return { value: env.name, label: env.name };
}

function logLevelToOption(logLevel) {
  return { value: logLevel.value, label: logLevel.label };
}

function createSetModelFn(instance, fieldName) {
  return function (value) {
    let model = instance.state.get('model');
    model = R.assoc(fieldName, value, model);
    instance.state.set('model', model);
  };
}

function calcActionLabel(action) {
  switch (action) {
  case 'insert':
    return 'Add';
  case 'remove':
    return 'Remove';
  case 'update':
    return 'Update';
  default:
    return 'Submit';
  }
}

function submitItem(
  instance, 
  model
) {

  let action = instance.state.get('action');

  instance.state.set('isError', false);
  instance.state.set('isSuccess', false);
  instance.state.set('isMessage', false);
  instance.state.set('message', null);

  switch (action) {
  case 'insert':
    insert.call({
      environment: model.environment,
      object_id: model.object_id,
      log_level: model.log_level,
      clear: model.clear,
      scan_only_inventory: model.scan_only_inventory,
      scan_only_links: model.scan_only_links,
      scan_only_cliques: model.scan_only_cliques,
      freq: model.freq,
    }, processActionResult.bind(null, instance));
    break;

  case 'update': 
    update.call({
      _id: model._id,
      environment: model.environment,
      object_id: model.object_id,
      log_level: model.log_level,
      clear: model.clear,
      scan_only_inventory: model.scan_only_inventory,
      scan_only_links: model.scan_only_links,
      scan_only_cliques: model.scan_only_cliques,
      freq: model.freq,
    }, processActionResult.bind(null, instance));
    break;

  case 'remove':
    remove.call({
      _id: model._id,
    }, processActionResult.bind(null, instance));
    break;

  default:
      // todo
    break;
  }
}

function processActionResult(instance, error) {
  let action = instance.state.get('action');

  if (error) {
    instance.state.set('isError', true);
    instance.state.set('isSuccess', false);
    instance.state.set('isMessage', true);

    if (typeof error === 'string') {
      instance.state.set('message', error);
    } else {
      instance.state.set('message', error.message);
    }

    return;
  }

  instance.state.set('isError', false);
  instance.state.set('isSuccess', true);
  instance.state.set('isMessage', true);

  switch (action) {
  case 'insert':
    instance.state.set('message', 'Record had been added successfully');
    instance.state.set('disabled', true);
    break;  

  case 'remove':
    instance.state.set('message', 'Record had been removed successfully');
    instance.state.set('disabled', true);
    break;

  case 'update':  
    instance.state.set('message', 'Record had been updated successfully');
    break;
  }

  //Router.go('/link-types-list');
  setTimeout(() => {
    instance.state.set('reload', Date.now());
  }, 7000);
}
